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
    Groupe, Notification,
    NotificationClient, Retrait,
    Transaction, Epargne, TransactionEpargne,
)
from routes.auth import get_compte_epargne_actif

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


@mobile_api_bp.route("/api/mobile/transfert", methods=["POST"])
def mobile_transfert():
    try:
        # ==============================
        # AUTHENTIFICATION JWT
        # ==============================
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify({
                "success": False,
                "error": "Token manquant."
            }), 401

        token = auth_header.split(" ", 1)[1]

        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return jsonify({
                "success": False,
                "error": "Session expirée."
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                "success": False,
                "error": "Token invalide."
            }), 401

        # ==============================
        # UTILISATEUR
        # ==============================
        user = User.query.get(payload.get("user_id"))

        if not user:
            return jsonify({
                "success": False,
                "error": "Utilisateur introuvable."
            }), 404

        client = None

        if getattr(user, "client_id", None):
            client = Client.query.filter_by(
                id=user.client_id
            ).first()

        if not client:
            client = Client.query.filter_by(
                user_id=user.id
            ).first()

        if not client:
            return jsonify({
                "success": False,
                "error": "Profil client introuvable."
            }), 404

        # ==============================
        # DONNÉES DU TRANSFERT
        # ==============================
        data = request.get_json(silent=True) or {}

        numero_compte_destinataire = str(
            data.get("numero_compte_destinataire", "")
        ).strip()

        montant = data.get("montant")
        motif = str(data.get("motif", "")).strip()

        if not numero_compte_destinataire:
            return jsonify({
                "success": False,
                "error": "Numéro de compte destinataire obligatoire."
            }), 400

        try:
            montant = float(montant)
        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "error": "Montant invalide."
            }), 400

        if montant <= 0:
            return jsonify({
                "success": False,
                "error": "Le montant doit être supérieur à zéro."
            }), 400

        # ==============================
        # COMPTE ÉPARGNE EXPÉDITEUR
        # ==============================
        compte_source = get_compte_epargne_actif(client)

        if not compte_source:
            return jsonify({
                "success": False,
                "error": "Compte épargne introuvable."
            }), 404

        solde_source = float(compte_source.solde or 0)

        if solde_source < montant:
            return jsonify({
                "success": False,
                "error": "Solde insuffisant."
            }), 400

        # ==============================
        # DESTINATAIRE
        # ==============================
        compte_destinataire = Epargne.query.filter_by(
            numero_compte=numero_compte_destinataire
        ).first()

        if not compte_destinataire:
            return jsonify({
                "success": False,
                "error": "Compte destinataire introuvable."
            }), 404

        if compte_destinataire.id == compte_source.id:
            return jsonify({
                "success": False,
                "error": "Vous ne pouvez pas transférer vers votre propre compte."
            }), 400

        # ==============================
        # TRANSACTION
        # ==============================
        compte_source.solde = solde_source - montant

        compte_destinataire.solde = (
            float(compte_destinataire.solde or 0)
            + montant
        )

        # ==============================
        # ENREGISTREMENT
        # ==============================
        # Adapte cette partie aux champs exacts
        # de ton modèle TransactionEpargne.

        transaction = TransactionEpargne(
            compte_epargne_id=compte_source.id,
            montant=-montant,
            type_transaction="transfert",
            description=(
                f"Transfert vers {numero_compte_destinataire}"
                + (f" - {motif}" if motif else "")
            )
        )

        db.session.add(transaction)

        transaction_recue = TransactionEpargne(
            compte_epargne_id=compte_destinataire.id,
            montant=montant,
            type_transaction="transfert",
            description=(
                f"Transfert reçu de {compte_source.numero_compte}"
                + (f" - {motif}" if motif else "")
            )
        )

        db.session.add(transaction_recue)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Transfert effectué avec succès.",
            "montant": montant,
            "solde": float(compte_source.solde or 0),
            "destinataire": numero_compte_destinataire
        }), 200

    except Exception as e:
        db.session.rollback()

        print("❌ ERREUR TRANSFERT :", str(e))

        return jsonify({
            "success": False,
            "error": "Erreur interne lors du transfert."
        }), 500

# ============================================================
# API MOBILE — DEMANDE DE PRÊT
# ============================================================

@mobile_api_bp.route(
    "/api/mobile/demande-pret",
    methods=["POST"]
)
def mobile_demande_pret(current_user):

    try:
        # ----------------------------------------------------
        # RÉCUPÉRER LE CLIENT CONNECTÉ
        # ----------------------------------------------------
        client = obtenir_client(current_user)

        if not client:
            return jsonify({
                "success": False,
                "error": "Profil client introuvable"
            }), 404

        # ----------------------------------------------------
        # DONNÉES JSON
        # ----------------------------------------------------
        data = request.get_json(silent=True) or {}

        print("==============================================")
        print("📱 DEMANDE DE PRÊT MOBILE")
        print("CLIENT :", client.id)
        print("DONNÉES :", data)
        print("==============================================")

        # ----------------------------------------------------
        # CHAMPS OBLIGATOIRES
        # ----------------------------------------------------
        montant = data.get("montant")
        duree = data.get("duree")
        objet = data.get("objet")
        type_pret = data.get("type_pret")

        if not montant:
            return jsonify({
                "success": False,
                "error": "Le montant du prêt est obligatoire."
            }), 400

        if not duree:
            return jsonify({
                "success": False,
                "error": "La durée du prêt est obligatoire."
            }), 400

        if not objet:
            return jsonify({
                "success": False,
                "error": "L'objet du prêt est obligatoire."
            }), 400

        if not type_pret:
            return jsonify({
                "success": False,
                "error": "Le type de prêt est obligatoire."
            }), 400

        # ----------------------------------------------------
        # CONVERSION
        # ----------------------------------------------------
        try:
            montant = float(montant)
            duree = int(duree)
        except (ValueError, TypeError):

            return jsonify({
                "success": False,
                "error": "Montant ou durée invalide."
            }), 400

        # ----------------------------------------------------
        # VALIDATION MONTANT
        # ----------------------------------------------------
        if montant < 10000 or montant > 10_000_000_000:

            return jsonify({
                "success": False,
                "error": (
                    "Le montant doit être compris entre "
                    "10 000 et 10 000 000 000 Gdes."
                )
            }), 400

        # ----------------------------------------------------
        # VALIDATION DURÉE
        # ----------------------------------------------------
        if duree < 3 or duree > 60:

            return jsonify({
                "success": False,
                "error": "La durée doit être comprise entre 3 et 60 mois."
            }), 400

        # ----------------------------------------------------
        # VÉRIFIER LES CONDITIONS DU CLIENT
        # ----------------------------------------------------
        if not client.terms_accepted:

            return jsonify({
                "success": False,
                "requires_terms": True,
                "error": (
                    "Vous devez d'abord accepter les conditions "
                    "générales de votre compte."
                )
            }), 403

        # ----------------------------------------------------
        # VÉRIFIER LES PRÊTS EXISTANTS
        # ----------------------------------------------------
        pret_existant = Pret.query.filter(
            Pret.client_id == client.id,
            Pret.statut.in_([
                "en_attente",
                "attente_signature",
                "approuve",
                "actif",
                "en_retard"
            ])
        ).first()

        if pret_existant:

            return jsonify({
                "success": False,
                "error": (
                    "Vous avez déjà une demande de prêt "
                    "en cours."
                ),
                "pret_id": pret_existant.id,
                "numero_pret": pret_existant.numero_pret,
                "statut": pret_existant.statut
            }), 409

        # ----------------------------------------------------
        # TAUX
        # ----------------------------------------------------
        taux_annuel = float(
            data.get("taux_interet", 12)
        )

        # ----------------------------------------------------
        # CALCUL INTÉRÊT
        # ----------------------------------------------------
        montant_interet = (
            montant
            * (taux_annuel / 100)
            * (duree / 12)
        )

        montant_total = montant + montant_interet

        mensualite = (
            montant_total / duree
            if duree > 0
            else montant_total
        )

        # ----------------------------------------------------
        # RATIO D'ENDETTEMENT
        # ----------------------------------------------------
        revenu_mensuel = client.revenu_mensuel or 0

        if revenu_mensuel > 0:

            ratio_endettement = (
                mensualite / float(revenu_mensuel)
            ) * 100

            if ratio_endettement > 35:

                return jsonify({
                    "success": False,
                    "error": (
                        f"Ratio d'endettement trop élevé "
                        f"({ratio_endettement:.1f}%)."
                    ),
                    "ratio_endettement": round(
                        ratio_endettement, 2
                    )
                }), 400

        # ----------------------------------------------------
        # NUMÉRO DE PRÊT
        # ----------------------------------------------------
        numero_pret_unique = generer_numero_pret()

        # ----------------------------------------------------
        # CRÉATION DU PRÊT
        # ----------------------------------------------------
        nouveau_pret = Pret(

            numero_pret=numero_pret_unique,

            client_id=client.id,

            agent_id=None,

            montant=montant,

            montant_demande=montant,

            montant_accorde=0,

            montant_rembourse=0,

            solde_restant=round(
                montant_total,
                2
            ),

            duree_mois=duree,

            motif=objet,

            type_pret=type_pret,

            autre_type_pret=data.get(
                "autre_type_pret"
            ) if type_pret == "autre" else None,

            succursale_id=client.succursale_id,

            mensualite=round(
                mensualite,
                2
            ),

            montant_interet=round(
                montant_interet,
                2
            ),

            montant_total=round(
                montant_total,
                2
            ),

            taux_interet=taux_annuel,

            statut="attente_signature",

            numero_dossier=data.get(
                "numero_dossier"
            )
        )

        db.session.add(nouveau_pret)

        db.session.flush()

        print(
            "✅ PRÊT MOBILE CRÉÉ :",
            nouveau_pret.id,
            nouveau_pret.numero_pret
        )

        # ----------------------------------------------------
        # COMMIT
        # ----------------------------------------------------
        db.session.commit()

        # ----------------------------------------------------
        # NOTIFICATION CLIENT
        # ----------------------------------------------------
        try:

            notifier_client(
                client_id=client.id,
                titre="Demande de prêt envoyée",
                message=(
                    "Votre demande de prêt a été enregistrée "
                    "et est en attente de signature."
                ),
                type="info",
                lien=None
            )

        except Exception as notification_error:

            print(
                "⚠️ Notification client non envoyée :",
                notification_error
            )

        # ----------------------------------------------------
        # NOTIFICATION DIRECTION
        # ----------------------------------------------------
        try:

            notifier_directeurs_demande_pret(
                nouveau_pret,
                type_action="attente_signature"
            )

        except Exception as notification_error:

            print(
                "⚠️ Notification direction non envoyée :",
                notification_error
            )

        # ----------------------------------------------------
        # RÉPONSE MOBILE
        # ----------------------------------------------------
        return jsonify({

            "success": True,

            "message": (
                "Votre demande de prêt a été enregistrée."
            ),

            "pret": {

                "id": nouveau_pret.id,

                "numero_pret":
                    nouveau_pret.numero_pret,

                "montant":
                    nouveau_pret.montant,

                "duree":
                    nouveau_pret.duree_mois,

                "taux":
                    nouveau_pret.taux_interet,

                "mensualite":
                    nouveau_pret.mensualite,

                "montant_interet":
                    nouveau_pret.montant_interet,

                "montant_total":
                    nouveau_pret.montant_total,

                "statut":
                    nouveau_pret.statut
            }

        }), 201

    except Exception as e:

        db.session.rollback()

        import traceback
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================================
# NOTIFICATIONS CLIENT
# ============================================================
# ============================================================
# À AJOUTER dans routes/auth.py
#
# Import à ajouter en haut du fichier :
#   from models import NotificationClient
#   from services.notifier_client import notifier_client
# ============================================================


# ============================================================
# API MOBILE — NOTIFICATIONS DU CLIENT (uniquement les siennes)
# ============================================================

@mobile_api_bp.route("/api/mobile/notifications", methods=["GET"])
@token_required
def mobile_notifications(current_user):

    try:
        client = obtenir_client(current_user)

        if not client:
            return jsonify({
                "success": False,
                "error": "Profil client introuvable"
            }), 404

        notifications = NotificationClient.query.filter_by(
            client_id=client.id
        ).order_by(
            NotificationClient.date_creation.desc()
        ).limit(100).all()

        resultats = []

        for n in notifications:
            resultats.append({
                "id": n.id,
                "titre": n.titre,
                "message": n.message,
                "type": n.type,
                "lien": n.lien,
                "lue": bool(n.lue),
                "date_creation": (
                    n.date_creation.isoformat()
                    if n.date_creation
                    else None
                )
            })

        non_lues = sum(
            1 for n in notifications
            if not n.lue
        )

        return jsonify({
            "success": True,
            "notifications": resultats,
            "non_lues": non_lues
        }), 200


    except Exception as e:

        import traceback

        print("❌ ERREUR MOBILE NOTIFICATIONS :", repr(e))

        traceback.print_exc()

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


@mobile_api_bp.route(
    "/api/mobile/notifications/<int:notification_id>/lire",
    methods=["POST"]
)
@token_required
def mobile_notification_lire(current_user, notification_id):

    try:
        client = obtenir_client(current_user)

        if not client:
            return jsonify({
                "success": False,
                "error": "Profil client introuvable"
            }), 404

        notif = NotificationClient.query.filter_by(
            id=notification_id,
            client_id=client.id
        ).first()

        if notif is None:
            return jsonify({
                "success": False,
                "error": "Notification introuvable."
            }), 404

        notif.lue = True
        db.session.commit()

        return jsonify({
            "success": True
        }), 200

    except Exception as e:
        db.session.rollback()

        print(
            "❌ Erreur mobile_notification_lire :",
            str(e)
        )

        return jsonify({
            "success": False,
            "error": "Erreur interne du serveur."
        }), 500

