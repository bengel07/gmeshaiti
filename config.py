
import os
from datetime import timedelta
import requests
from flask import current_app
from dotenv import load_dotenv


load_dotenv()

# ==================== CONSTANTES GLOBALES ====================
UPLOAD_FOLDER = 'static/uploads/profils'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 Mo


def allowed_file(filename):
    """Vérifie si l'extension du fichier est autorisée"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


print("DATABASE_URL =", os.environ.get("DATABASE_URL"))

# ==================== CONFIGURATION DE BASE ====================
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'f101f28e0e79a76b6f296fd0a213b623fc5551a3762d555397572b0eeaf748a0'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///gmes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = 'static/uploads/profils'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 Mo

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Configuration des langues
    LANGUAGES = ['fr', 'en', 'es', 'ht']
    BABEL_DEFAULT_LOCALE = 'fr'

    # Configuration des publicités
    ADS_CONFIG_FILE = '.ads_config.json'

    # Dans email_utils.py, remplacez :
    BREVO_API_KEY = os.environ.get('BREVO_API_KEY')
    FROM_EMAIL = os.environ.get('FROM_EMAIL', 'gmeshaiti@gmail.com')
    FROM_NAME = os.environ.get('FROM_NAME', 'GMES Microcrédit')

    # Taux d'intérêt par défaut
    DEFAULT_INTEREST_RATE = 12.0  # 12% annuel

    # Configuration du portail employé
    EMPLOYE_ROLES = ['manager', 'agent', 'cashier', 'advisor']

    SERVER_NAME = os.environ.get('SERVER_NAME')
    PREFERRED_URL_SCHEME = os.environ.get('PREFERRED_URL_SCHEME', 'http')

    @staticmethod
    def init_app(app):
        """Initialisation supplémentaire si nécessaire"""
        upload_path = os.path.join(app.root_path, Config.UPLOAD_FOLDER)
        os.makedirs(upload_path, exist_ok=True)


# ==================== ENVIRONNEMENTS ====================
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False



# ==================== FONCTION D'ENVOI D'EMAIL BREVO ====================
def send_email(recipient, subject, body_html=None, body_text=None):
    """
    Envoie un email via l'API Brevo.

    Args:
        recipient (str): Adresse email du destinataire.
        subject (str): Sujet de l'email.
        body_html (str): Corps HTML (optionnel).
        body_text (str): Corps texte (optionnel).

    Returns:
        bool: True si l'envoi a réussi, False sinon.
    """

    try:
        api_key = current_app.config.get("BREVO_API_KEY")
        sender_email = current_app.config.get("FROM_EMAIL")
        sender_name = current_app.config.get("FROM_NAME", "GMES Microcrédit")

        if not api_key:
            current_app.logger.error("BREVO_API_KEY manquante.")
            return False

        if not sender_email:
            current_app.logger.error("FROM_EMAIL manquant.")
            return False

        # Si aucun HTML n'est fourni, utiliser le texte
        if not body_html:
            body_html = f"<pre>{body_text or ''}</pre>"

        payload = {
            "sender": {
                "name": sender_name,
                "email": sender_email
            },
            "to": [
                {
                    "email": recipient
                }
            ],
            "subject": subject,
            "htmlContent": body_html
        }

        if body_text:
            payload["textContent"] = body_text

        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }

        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            json=payload,
            headers=headers,
            timeout=30
        )

        if response.status_code in (200, 201):
            current_app.logger.info(f"✅ Email envoyé à {recipient}")
            return True

        current_app.logger.error(
            f"❌ Erreur Brevo {response.status_code}: {response.text}"
        )
        return False

    except Exception as e:
        current_app.logger.exception(f"❌ Exception lors de l'envoi de l'email : {e}")
        return False


# ==================== DICTIONNAIRE DES CONFIGURATIONS ====================
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Pour la compatibilité avec votre code existant
MAX_FILE_SIZE = Config.MAX_CONTENT_LENGTH