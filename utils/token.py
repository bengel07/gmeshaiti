"""Service central de création et vérification des tokens GMES Haïti.

Les JWT sont séparés cryptographiquement par usage. Les tokens opaques sont
retournés en clair uniquement pour leur transmission; seule leur empreinte doit
être conservée en base de données.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

import jwt

ISSUER = "gmes-haiti"
CLES_INTERDITES = {"gmes-microcredit-2024", "changeme", "secret", "password", ""}
DUREES = {
    "mobile_access": timedelta(minutes=15),
    "mobile_refresh": timedelta(days=30),
    "conditions": timedelta(days=2),
    "conditions_pret": timedelta(days=2),
    "signature_client": timedelta(days=2),
    "retrait": timedelta(minutes=15),
}
MAX_ESSAIS_OTP = 5


class TokenInvalide(Exception):
    """Token absent, falsifié, expiré ou destiné à un autre usage."""


def _cle_maitre() -> bytes:
    cle = os.environ.get("TOKEN_MASTER_KEY", "").strip()
    if cle.lower() in CLES_INTERDITES or len(cle) < 32:
        raise RuntimeError(
            "TOKEN_MASTER_KEY manquante, connue ou trop courte "
            "(32 caractères minimum)."
        )
    return cle.encode("utf-8")


def cle_pour(usage: str) -> bytes:
    if not isinstance(usage, str) or not usage.strip():
        raise ValueError("Usage de token invalide.")
    return hmac.new(_cle_maitre(), b"gmes|" + usage.encode("utf-8"), hashlib.sha256).digest()


def verifier_configuration() -> None:
    """À appeler au démarrage; échoue si TOKEN_MASTER_KEY n'est pas configurée."""
    _cle_maitre()


def creer_jwt(usage: str, claims: dict[str, Any] | None = None, duree: timedelta | None = None) -> str:
    if usage not in DUREES:
        raise ValueError(f"Usage de token inconnu : {usage}")
    duree_effective = DUREES[usage] if duree is None else duree
    if not isinstance(duree_effective, timedelta) or duree_effective <= timedelta(0):
        raise ValueError("La durée du token doit être une durée positive.")
    duree_effective = min(duree_effective, DUREES[usage])
    maintenant = datetime.now(timezone.utc)
    payload = dict(claims or {})
    # Les champs de sécurité sont imposés et ne peuvent pas être remplacés par claims.
    payload.update({
        "iss": ISSUER,
        "aud": usage,
        "iat": maintenant,
        "nbf": maintenant,
        "exp": maintenant + duree_effective,
        "jti": uuid.uuid4().hex,
    })
    return jwt.encode(payload, cle_pour(usage), algorithm="HS256")


def verifier_jwt(token: str, usage: str) -> dict[str, Any]:
    if usage not in DUREES:
        raise ValueError(f"Usage de token inconnu : {usage}")
    if not token or not isinstance(token, str):
        raise TokenInvalide("Token manquant.")
    try:
        return jwt.decode(
            token.strip(), cle_pour(usage), algorithms=["HS256"],
            audience=usage, issuer=ISSUER, leeway=10,
            options={"require": ["exp", "iat", "nbf", "iss", "aud", "jti"]},
        )
    except jwt.ExpiredSignatureError as exc:
        raise TokenInvalide("Token expiré.") from exc
    except jwt.InvalidTokenError as exc:
        raise TokenInvalide("Token invalide.") from exc


def creer_jwt_mobile(user) -> str:
    claims = {
        "user_id": user.id,
        "tv": int(getattr(user, "token_version", 0) or 0),
    }
    if getattr(user, "role", None):
        claims["role"] = user.role
    if getattr(user, "client_id", None):
        claims["client_id"] = user.client_id
    return creer_jwt("mobile_access", claims)


def verifier_jwt_mobile(token: str, charger_user: Callable[[Any], Any]):
    data = verifier_jwt(token, "mobile_access")
    user = charger_user(data.get("user_id"))
    if user is None:
        raise TokenInvalide("Utilisateur introuvable.")
    if int(data.get("tv", -1)) != int(getattr(user, "token_version", 0) or 0):
        raise TokenInvalide("Session révoquée.")
    if not getattr(user, "actif", True) or getattr(user, "statut", "actif") not in ("actif", None):
        raise TokenInvalide("Compte inactif.")
    return user


def nouveau_token_opaque(octets: int = 32) -> tuple[str, str]:
    if not isinstance(octets, int) or octets < 16 or octets > 128:
        raise ValueError("La taille du token opaque doit être comprise entre 16 et 128 octets.")
    clair = secrets.token_urlsafe(octets)
    return clair, empreinte(clair)


def empreinte(token: str) -> str:
    if not isinstance(token, str):
        raise TypeError("Le token doit être une chaîne.")
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def correspond(token_recu: str | None, empreinte_stockee: str | None) -> bool:
    if not token_recu or not empreinte_stockee:
        return False
    return hmac.compare_digest(empreinte(token_recu), empreinte_stockee)


def nouvel_otp() -> tuple[str, str]:
    code = f"{secrets.randbelow(10**6):06d}"
    digest = hmac.new(cle_pour("retrait"), code.encode(), hashlib.sha256).hexdigest()
    return code, digest


def otp_valide(code_saisi: str | None, empreinte_stockee: str | None) -> bool:
    if not empreinte_stockee or not isinstance(empreinte_stockee, str):
        return False
    code = (code_saisi or "").strip()
    if len(code) != 6 or not code.isdigit():
        return False
    attendu = hmac.new(cle_pour("retrait"), code.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(attendu, empreinte_stockee)


def chiffres_aleatoires(n: int) -> str:
    if not isinstance(n, int) or n < 1 or n > 128:
        raise ValueError("Le nombre de chiffres doit être compris entre 1 et 128.")
    return "".join(str(secrets.randbelow(10)) for _ in range(n))
