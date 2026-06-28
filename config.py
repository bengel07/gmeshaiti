# import os
# from datetime import timedelta
#
# from dotenv import load_dotenv
#
# load_dotenv()
#
# # Constantes
# UPLOAD_FOLDER = 'static/uploads/profils'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 Mo
#
# def allowed_file(filename):
#     """Vérifie si l'extension du fichier est autorisée"""
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'f101f28e0e79a76b6f296fd0a213b623fc5551a3762d555397572b0eeaf748a0'
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///gmes.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#     UPLOAD_FOLDER = 'static/uploads/profils'  # ← Utilisé dans demande_pret
#
#     # ✅ AJOUTEZ CES LIGNES POUR L'URL DE BASE
#     SERVER_NAME = os.environ.get('SERVER_NAME')  # None en développement
#     PREFERRED_URL_SCHEME = os.environ.get('PREFERRED_URL_SCHEME', 'http')
#
#     # Configuration des uploads
#     UPLOAD_FOLDER = 'static/uploads/profils'
#     ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
#     MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 Mo
#
#     # Autres configurations
#     PERMANENT_SESSION_LIFETIME = timedelta(days=7)
#
#     # Configuration des langues
#     LANGUAGES = ['fr', 'en', 'es', 'ht']
#     BABEL_DEFAULT_LOCALE = 'fr'
#
#     # Configuration des publicités
#     ADS_CONFIG_FILE = '.ads_config.json'
#
#     # Configuration email
#     MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
#     MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = "gmeshaiti@gmail.com"
#     MAIL_PASSWORD = "kdez topb wmwm yucj"
#     MAIL_DEFAULT_SENDER = 'GMES Microcrédit <gmeshaiti@gmail.com>'
#
#     # Taux d'intérêt par défaut
#     DEFAULT_INTEREST_RATE = 12.0  # 12% annuel
#
#     # Configuration du portail employé
#     EMPLOYE_ROLES = ['manager', 'agent', 'cashier', 'advisor']
#
#     # config.py (à la fin du fichier)
#
#     def allowed_file(filename):
#         """Vérifie si l'extension du fichier est autorisée"""
#         return '.' in filename and \
#             filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
#
#
#     @staticmethod
#     def init_app(app):
#         """Initialisation supplémentaire si nécessaire"""
#         # Créer le dossier d'upload s'il n'existe pas
#         upload_path = os.path.join(app.root_path, Config.UPLOAD_FOLDER)
#         os.makedirs(upload_path, exist_ok=True)
#
#
# # Pour la compatibilité avec votre code existant
# UPLOAD_FOLDER = Config.UPLOAD_FOLDER
# # Variable globale pour la compatibilité (si vous l'utilisez directement)
# MAX_FILE_SIZE = Config.MAX_CONTENT_LENGTH
#
# # Vous pouvez aussi avoir plusieurs configurations
# class DevelopmentConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_ECHO = True
#
#
# class ProductionConfig(Config):
#     DEBUG = False
#     SQLALCHEMY_ECHO = False
#
#
# # Fonction utilitaire pour vérifier les fichiers
# def allowed_file(filename):
#     """Vérifie si le fichier a une extension autorisée"""
#     if not filename or '.' not in filename:
#         return False
#     extension = filename.rsplit('.', 1)[1].lower()
#     return extension in Config.ALLOWED_EXTENSIONS
#
#
# # Dictionnaire des configurations
# config = {
#     'development': DevelopmentConfig,
#     'production': ProductionConfig,
#     'default': DevelopmentConfig
# }
#
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from flask import current_app
#
#
# def send_email(recipient, subject, body_html=None, body_text=None):
#     """
#     Envoie un email avec support HTML et texte
#
#     Args:
#         recipient (str): Adresse email du destinataire
#         subject (str): Sujet de l'email
#         body_html (str): Corps HTML de l'email (optionnel)
#         body_text (str): Corps texte de l'email (optionnel)
#
#     Returns:
#         bool: True si l'envoi a réussi, False sinon
#     """
#     try:
#         # Configuration depuis les variables d'environnement
#         smtp_server = current_app.config.get('MAIL_SERVER', 'smtp.gmail.com')
#         smtp_port = current_app.config.get('MAIL_PORT', 587)
#         smtp_username = current_app.config.get('MAIL_USERNAME')
#         smtp_password = current_app.config.get('MAIL_PASSWORD')
#         sender = current_app.config.get('MAIL_DEFAULT_SENDER', smtp_username)
#
#         if not smtp_username or not smtp_password:
#             current_app.logger.error("Configuration email manquante")
#             return False
#
#         # Créer le message
#         msg = MIMEMultipart('alternative')
#         msg['Subject'] = subject
#         msg['From'] = sender
#         msg['To'] = recipient
#
#         # Ajouter la version texte si fournie
#         if body_text:
#             part_text = MIMEText(body_text, 'plain')
#             msg.attach(part_text)
#
#         # Ajouter la version HTML si fournie
#         if body_html:
#             part_html = MIMEText(body_html, 'html')
#             msg.attach(part_html)
#
#         # Envoyer l'email
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(smtp_username, smtp_password)
#             server.send_message(msg)
#
#         current_app.logger.info(f"Email envoyé à {recipient}")
#         return True
#
#     except Exception as e:
#         current_app.logger.error(f"Erreur envoi email à {recipient}: {e}")
#         return False


import os
from datetime import timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

    # Configuration email
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'gmeshaiti@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'kdez topb wmwm yucj')
    MAIL_DEFAULT_SENDER = 'GMES Microcrédit <gmeshaiti@gmail.com>'

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


# ==================== FONCTION D'ENVOI D'EMAIL ====================
def send_email(recipient, subject, body_html=None, body_text=None):
    """
    Envoie un email avec support HTML et texte

    Args:
        recipient (str): Adresse email du destinataire
        subject (str): Sujet de l'email
        body_html (str): Corps HTML de l'email (optionnel)
        body_text (str): Corps texte de l'email (optionnel)

    Returns:
        bool: True si l'envoi a réussi, False sinon
    """
    try:
        # Configuration depuis les variables d'environnement
        smtp_server = current_app.config.get('MAIL_SERVER', 'smtp.gmail.com')
        smtp_port = current_app.config.get('MAIL_PORT', 587)
        smtp_username = current_app.config.get('MAIL_USERNAME')
        smtp_password = current_app.config.get('MAIL_PASSWORD')
        sender = current_app.config.get('MAIL_DEFAULT_SENDER', smtp_username)

        if not smtp_username or not smtp_password:
            current_app.logger.error("Configuration email manquante")
            return False

        # Créer le message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient

        # Ajouter la version texte si fournie
        if body_text:
            part_text = MIMEText(body_text, 'plain')
            msg.attach(part_text)

        # Ajouter la version HTML si fournie
        if body_html:
            part_html = MIMEText(body_html, 'html')
            msg.attach(part_html)

        # Envoyer l'email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        current_app.logger.info(f"Email envoyé à {recipient}")
        return True

    except Exception as e:
        current_app.logger.error(f"Erreur envoi email à {recipient}: {e}")
        return False


# ==================== DICTIONNAIRE DES CONFIGURATIONS ====================
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Pour la compatibilité avec votre code existant
MAX_FILE_SIZE = Config.MAX_CONTENT_LENGTH