
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

EXTENSIONS = {
    ".py", ".html", ".htm", ".js", ".ts",
    ".json", ".yaml", ".yml", ".toml", ".ini"
}

EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "__pycache__",
    "node_modules", "dist", "build"
}

# Termes et fonctions liés à la création ou validation des tokens.
PATTERNS = [
    r"\btoken\b",
    r"\btokens\b",
    r"\bcsrf\b",
    r"\bcsrf_token\b",
    r"\bgenerate_csrf\b",
    r"\bCSRFProtect\b",
    r"\bURLSafeTimedSerializer\b",
    r"\bURLSafeSerializer\b",
    r"\bTimedJSONWebSignatureSerializer\b",
    r"\bJWT\b",
    r"\bjwt\.(encode|decode)\b",
    r"\b(secret|signing)_key\b",
    r"\bsalt\s*=",
    r"\bmax_age\b",
    r"\bexpires?\b",
    r"\bexpiration\b",
    r"\bexp\s*[:=]",
    r"\bitsdangerous\b",
    r"\bserializer\.(dumps|loads)\b",
    r"\bsecrets\.(token_hex|token_urlsafe|token_bytes)\b",
    r"\b(password_reset|reset_password|email_verification)\b",
    r"\b(signature|signing|verify_signature)\b",
    r"\b(hmac|fernet)\b",
    r"\b(confirm|activation)_token\b",
]

SEARCH_RE = re.compile("|".join(PATTERNS), re.IGNORECASE)

# Masquer les valeurs potentiellement confidentielles.
SENSITIVE_RE = re.compile(
    r"""(?ix)
    (
      ["']?(?:secret_key|api_key|access_token|refresh_token|
      auth_token|password|passwd|client_secret|private_key|
      secret|brevo_api_key)["']?
      \s*[:=]\s*
    )
    (.+)
    """
)

def redact(line):
    line = line.rstrip()

    # Masquer la valeur complète d'une affectation sensible.
    match = SENSITIVE_RE.search(line)
    if match:
        line = (
            line[:match.start(2)]
            + "[VALEUR MASQUÉE]"
        )

    # Masquer les chaînes ressemblant à des JWT.
    line = re.sub(
        r"\beyJ[A-Za-z0-9_-]{10,}\."
        r"[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b",
        "[JWT MASQUÉ]",
        line
    )

    return line

def iter_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        relative = path.relative_to(ROOT)

        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue

        # Ne pas lire les fichiers contenant des secrets de déploiement.
        if path.name.lower() in {
            ".env", ".env.local", ".env.production",
            ".flaskenv", "credentials.json"
        }:
            continue

        if path.suffix.lower() in EXTENSIONS:
            yield path

def main():
    print("=" * 76)
    print("AUDIT DES TOKENS - GMES HAÏTI")
    print("Mode lecture seule : aucun fichier ni aucune donnée modifiés.")
    print("Les fichiers .env et credentials.json sont exclus.")
    print("=" * 76)

    total_files = 0
    total_matches = 0

    for path in sorted(iter_files()):
        try:
            lines = path.read_text(
                encoding="utf-8", errors="replace"
            ).splitlines()
        except OSError as exc:
            print(f"[LECTURE IMPOSSIBLE] {path.relative_to(ROOT)}: {exc}")
            continue

        matches = [
            (number, line)
            for number, line in enumerate(lines, start=1)
            if SEARCH_RE.search(line)
        ]

        if not matches:
            continue

        total_files += 1
        total_matches += len(matches)

        print(f"\n--- {path.relative_to(ROOT)} ---")

        for number, line in matches:
            print(f"{number:5}: {redact(line).strip()}")

    print("\n" + "=" * 76)
    print(f"Fichiers contenant des correspondances : {total_files}")
    print(f"Lignes correspondantes : {total_matches}")
    print("Fin de l'audit.")
    print("=" * 76)

if __name__ == "__main__":
    main()
