# ============================================================
# GMES - API MOBILE
# ============================================================

from flask import Blueprint, jsonify, request, current_app
from functools import wraps
from datetime import datetime, timedelta

import jwt
from sqlalchemy import or_

from models import (
    db,
    User,
    Client,
    Pret,
    Remboursement,
    Groupe, Notification
)


# ============================================================
# BLUEPRINT
# ============================================================

mobile_api_bp = Blueprint("mobile_api", __name__)


# ============================================================
# OUTILS AUTHENTIFICATION
# ============================================================

def generer_token_mobile(user):
    """Génère un JWT pour l'application mobile."""

    payload = {
        "user_id": user.id,
        "type": "mobile",
        "exp": datetime.utcnow() + timedelta(hours=24)
    }

    return jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )


def obtenir_client(user):
    """
    Retourne le Client correspondant au User.

    Priorité :
    1. User.client_id
    2. Client.user_id
    """

    # Relation User -> Client
    client_id = getattr(user, "client_id", None)

    if client_id:
        client = Client.query.get(client_id)

        if client:
            return client

    # Relation Client -> User
    return Client.query.filter_by(
        user_id=user.id
    ).first()


def token_required(f):
    """Vérifie le JWT envoyé par l'application mobile."""

    @wraps(f)
    def decorated(*args, **kwargs):

        authorization = request.headers.get("Authorization")

        if not authorization:
            return jsonify({
                "success": False,
                "error": "Token manquant"
            }), 401

        try:

            if authorization.startswith("Bearer "):
                token = authorization.split(" ", 1)[1]
            else:
                token = authorization

            data = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            if data.get("type") != "mobile":
                return jsonify({
                    "success": False,
                    "error": "Token mobile invalide"
                }), 401

            user_id = data.get("user_id")

            if not user_id:
                return jsonify({
                    "success": False,
                    "error": "Token invalide"
                }), 401

            user = User.query.get(user_id)

            if not user:
                return jsonify({
                    "success": False,
                    "error": "Utilisateur introuvable"
                }), 401

            if user.statut != "actif":
                return jsonify({
                    "success": False,
                    "error": "Compte inactif"
                }), 403

            return f(user, *args, **kwargs)

        except jwt.ExpiredSignatureError:

            return jsonify({
                "success": False,
                "error": "Token expiré"
            }), 401

        except jwt.InvalidTokenError:

            return jsonify({
                "success": False,
                "error": "Token invalide"
            }), 401

        except Exception:

            current_app.logger.exception(
                "Erreur authentification mobile"
            )

            return jsonify({
                "success": False,
                "error": "Erreur d'authentification"
            }), 401

    return decorated


# ============================================================
# TEST API MOBILE
# ============================================================

@mobile_api_bp.route("/api/mobile/test", methods=["GET"])
def mobile_test():

    return jsonify({
        "success": True,
        "message": "API mobile GMES opérationnelle",
        "timestamp": datetime.utcnow().isoformat()
    })


# ============================================================
# PROFIL UTILISATEUR CONNECTÉ
# ============================================================

@mobile_api_bp.route("/api/mobile/me", methods=["GET"])
@token_required
def mobile_me(current_user):

    client = obtenir_client(current_user)

    response = {
        "success": True,

        "user": {
            "id": current_user.id,
            "nom": current_user.nom,
            "prenom": current_user.prenom,
            "nom_complet": getattr(
                current_user,
                "nom_complet",
                None
            ),
            "email": current_user.email,
            "telephone": current_user.telephone,
            "username": current_user.username,
            "role": current_user.role,
            "fonction": current_user.fonction
        },

        "client": None
    }

    if client:

        response["client"] = {
            "id": client.id,
            "id_client": client.id_client,
            "numero_compte": client.numero_compte,
            "nom": client.nom,
            "prenom": client.prenom,
            "telephone": client.telephone,
            "email": client.email,
            "statut": client.statut,
            "compte_actif": client.compte_actif,
            "solde": client.solde or 0
        }

    return jsonify(response)


# ============================================================
# MES PRÊTS
# ============================================================

@mobile_api_bp.route("/api/mobile/prets", methods=["GET"])
@token_required
def mobile_prets(current_user):

    client = obtenir_client(current_user)

    if not client:
        return jsonify({
            "success": False,
            "error": "Profil client introuvable"
        }), 404

    prets = (
        Pret.query
        .filter_by(client_id=client.id)
        .order_by(Pret.date_demande.desc())
        .all()
    )

    resultats = []

    for pret in prets:

        montant_total = pret.montant_total or 0
        montant_rembourse = pret.montant_rembourse or 0

        # Utiliser le solde calculé s'il existe
        if pret.solde_restant_cache is not None:
            solde_restant = pret.solde_restant_cache
        else:
            solde_restant = montant_total - montant_rembourse

        solde_restant = max(0, solde_restant)

        montant_accorde = (
            pret.montant_accorde
            if pret.montant_accorde is not None
            else pret.montant or 0
        )

        resultats.append({

            "id": pret.id,

            "numero_pret": pret.numero_pret,

            "numero_dossier": pret.numero_dossier,

            "statut": pret.statut,

            "decision": pret.decision,

            "motif": pret.motif,

            "montant": pret.montant or 0,

            "montant_demande": (
                pret.montant_demande
                if pret.montant_demande is not None
                else pret.montant or 0
            ),

            "montant_accorde": montant_accorde,

            "taux_interet": pret.taux_interet or 0,

            "duree_mois": pret.duree_mois or 0,

            "mensualite": pret.mensualite or 0,

            "montant_interet": pret.montant_interet or 0,

            "montant_total": montant_total,

            "montant_rembourse": montant_rembourse,

            "solde_restant": solde_restant,

            "penalite": pret.penalite or 0,

            "type_pret": pret.type_pret,

            "date_demande": (
                pret.date_demande.isoformat()
                if pret.date_demande
                else None
            ),

            "date_approbation": (
                pret.date_approbation.isoformat()
                if pret.date_approbation
                else None
            ),

            "date_decaissement": (
                pret.date_decaissement.isoformat()
                if pret.date_decaissement
                else None
            ),

            "date_echeance": (
                pret.date_echeance.isoformat()
                if pret.date_echeance
                else None
            ),

            "prochaine_echeance": (
                pret.prochaine_echeance.isoformat()
                if pret.prochaine_echeance
                else None
            )
        })

    return jsonify({
        "success": True,
        "client_id": client.id,
        "prets": resultats,
        "total": len(resultats)
    }), 200


# ============================================================
# DEMANDE DE PRÊT
# ============================================================

@mobile_api_bp.route(
    "/api/demande-pret",
    methods=["POST"]
)
@token_required
def mobile_demande_pret(current_user):

    client = obtenir_client(current_user)

    if not client:

        return jsonify({
            "success": False,
            "error": "Profil client introuvable"
        }), 404

    # --------------------------------------------------------
    # Compte client
    # --------------------------------------------------------

    if not client.compte_actif:

        return jsonify({
            "success": False,
            "error": "Votre compte client est désactivé"
        }), 403

    # --------------------------------------------------------
    # Conditions du compte
    # --------------------------------------------------------

    if not client.terms_accepted:

        return jsonify({
            "success": False,
            "error": "Vous devez accepter les conditions du compte"
        }), 400

    data = request.get_json(silent=True) or {}

    montant = data.get("montant")

    duree = (
        data.get("duree_mois")
        or data.get("duree")
    )

    motif = data.get("motif", "").strip()

    if montant is None or duree is None:

        return jsonify({
            "success": False,
            "error": "Montant et durée obligatoires"
        }), 400

    try:
        montant = float(montant)
        duree = int(duree)

    except (ValueError, TypeError):

        return jsonify({
            "success": False,
            "error": "Montant ou durée invalide"
        }), 400

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if montant < 10000:

        return jsonify({
            "success": False,
            "error": "Le montant minimum est de 10 000 HTG"
        }), 400

    if montant > 10_000_000_000:

        return jsonify({
            "success": False,
            "error": "Le montant demandé est trop élevé"
        }), 400

    if duree < 3 or duree > 60:

        return jsonify({
            "success": False,
            "error": "La durée doit être comprise entre 3 et 60 mois"
        }), 400

    # --------------------------------------------------------
    # Vérification métier existante
    # --------------------------------------------------------

    if hasattr(client, "verifier_peut_demander_pret"):

        try:

            resultat = client.verifier_peut_demander_pret()

            if isinstance(resultat, tuple):

                autorise, message = resultat

                if not autorise:

                    return jsonify({
                        "success": False,
                        "error": message
                    }), 400

            elif resultat is False:

                return jsonify({
                    "success": False,
                    "error": "Le client ne peut pas demander un prêt"
                }), 400

        except TypeError:
            pass

    # --------------------------------------------------------
    # Vérifier les prêts déjà en cours
    # --------------------------------------------------------

    pret_existant = (
        Pret.query
        .filter(
            Pret.client_id == client.id,
            Pret.statut.in_([
                "en_attente",
                "actif",
                "approuve",
                "en_retard"
            ])
        )
        .first()
    )

    if pret_existant:

        return jsonify({
            "success": False,
            "error": "Vous avez déjà un prêt en cours ou en attente",
            "numero_pret": getattr(
                pret_existant,
                "numero_pret",
                None
            )
        }), 400

    # --------------------------------------------------------
    # Création du prêt
    # --------------------------------------------------------

    nouveau_pret = Pret(
        client_id=client.id,
        montant=montant,
        duree_mois=duree,
        motif=motif,
        statut="en_attente",
        date_demande=datetime.utcnow()
    )

    db.session.add(nouveau_pret)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Demande de prêt envoyée",
        "pret": {
            "id": nouveau_pret.id,
            "numero_pret": getattr(
                nouveau_pret,
                "numero_pret",
                None
            ),
            "montant": nouveau_pret.montant,
            "duree_mois": nouveau_pret.duree_mois,
            "statut": nouveau_pret.statut
        }
    }), 201


# ============================================================
# NOTIFICATIONS CLIENT
# ============================================================

@mobile_api_bp.route(
    "/api/mobile/notifications",
    methods=["GET"]
)
@token_required
def mobile_notifications(current_user):

    client = obtenir_client(current_user)

    if not client:
        return jsonify({
            "success": False,
            "error": "Profil client introuvable"
        }), 404

    notifications = (
        Notification.query
        .filter_by(client_id=client.id)
        .order_by(Notification.date_creation.desc())
        .all()
    )

    resultats = []

    for notification in notifications:

        resultats.append({
            "id": notification.id,

            "titre": notification.titre,

            "message": notification.message,

            "type": notification.type_notification
                or notification.type
                or notification.niveau
                or "info",

            "lue": bool(
                notification.lue
                or notification.is_read
            ),

            "requires_action": bool(
                notification.requires_action
            ),

            "pret_id": notification.pret_id,

            "client_id": notification.client_id,

            "lien": notification.lien or notification.url,

            "date_creation": (
                notification.date_creation.isoformat()
                if notification.date_creation
                else None
            )
        })

    non_lues = sum(
        1 for notification in notifications
        if not (
            notification.lue
            or notification.is_read
        )
    )

    return jsonify({
        "success": True,
        "notifications": resultats,
        "total": len(resultats),
        "non_lues": non_lues
    }), 200


# ============================================================
# MARQUER NOTIFICATION COMME LUE
# ============================================================

@mobile_api_bp.route(
    "/api/mobile/notifications/<int:notification_id>/lire",
    methods=["POST"]
)
@token_required
def mobile_notification_lire(
    current_user,
    notification_id
):

    client = obtenir_client(current_user)

    if not client:
        return jsonify({
            "success": False,
            "error": "Profil client introuvable"
        }), 404

    notification = Notification.query.filter_by(
        id=notification_id,
        client_id=client.id
    ).first()

    if not notification:
        return jsonify({
            "success": False,
            "error": "Notification introuvable"
        }), 404

    notification.lue = True
    notification.is_read = True
    notification.date_lecture = datetime.utcnow()
    notification.read_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Notification marquée comme lue"
    }), 200
