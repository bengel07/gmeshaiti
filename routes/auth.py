
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
    current_app
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from datetime import datetime, timedelta

import jwt

from models import User, Client, db



# ============================================================
# BLUEPRINT
# ============================================================

auth_bp = Blueprint("auth", __name__)


# ============================================================
# OUTILS
# ============================================================

def hash_password(password):
    return generate_password_hash(password)


def validate_password(password):

    if not password:
        return False, "Le mot de passe est obligatoire."

    if len(password) < 6:
        return False, (
            "Le mot de passe doit contenir "
            "au moins 6 caractères."
        )

    return True, "OK"


# ============================================================
# ROUTE WEB — INSCRIPTION
# ============================================================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    return """
    <h1>Inscription</h1>
    <p>Utilisez l'application GMES pour créer votre compte.</p>
    <a href="/connexion">Retour à la connexion</a>
    """


# ============================================================
# ROUTE WEB — DÉCONNEXION
# ============================================================

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()
    session.clear()

    return redirect(url_for("main.accueil"))


# ============================================================
# TOKEN MOBILE
# ============================================================

def generer_token_mobile(user):

    payload = {

        "user_id": user.id,

        "role": user.role,

        "type": "mobile",

        "exp": datetime.utcnow() + timedelta(days=30)
    }

    # Si le User est lié directement à un Client
    if getattr(user, "client_id", None):

        payload["client_id"] = user.client_id

    return jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )


# ============================================================
# API MOBILE — CONNEXION
# ============================================================

@auth_bp.route("/api/mobile/login", methods=["POST"])
def mobile_login():

    try:

        data = request.get_json(silent=True) or {}

        identifier = str(
            data.get("identifier") or ""
        ).strip()

        password = str(
            data.get("password") or ""
        )

        if not identifier or not password:

            return jsonify({

                "success": False,

                "error":
                    "Veuillez remplir tous les champs."

            }), 400

        user = None
        client = None

        # ====================================================
        # 1. RECHERCHE USER PAR EMAIL OU USERNAME
        # ====================================================

        user = User.query.filter(
            db.or_(
                User.username == identifier,
                User.email == identifier
            )
        ).first()

        # ====================================================
        # 2. SI PAS USER → RECHERCHE NUMÉRO DE COMPTE
        # ====================================================

        if user is None:

            client = Client.query.filter(
                Client.numero_compte == identifier
            ).first()

            if client:

                # Relation Client → User
                if client.user_id:

                    user = User.query.filter_by(
                        id=client.user_id
                    ).first()

                # Relation User → Client
                if user is None:

                    user = User.query.filter_by(
                        client_id=client.id
                    ).first()

        # ====================================================
        # 3. USER INTROUVABLE
        # ====================================================

        if user is None:

            return jsonify({

                "success": False,

                "error":
                    "Identifiants incorrects."

            }), 401

        # ====================================================
        # 4. RÉCUPÉRER LE CLIENT
        # ====================================================

        if getattr(user, "client_id", None):

            client = Client.query.filter_by(
                id=user.client_id
            ).first()

        if client is None:

            client = Client.query.filter_by(
                user_id=user.id
            ).first()

        # ====================================================
        # 5. VÉRIFICATION STATUT USER
        # ====================================================

        if user.statut != "actif":

            if user.statut == "en_attente":

                message = (
                    "Compte en attente d'approbation."
                )

            elif user.statut == "rejete":

                message = (
                    "Compte rejeté par l'administration."
                )

            else:

                message = (
                    f"Compte désactivé "
                    f"(statut : {user.statut})."
                )

            return jsonify({

                "success": False,

                "error": message,

                "statut": user.statut

            }), 403

        # ====================================================
        # 6. VÉRIFICATION STATUT CLIENT
        # ====================================================

        if client:

            if client.statut not in [
                "actif",
                "suspendu"
            ]:

                return jsonify({

                    "success": False,

                    "error":
                        "Votre compte client "
                        "n'est pas actif.",

                    "statut": client.statut

                }), 403

        # ====================================================
        # 7. VÉRIFICATION MOT DE PASSE
        # ====================================================

        password_correct = False

        # Mot de passe User
        if user.password_hash:

            try:

                password_correct = check_password_hash(
                    user.password_hash,
                    password
                )

            except Exception:

                password_correct = False

        # Mot de passe Client
        if (
            not password_correct
            and client
            and client.mot_de_passe_hash
        ):

            try:

                password_correct = check_password_hash(
                    client.mot_de_passe_hash,
                    password
                )

            except Exception:

                password_correct = False

        if not password_correct:

            return jsonify({

                "success": False,

                "error":
                    "Identifiants incorrects."

            }), 401

        # ====================================================
        # 8. DERNIÈRE CONNEXION
        # ====================================================

        user.derniere_connexion = datetime.utcnow()

        db.session.commit()

        # ====================================================
        # 9. TOKEN
        # ====================================================

        token = generer_token_mobile(user)

        # ====================================================
        # 10. INFORMATIONS CLIENT
        # ====================================================

        client_data = None

        if client:

            client_data = {

                "id": client.id,

                "id_client":
                    client.id_client,

                "numero_compte":
                    client.numero_compte,

                "nom":
                    client.nom,

                "prenom":
                    client.prenom,

                "nom_complet":
                    client.nom_complet,

                "email":
                    client.email,

                "telephone":
                    client.telephone,

                "solde":
                    client.solde or 0,

                "statut":
                    client.statut,

                "compte_actif":
                    client.compte_actif,

                "terms_accepted":
                    client.terms_accepted,

                "email_confirme":
                    client.email_confirme,

                "a_un_pret_actif":
                    client.a_un_pret_actif,

                "compte_suspendu":
                    client.compte_suspendu,

                "succursale_id":
                    client.succursale_id
            }

        # ====================================================
        # 11. RÉPONSE
        # ====================================================

        return jsonify({

            "success": True,

            "message":
                "Connexion réussie.",

            "token": token,

            "user": {

                "id":
                    user.id,

                "username":
                    user.username,

                "email":
                    user.email,

                "first_name":
                    user.prenom,

                "last_name":
                    user.nom,

                "role":
                    user.role,

                "fonction":
                    user.fonction,

                "statut":
                    user.statut,

                "premier_connexion":
                    user.premier_connexion,

                "succursale_id":
                    user.succursale_id,

                "client_id":
                    user.client_id
            },

            "client": client_data

        }), 200

    except Exception as e:

        db.session.rollback()

        print(
            "❌ Erreur API mobile login :",
            str(e)
        )

        return jsonify({

            "success": False,

            "error":
                "Erreur interne du serveur."

        }), 500


# ============================================================
# API MOBILE — DÉCONNEXION
# ============================================================

@auth_bp.route(
    "/api/mobile/logout",
    methods=["POST"]
)
def mobile_logout():

    return jsonify({

        "success": True,

        "message":
            "Déconnexion réussie."

    }), 200


# ============================================================
# API MOBILE — INSCRIPTION
# ============================================================

@auth_bp.route(
    "/api/mobile/register",
    methods=["POST"]
)
def mobile_register():

    try:

        data = request.get_json(
            silent=True
        ) or {}

        first_name = str(
            data.get("first_name") or ""
        ).strip()

        last_name = str(
            data.get("last_name") or ""
        ).strip()

        phone = str(
            data.get("phone") or ""
        ).strip()

        email = str(
            data.get("email") or ""
        ).strip().lower()

        password = str(
            data.get("password") or ""
        )

        # ====================================================
        # VALIDATION
        # ====================================================

        if not all([
            first_name,
            last_name,
            phone,
            email,
            password
        ]):

            return jsonify({

                "success": False,

                "error":
                    "Tous les champs sont obligatoires."

            }), 400

        valid, message = validate_password(
            password
        )

        if not valid:

            return jsonify({

                "success": False,

                "error": message

            }), 400

        # ====================================================
        # EMAIL EXISTANT
        # ====================================================

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            return jsonify({

                "success": False,

                "error":
                    "Cette adresse email est déjà utilisée."

            }), 409

        # ====================================================
        # TÉLÉPHONE EXISTANT
        # ====================================================

        existing_phone = User.query.filter_by(
            telephone=phone
        ).first()

        if existing_phone:

            return jsonify({

                "success": False,

                "error":
                    "Ce numéro de téléphone est déjà utilisé."

            }), 409

        # ====================================================
        # CRÉATION DU USER
        # ====================================================

        new_user = User(

            email=email,

            prenom=first_name,

            nom=last_name,

            nom_complet=
                f"{first_name} {last_name}",

            telephone=phone,

            role="client",

            statut="actif",

            premier_connexion=False
        )

        new_user.set_password(
            password
        )

        db.session.add(new_user)

        db.session.flush()

        # ====================================================
        # SUCCURSALE
        # ====================================================

        # Une inscription mobile ne crée PAS
        # automatiquement un Client complet ici.
        #
        # Le compte User est créé d'abord.
        # Le processus GMES pourra ensuite créer
        # le dossier Client avec toutes les informations
        # réglementaires nécessaires.

        db.session.commit()

        return jsonify({

            "success": True,

            "message":
                "Compte créé avec succès.",

            "user": {

                "id":
                    new_user.id,

                "email":
                    new_user.email,

                "first_name":
                    new_user.prenom,

                "last_name":
                    new_user.nom,

                "role":
                    new_user.role,

                "statut":
                    new_user.statut
            }

        }), 201

    except Exception as e:

        db.session.rollback()

        print(
            "❌ Erreur inscription mobile :",
            str(e)
        )

        return jsonify({

            "success": False,

            "error":
                "Erreur lors de la création du compte."

        }), 500


# ============================================================
# API MOBILE — TEST
# ============================================================

@auth_bp.route(
    "/api/mobile/test",
    methods=["GET"]
)
def mobile_test():

    return jsonify({

        "success": True,

        "status": "OK",

        "message":
            "API mobile GMES fonctionnelle.",

        "timestamp":
            datetime.utcnow().isoformat()

    }), 200

