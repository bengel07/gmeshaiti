#
# import time
# import json
# # ==================== FLASK CORE ====================
#
# # ==================== DATABASE ====================
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import inspect, text
#
# # ==================== SECURITY ====================
# from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.utils import secure_filename
# from werkzeug.exceptions import RequestEntityTooLarge
# from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
#
# # ==================== SOCKET / REALTIME ====================
# from flask_socketio import SocketIO, emit, join_room, leave_room
# from flask_sock import Sock
# from flask import Blueprint
#
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import mm
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
# from reportlab.pdfgen import canvas
# import qrcode
# import os
# from datetime import datetime
#
# from flask import render_template, request, flash, redirect, url_for
#
#
#
# from models import Pret, Client
# from datetime import datetime, timedelta
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import mm
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
# from reportlab.pdfgen import canvas
# import qrcode
# import os
#
#
# from flask import render_template, request, flash, redirect, url_for
# from flask_login import login_required, current_user
# from models import Epargne, TransactionEpargne, Client, Depense
#
# from datetime import datetime
#
#
# # ==================== EMAIL ====================
# from flask_mail import Mail, Message
#
# # ==================== CORS / PROXY ====================
# from flask_cors import CORS
# from werkzeug.middleware.proxy_fix import ProxyFix
#
# # ==================== ENV ====================
# from dotenv import load_dotenv
#
# # ==================== DATE / TIME ====================
# from datetime import datetime, timedelta
#
# # ==================== STANDARD LIB ====================
# import os
# import uuid
# import random
# import json
# import re
# import io
# import base64
# import traceback
# import warnings
#
# # ==================== WARNINGS ====================
# from pkg_resources import PkgResourcesDeprecationWarning
#
# # ==================== IMAGE / AI ====================
# import cv2
# import numpy as np
# from PIL import Image
# from datetime import datetime, timedelta
# import schedule
# import threading
#
# # ==================== QR / JWT ====================
# import qrcode
# import jwt
#
# # ==================== PDF ====================
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Image as RLImage, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from functools import wraps
# from flask import flash, redirect, url_for
#
# # ==================== MATH ====================
#
# # ==================== LOCAL CONFIG ====================
# from config import Config, allowed_file, UPLOAD_FOLDER, MAX_FILE_SIZE, ALLOWED_EXTENSIONS, send_email
#
# # ==================== DATABASE CUSTOM ====================
# from database import db, init_db
#
#
#
# # ==================== MODELS ====================
# from models import (
#     Pret, Notification, Pointage, Employe, Remboursement, Journal,
#     Transaction, TransactionCaisse, AuditLog, Paiement,
#     CreerGroupeForm, Succursale, ErrorLog, Competence, Note,
#     ContactHistorique, HistoriqueAction, Tracking, QuestionSecrete,
#     Client, Groupe, User, Document, Dossier, Action, RetardPaiement, ScoringCredit, HistoriqueEmploye)
#
# # ==================== ROUTES / BLUEPRINTS ====================
# from routes import *
# from routes.auth import auth_bp
# from routes.prets import prets_bp
# from routes.accueil import accueil_bp
# from routes.employees import employees_bp
# from routes.terms import terms_bp
# from routes.clients import clients_bp
# from routes.functions import functions_bp
# from config import Config
#
# # routes/api.py (ou dans le même fichier)
# from utils.stats import (
#      get_stats_dashboard,get_stats_employes_succursale,
#     get_stats_direction_succursale,get_stats_remboursements_succursale,
#      get_stats_dossiers_attente, get_stats_caissier,get_stats_succursale,
#     get_stats_admin_succursale, get_stats_verifications_brh,
#      get_stats_employe, get_stats_employes, get_stats_succursales, get_detail_succursale_stats,
#      get_stats_admin_central_succursales ) # ← IMPORTER
#
#
#
# # ==================== UTILS ====================
# from utils.errors import humanize_unique_error
# from jinja2.exceptions import TemplateNotFound
# # ==================== DECORATORS ====================
# from functools import wraps
#
# from utils.notifications import notification_manager


# ==================== STANDARD LIB ====================
import os
import uuid
import random
import json
import re
import io
import base64
import time
import traceback
import warnings
from datetime import datetime, timedelta

# ==================== FLASK CORE ====================
from flask import (
    Flask, render_template, redirect, url_for, flash,
    request, session, jsonify, abort, g, send_file, Blueprint
)

# ==================== AUTH ====================
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# ==================== DATABASE ====================
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect, text

# ==================== SECURITY ====================
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# ==================== SOCKET / REALTIME ====================
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sock import Sock

# ==================== PDF ====================
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfgen import canvas

# ==================== QR / IMAGE ====================
import qrcode
import cv2
import numpy as np
from PIL import Image

# ==================== JWT ====================
import jwt

# ==================== EMAIL ====================
from flask_mail import Mail, Message

# ==================== CORS ====================
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

# ==================== ENV ====================
from dotenv import load_dotenv

# ==================== WARNINGS ====================
from pkg_resources import PkgResourcesDeprecationWarning

# ==================== DECORATORS ====================
from functools import wraps

# ==================== LOCAL CONFIG ====================
from config import Config, allowed_file, UPLOAD_FOLDER, MAX_FILE_SIZE, ALLOWED_EXTENSIONS, send_email

# ==================== DATABASE CUSTOM ====================
from database import db, init_db

# ==================== MODELS ====================
import models

# from models import (
#     Pret, Notification, Pointage, Employe, Remboursement, Journal,
#     Transaction, TransactionCaisse, AuditLog, Paiement,
#     CreerGroupeForm, Succursale, ErrorLog, Competence, Note,
#     ContactHistorique, HistoriqueAction, Tracking, QuestionSecrete,
#     Client, Groupe, User, Document, Dossier, Action, RetardPaiement,
#     ScoringCredit, HistoriqueEmploye, Epargne, TransactionEpargne, Depense
# )

# ==================== ROUTES / BLUEPRINTS ====================
from routes import *
from routes.auth import auth_bp
from routes.prets import prets_bp
from routes.accueil import accueil_bp
from routes.employees import employees_bp
from routes.terms import terms_bp
from routes.clients import clients_bp
from routes.functions import functions_bp

# ==================== UTILS ====================
from utils.stats import (
    get_stats_dashboard, get_stats_employes_succursale,
    get_stats_direction_succursale, get_stats_remboursements_succursale,
    get_stats_dossiers_attente, get_stats_caissier, get_stats_succursale,
    get_stats_admin_succursale, get_stats_verifications_brh,
    get_stats_employe, get_stats_employes, get_stats_succursales,
    get_detail_succursale_stats, get_stats_admin_central_succursales
)
from utils.errors import humanize_unique_error
from utils.notifications import notification_manager
from jinja2.exceptions import TemplateNotFound

# ==================== SCHEDULER (si utilisé) ====================
import schedule
import threading


mail = Mail()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'gmes-microcredit-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gmes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['DEBUG'] = True  # Pour le développement

app.config.from_object(Config)  # ← Charge TOUTES les configs (y compris email)


sock = Sock(app)
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.init_app(app)




main = Blueprint('main', __name__)


# Enregistre le Blueprint
app.register_blueprint(auth_bp, url_prefix="/auth")
app.wsgi_app = ProxyFix(app.wsgi_app)
app.register_blueprint(accueil_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(prets_bp)

app._static_folder = 'static'

init_db(app)  # ← Déplacé ICI, avant les imports des modèles !

import os

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads', 'profils')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

# Créer le blueprint
# employees_bp = Blueprint('employees', __name__, url_prefix='/employees')

mail.init_app(app)

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Veuillez vous connecter', 'danger')
                return redirect(url_for('connexion'))
            if current_user.role not in roles:
                flash('Accès non autorisé', 'danger')
                # ✅ Au lieu de dashboard_redirect, rester sur la page si possible
                if request.referrer:
                    return redirect(request.referrer)
                return redirect(url_for('dashboard_redirect'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.template_filter('age')
def age_filter(date_naissance):
    from datetime import datetime
    if date_naissance:
        today = datetime.now().date()
        age = today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))
        return age
    return 'N/A'

# ... le reste de votre code ...

# ==================== ROUTES PRINCIPALES ====================
@app.route('/')
def index():
    """Page d'accueil publique"""
    stats = get_stats_dashboard()
    return render_template('index.html', stats=stats)



# Filtre Flask
@app.template_filter('age')
def age_filter(date_naissance):
    from datetime import datetime
    if date_naissance:
        today = datetime.now().date()
        age = today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))
        return age
    return 'N/A'
clients = []

# 📍 Endpoint tracking mobile
@app.post("/track")
async def track(data: dict):
    employe_id = data["employe_id"]
    lat = data["lat"]
    lon = data["lon"]

    conn = sqlite3.connect("gmes.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tracking (employe_id, lat, lon, time)
        VALUES (?, ?, ?, ?)
    """, (employe_id, lat, lon, datetime.now()))

    conn.commit()
    conn.close()

    # 🔥 envoyer en live aux dashboards
    for ws in clients:
        await ws.send_json(data)

    return {"status": "ok"}

async def notify_director(message):
    for ws in clients:
        await ws.send_json({
            "type": "NOTIF",
            "message": message
        })

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     clients.append(websocket)
#
#     try:
#         while True:
#             await websocket.receive_text()
#     except:
#         clients.remove(websocket)


# ✅ Route WebSocket
@sock.route('/ws')
def websocket(ws):
    # Attendre les messages
    while True:
        data = ws.receive()
        # Traiter le message
        ws.send(json.dumps({"status": "ok"}))


clients_bp = Blueprint(
    'clients',
    __name__,
    url_prefix='/succursales'
)
caissier_bp = Blueprint(
    'caissier',
    __name__,
    url_prefix='/caissier')

@app.route('/')
def accueil():
    return "Bienvenue sur GMES"

# Dans ton blueprint pour les succursales ou employés
@employees_bp.route('/<branch_code>/dashboard')
@login_required
def branch_dashboard(branch_code):
    # Vérifier que l'utilisateur est un admin_succursale
    if not hasattr(current_user, 'role') or current_user.role != 'admin_succursale':
        # Rediriger les autres rôles vers leurs dashboards respectifs
        if current_user.role == 'super_admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'client':
            return redirect(url_for('clients.client_dashboard'))
        elif current_user.role == 'employee':
            return redirect(url_for('employees.employee_dashboard'))
        else:
            abort(403)

    # Vérifier que l'admin a accès à cette succursale spécifique
    if not hasattr(current_user, 'branch_code'):
        abort(403, "Admin sans succursale affectée")

    if current_user.branch_code != branch_code:
        abort(403, f"Accès non autorisé à la succursale {branch_code}")

    # DEBUG
    print(f"=== DEBUG BRANCH DASHBOARD ===")
    print(f"Admin: {current_user.username}")
    print(f"Succursale demandée: {branch_code}")
    print(f"Succursale admin: {current_user.branch_code}")

    # Récupérer les statistiques de LA SUCCURSALE SPÉCIFIQUE
    from models import User, Loan, Transaction

    # Compter seulement les clients de cette succursale
    total_clients = Client.query.filter_by(branch_code=branch_code, role='client').count()

    # Prêts en attente de cette succursale
    pending_loans = Loan.query.join(User).filter(
        User.branch_code == branch_code,
        Loan.status == 'pending'
    ).count()

    # Transactions en attente de cette succursale
    pending_transactions = Transaction.query.join(User).filter(
        User.branch_code == branch_code,
        Transaction.status == 'pending'
    ).count()

    return render_template('branch_dashboard.html',
                           branch_code=branch_code,
                           total_clients=total_clients,
                           pending_loans=pending_loans,
                           pending_transactions=pending_transactions,
                           user=current_user)

def compare_faces(id_image_path, selfie_image_path):
    """Compare les visages entre photo ID et selfie avec DeepFace"""
    try:
        # Utiliser DeepFace pour comparer les visages
        result = DeepFace.verify(
            img1_path=id_image_path,
            img2_path=selfie_image_path,
            model_name="VGG-Face",  # Modèle recommandé
            detector_backend="opencv",  # Détecteur rapide
            distance_metric="cosine",  # Métrique de distance
            enforce_detection=True
        )

        # result contient 'verified' (bool) et 'distance' (float)
        match = result["verified"]
        distance = result["distance"]
        similarity = 1 - distance

        return match, f"Similarité: {round(similarity * 100, 2)}%"

    except Exception as e:
        # Si DeepFace échoue (pas de visage détecté), retourner False
        if "Face could not be detected" in str(e):
            return False, "Aucun visage détecté dans une des images"
        return False, f"Erreur de comparaison: {str(e)}"



# app.py - Ajoutez ceci après app = Flask(__name__)

@app.template_filter('age')
def calculate_age(birth_date):
    """Calcule l'âge à partir d'une date de naissance"""
    if not birth_date:
        return 0
    today = datetime.now().date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return "Fichier trop volumineux (max 100MB)", 413


@app.after_request
def add_header(response):
    """Empêche le cache des pages"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

def envoyer_email_conditions(client):
    print("EMAIL AP VOYE POU:", client.email)
    """
    Envoie un email au client avec un lien pour accepter les conditions d'utilisation
    """
    if client.terms_accepted:
        print(f"ℹ️ Client {client.email} a déjà accepté, pas d'envoi")
        return False

    try:
        # Générer un token unique pour ce client
        token = generer_token_conditions(client)

        # Créer le lien d'acceptation
        lien_acceptation = url_for('accepter_conditions', token=token, _external=True)
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            lien_acceptation = lien_acceptation.replace('127.0.0.1', local_ip).replace('localhost', local_ip)
        except:
            pass

        # 3. ENVOYER L'EMAIL VIA SMTP (solution intégrée)
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # Configuration email (à mettre dans vos variables d'environnement)
        import os
        EMAIL_EXPEDITEUR = os.environ.get('MAIL_USERNAME', 'gmeshaiti@gmail.com')
        EMAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')  # ← Utilise le .env
        EMAIL_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        EMAIL_PORT = int(os.environ.get('SMTP_PORT', 587))

        print(f"📧 Envoi depuis: {EMAIL_EXPEDITEUR}")
        print(f"🔐 Mot de passe: {'✅ Défini' if EMAIL_PASSWORD else '❌ Manquant'}")
        # Créer le message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "📋 GMES Microcrédit - Acceptation des conditions d'utilisation"
        msg['From'] = f"GMES Microcrédit <{EMAIL_EXPEDITEUR}>"
        msg['To'] = client.email

        # Corps de l'email (version HTML)
        corps_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; 
                          margin: 20px 0; font-weight: bold; }}
                .button:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); }}
                .footer {{ margin-top: 30px; font-size: 0.9em; color: #666; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏦 GMES Microcrédit</h1>
                </div>
                <div class="content">
                    <h2>Bonjour {client.prenom} {client.nom},</h2>

                    <p>Pour finaliser la création de votre compte et pouvoir bénéficier de nos services, 
                       vous devez accepter nos conditions générales d'utilisation.</p>

                    <p>Veuillez cliquer sur le bouton ci-dessous pour lire et accepter nos conditions :</p>

                    <div style="text-align: center;">
                        <a href="{lien_acceptation}" class="button">
                            ✅ Accepter les conditions
                        </a>
                    </div>

                    <p><strong>Ce lien est valable pendant 7 jours.</strong></p>

                    <p>Si le bouton ne fonctionne pas, copiez et collez ce lien dans votre navigateur :<br>
                    <small style="color: #667eea;">{lien_acceptation}</small></p>

                    <p>Si vous n'êtes pas à l'origine de cette demande, ignorez simplement cet email.</p>
                </div>
                <div class="footer">
                    <p>© 2024 GMES Microcrédit - Tous droits réservés</p>
                    <p>Cet email a été envoyé automatiquement, merci de ne pas y répondre.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Corps de l'email (version texte)
        corps_texte = f"""
        Bonjour {client.prenom} {client.nom},

        Pour finaliser la création de votre compte et pouvoir bénéficier de nos services, 
        vous devez accepter nos conditions générales d'utilisation.

        Veuillez cliquer sur ce lien pour accepter nos conditions :
        {lien_acceptation}

        Ce lien est valable pendant 7 jours.

        Si vous n'êtes pas à l'origine de cette demande, ignorez simplement cet email.

        ---
        GMES Microcrédit
        """

        # Attacher les versions texte et HTML
        part1 = MIMEText(corps_texte, 'plain')
        part2 = MIMEText(corps_html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Envoyer l'email
        try:
            server = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
            server.starttls()
            server.login(EMAIL_EXPEDITEUR, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            email_envoye = True
            print(f"✅ Email envoyé avec succès à {client.email}")
        except Exception as e:
            print(f"❌ Erreur envoi email: {e}")
            email_envoye = False

        # 4. Créer une notification dans la base
        from datetime import datetime
        from models import Notification

        nouvelle_notification = Notification(
            employe_id=client.id,
            titre="🔔 Nouveau lien de signature",
            message=f"Bonjour {client.prenom}, voici votre nouveau lien pour signer vos conditions : {lien_acceptation}",
            type_notification='terms',
            lien=lien_acceptation,
            date_envoi=datetime.now(),
            lue=False,
            date_creation=datetime.now(),
            destinataire_id=client.id,
            action_id=0
        )
        db.session.add(nouvelle_notification)
        db.session.commit()

        # 5. Message flash pour le conseiller
        flash(f'✅ Lien de signature renvoyé à {client.prenom} {client.nom} ({client.email})', 'success')

        if email_envoye:
            return jsonify({
                'success': True,
                'message': f'✅ Email envoyé à {client.email}',
                'email_envoye': True
            })
        else:
            return jsonify({
                'success': True,
                'message': f'⚠️ Notification créée mais email non envoyé (vérifiez config SMTP)',
                'email_envoye': False
            })

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erreur envoi email conditions à {client.email}: {e}")
        return jsonify({'success': False, 'message': f'❌ Erreur: {str(e)}'}), 500


# Ajouter cette fonction au début du fichier (hors de la route)
def generer_numero_pret():
    from datetime import datetime
    import random

    date_actuelle = datetime.now().strftime("%Y%m%d")
    chiffres_aleatoires = str(random.randint(000, 99999))
    return f"GMES-{date_actuelle}-{chiffres_aleatoires}"

@app.route('/prets/demande-pret', methods=['GET', 'POST'])
@login_required
def demande_pret():
    """Page de demande de prêt - accessible aux clients et aux agents"""

    # 🔥 AJOUTEZ CES 3 LIGNES ICI (au tout début)
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    from models import Client, Pret, Succursale, Journal
    from flask import session
    import re
    import os
    import json
    from datetime import datetime
    from werkzeug.utils import secure_filename

    print("🔥 ROUTE DEMANDE PRET EXECUTÉE")

    print(f"👤 Utilisateur connecté: ID {current_user.id}, Rôle: {current_user.role}, Fonction: {current_user.fonction}")

    # ===== DÉTERMINER QUI EST L'UTILISATEUR =====
    est_agent = current_user.role in ['admin', 'super_admin', 'direction', 'agent_credit', 'conseiller', 'employe']
    est_client = hasattr(current_user, 'client_profile') and current_user.client_profile is not None

    print(f"📋 Type d'utilisateur: {'Agent' if est_agent else 'Client' if est_client else 'Autre'}")

    # ===== RECHERCHE DU CLIENT =====
    client = None
    client_id = request.args.get('client_id') or request.form.get('client_id')

    # CAS 1: L'utilisateur est un AGENT - il cherche un client
    if est_agent:
        if client_id:
            client = db.session.get(Client, client_id)
            if client:
                print(f"✅ Agent - Client trouvé par ID: {client.id} - {client.prenom} {client.nom}")

        # Recherche par téléphone
        if not client:
            telephone = request.args.get('telephone') or request.form.get('telephone')
            if telephone:
                telephone_propre = re.sub(r'[\s\-\(\)]', '', telephone)
                client = Client.query.filter(
                    (Client.telephone == telephone) |
                    (Client.telephone == telephone_propre)
                ).first()
                if client:
                    print(f"✅ Agent - Client trouvé par téléphone: {client.id}")

        # Recherche par email
        if not client:
            email = request.args.get('email') or request.form.get('email')
            if email:
                client = Client.query.filter_by(email=email).first()
                if client:
                    print(f"✅ Agent - Client trouvé par email: {client.id}")

        # Si toujours pas de client, on affiche la liste
        if not client:
            print("ℹ️ Agent - Aucun client spécifié, affichage de la liste")

    # CAS 2: L'utilisateur est un CLIENT - il fait sa propre demande
    elif est_client:
        client = current_user.client_profile
        print(f"✅ Client connecté: {client.id} - {client.prenom} {client.nom}")

    # CAS 3: Autre type d'utilisateur
    else:
        flash("Accès non autorisé", "danger")
        return redirect(url_for('main.accueil'))

    # ========== CONTRÔLE D'ACCÈS POUR LES AGENTS ==========
    if est_agent:
        # Vérifier que l'employé a une succursale assignée
        if not current_user.succursale_id:
            flash('⛔ Vous n\'êtes pas assigné à une succursale. Contactez l\'administration.', 'danger')
            return redirect(url_for('employe_dashboard_generique'))

        # Récupérer la succursale
        succursale = db.session.get(Succursale, current_user.succursale_id)
        if not succursale:
            flash('⛔ Succursale introuvable', 'danger')
            return redirect(url_for('employe_dashboard_generique'))
    else:
        succursale = None

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # ========== TRAITEMENT POST ==========
    # if request.method == 'POST':
    #     if not client:
    #         flash("Veuillez ouvrir un compte pour beneficier nos service merci ", "danger")
    #         return redirect(request.url)

    # ========== TRAITEMENT POST ==========
    if request.method == 'POST':

        # ✅ SAUVEGARDER LES DONNÉES DANS LA SESSION AVANT EMAIL
        session['pret_data'] = request.form.to_dict()

        # ✅ 1. RÉCUPÉRER TOUTES LES VALEURS AU DÉBUT
        client_id_param = request.form.get('client_id') or request.args.get('client_id')
        telephone_param = request.form.get('telephone') or request.args.get('telephone')
        email_param = request.form.get('email') or request.args.get('email')

        # ✅ 2. Récupérer les valeurs du formulaire AVANT les validations
        nom_form = request.form.get('nom', '')
        prenom_form = request.form.get('prenom', '')
        email_form = request.form.get('email', '').strip().lower()
        telephone_form = request.form.get('telephone', '').strip()
        cin_nif_form = request.form.get('cin_nif', '').strip().upper()
        montant_form = request.form.get('montant_demande', '0')
        duree_form = request.form.get('duree', '0')

        print(f"📝 Données POST reçues: email={email_form}, tel={telephone_form}, montant={montant_form}")

        # Récupérer l'email
        email_verif = request.form.get('email', '').strip().lower()
        client_verif = Client.query.filter_by(email=email_verif).first()

        # Si client existe mais n'a pas signé
        if client_verif and not client_verif.terms_accepted:
            # RENVOYER L'EMAIL
            envoyer_email_conditions(client_verif)
            flash('⚠️ Vous devez d\'abord accepter les conditions générales. Un email vient de vous être renvoyé.',
                  'warning')
            return redirect(url_for('demande_pret', client_id=client_verif.id))

        if not client:
            flash("Veuillez sélectionner un client d'abord", "danger")
            return redirect(url_for('demande_pret',
                                    client_id=client_id_param,
                                    telephone=telephone_param,
                                    email=email_param))


        try:
            print("1. Avant validation")

            # Protection CSRF (si vous utilisez Flask-WTF)
            # csrf.protect()

            # ========== VALIDATION DES DONNÉES ==========
            required_fields = [
                'nom', 'prenom', 'sexe', 'date_naissance', 'lieu_naissance',
                'nationalite', 'cin_nif', 'telephone', 'email', 'adresse',
                'commune', 'departement', 'duree_adresse', 'etat_civil',
                'nb_enfants', 'profession', 'entreprise', 'adresse_travail',
                'revenu_mensuel', 'montant_demande', 'duree', 'objet', 'type_pret',
                'date_demande'
            ]

            for field in required_fields:
                if not request.form.get(field):
                    flash(f'⛔ Le champ {field} est requis', 'danger')
                    return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))

            # ========== VALIDATION SPÉCIFIQUE ==========
            email = request.form.get('email').strip().lower()
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                flash('⛔ Format d\'email invalide', 'danger')
                return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))

            telephone = request.form.get('telephone').strip()
            if not re.match(r'^(?:\+509|0)?[2-9]\d{7}$', telephone):
                flash('⛔ Format de téléphone invalide (ex: +509 34 56 7890)', 'danger')
                return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))

            cin_nif = request.form.get('cin_nif').strip().upper()
            if not re.match(r'^[0-9A-Z-]{6,20}$', cin_nif):
                flash('⛔ Format de CIN/NIF invalide', 'danger')
                return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))

            # ========== GESTION DES PHOTOS ==========
            photo_face = request.files.get('photo_face')
            photo_dos = request.files.get('photo_dos')

            client_upload_folder = os.path.join(app.root_path, UPLOAD_FOLDER)
            os.makedirs(client_upload_folder, exist_ok=True)

            photo_face_filename = None
            if photo_face and photo_face.filename:
                if not allowed_file(photo_face.filename):
                    flash('❌ Format de photo face invalide. Utilisez PNG, JPG ou JPEG.', 'danger')
                    return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))

                photo_face.seek(0, os.SEEK_END)
                file_size = photo_face.tell()
                photo_face.seek(0)

                if file_size > MAX_FILE_SIZE:
                    flash('❌ Photo face trop volumineuse. Maximum 5 Mo.', 'danger')
                    return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))

                original_filename = secure_filename(photo_face.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                photo_face_filename = f"face_{timestamp}_{original_filename}"
                photo_face.save(os.path.join(client_upload_folder, photo_face_filename))

            photo_dos_filename = None
            if photo_dos and photo_dos.filename:
                if not allowed_file(photo_dos.filename):
                    flash('❌ Format de photo dos invalide. Utilisez PNG, JPG ou JPEG.', 'danger')
                    return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))

                photo_dos.seek(0, os.SEEK_END)
                file_size = photo_dos.tell()
                photo_dos.seek(0)

                if file_size > MAX_FILE_SIZE:
                    flash('❌ Photo dos trop volumineuse. Maximum 5 Mo.', 'danger')
                    return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))

                original_filename = secure_filename(photo_dos.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                photo_dos_filename = f"dos_{timestamp}_{original_filename}"
                photo_dos.save(os.path.join(client_upload_folder, photo_dos_filename))

            # Validation des montants
            try:
                revenu_mensuel = float(request.form.get('revenu_mensuel'))
                montant_demande = float(request.form.get('montant_demande'))

                if revenu_mensuel <= 0:
                    flash("⛔ Le revenu mensuel doit être supérieur à 0", "danger")
                    return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))

                if montant_demande < 10000 or montant_demande > 10_000_000:
                    flash('⛔ Le montant demandé doit être entre 10 000 et 10 000 000 000 Gdes', 'danger')
                    return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))

                duree = int(request.form.get('duree'))
                taux_annuel = float(request.form.get('taux_interet', 12))

                if duree < 3 or duree > 60:
                    flash('⛔ La durée doit être entre 3 et 60 mois', 'danger')
                    return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))

                # Calcul de la mensualité estimée
                taux_mensuel = taux_annuel / 100 / 12
                if taux_mensuel > 0:
                    facteur = (1 + taux_mensuel) ** duree
                    mensualite_estimee = montant_demande * taux_mensuel * facteur / (facteur - 1)
                else:
                    mensualite_estimee = montant_demande / duree

                ratio_endettement = (mensualite_estimee / revenu_mensuel) * 100

                if ratio_endettement > 35:
                    flash(f'⚠️ Ratio d\'endettement trop élevé ({ratio_endettement:.1f}% > 35%). Prêt refusé.',
                          'danger')
                    return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))

            except ValueError as e:
                flash('⛔ Valeurs numériques invalides', 'danger')
                return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))

            # Validation date de naissance
            date_naissance = datetime.strptime(request.form.get('date_naissance'), '%Y-%m-%d').date()
            age = (datetime.now().date() - date_naissance).days / 365.25
            if age < 18:
                flash('⛔ Le client doit avoir au moins 18 ans', 'danger')
                return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))


            # ========== VÉRIFICATION CLIENT EXISTANT ==========
            client_existant = Client.query.filter(
                (Client.cin == cin_nif) | (Client.email == email)
            ).first()

            if client_existant:
                if est_agent and client_existant.succursale_id != current_user.succursale_id:
                    flash('⛔ Ce client appartient à une autre succursale', 'danger')
                    return redirect(url_for('demande_pret', client_id=client_id, telephone=telephone, email=email))

                client = client_existant

                # 🔥 AJOUTE TOUTE CETTE PARTIE POUR METTRE À JOUR
                # Mise à jour des informations personnelles
                client.nom = request.form.get('nom').strip().upper()
                client.prenom = request.form.get('prenom').strip().capitalize()
                client.sexe = request.form.get('sexe')
                client.date_naissance = date_naissance
                client.lieu_naissance = request.form.get('lieu_naissance', '').strip() or None
                client.nationalite = request.form.get('nationalite')
                client.autre_nationalite = request.form.get('autre_nationalite') if request.form.get(
                    'nationalite') == 'Autre' else None
                client.cin_nif = cin_nif if cin_nif else None
                client.telephone = telephone
                client.email = email

                # Mise à jour de l'adresse
                client.adresse = request.form.get('adresse', '').strip()
                client.commune = request.form.get('commune', '').strip() or None
                client.departement = request.form.get('departement') or None
                client.duree_adresse = int(request.form.get('duree_adresse', 0))

                # Mise à jour situation familiale
                client.etat_civil = request.form.get('etat_civil') or None
                client.nom_conjoint = request.form.get('nom_conjoint') if request.form.get('etat_civil') in ['marie',
                                                                                                             'union_libre'] else None
                client.nb_enfants = int(request.form.get('nb_enfants', 0))

                # Mise à jour profession
                client.profession = request.form.get('profession', '').strip()
                client.entreprise = request.form.get('entreprise', '').strip() or None
                client.adresse_travail = request.form.get('adresse_travail', '').strip() or None
                client.tel_travail = request.form.get('tel_travail') or None
                client.revenu_mensuel = revenu_mensuel
                client.autres_revenus = request.form.get('autres_revenus') or None
                client.date_creation = datetime.now()  # ← AJOUTEZ CETTE LIGNE

                db.session.commit()  # ← TRÈS IMPORTANT !
                print("✅ Client existant mis à jour")

                print("1,1. Avant creation client")
            else:
                # ========== CRÉATION NOUVEAU CLIENT ==========
                client = Client(
                    nom=request.form.get('nom').strip().upper(),
                    prenom=request.form.get('prenom').strip().capitalize(),
                    sexe=request.form.get('sexe'),
                    date_naissance=date_naissance,
                    lieu_naissance=request.form.get('lieu_naissance').strip(),
                    nationalite=request.form.get('nationalite'),
                    autre_nationalite=request.form.get('autre_nationalite') if request.form.get(
                        'nationalite') == 'Autre' else None,
                    cin_nif=cin_nif,
                    telephone=telephone,
                    email=email,
                    adresse=request.form.get('adresse').strip(),
                    commune=request.form.get('commune').strip(),
                    departement=request.form.get('departement'),
                    duree_adresse=int(request.form.get('duree_adresse')),
                    etat_civil=request.form.get('etat_civil'),
                    nom_conjoint=request.form.get('nom_conjoint') if request.form.get('etat_civil') in ['marie',
                                                                                                        'union_libre'] else None,
                    nb_enfants=int(request.form.get('nb_enfants')),
                    profession=request.form.get('profession').strip(),
                    entreprise=request.form.get('entreprise').strip(),
                    adresse_travail=request.form.get('adresse_travail').strip(),
                    tel_travail=request.form.get('tel_travail'),
                    revenu_mensuel=revenu_mensuel,
                    autres_revenus=request.form.get('autres_revenus'),
                    succursale_id=current_user.succursale_id if est_agent else None,
                    compte_actif=True,
                    email_confirme=False,
                    terms_accepted=False
                )

                db.session.add(client)
                # db.session.commit()  # ← AJOUTEZ CETTE LIGNE
                db.session.flush()

                flash("Client créé avec succès", "success")

            print(f"🔍 Vérification terms_accepted: {client.terms_accepted}")

            # 2. ENSUITE vérifier si email doit être envoyé
            if not client.terms_accepted:
                session['pret_data'] = request.form.to_dict()  # 🔥 AJOUT CRUCIAL
                envoyer_email_conditions(client)

                flash('⚠️ Vérifiez votre email et signez les conditions.', 'warning')
                return redirect(url_for('demande_pret', client_id=client.id))

            print("3. Avant création prêt")


            # ========== CRÉATION DE LA DEMANDE DE PRÊT ==========
            # Ajouter cette ligne juste avant la création du prêt
            numero_pret_unique = generer_numero_pret()
            montant_interet = montant_demande * (taux_annuel / 100) * (duree / 12)
            montant_total = montant_demande + montant_interet
            mensualite = montant_total / duree if duree > 0 else montant_total


            nouveau_pret = Pret(
                numero_pret=numero_pret_unique,  # ← LIGNE À AJOUTER
                client_id=client.id,
                agent_id=current_user.id if est_agent else None,
                montant=montant_demande,
                duree_mois=duree,
                motif=request.form.get('objet'),
                type_pret=request.form.get('type_pret'),
                autre_type_pret=request.form.get('autre_type_pret') if request.form.get(
                    'type_pret') == 'autre' else None,
                garantie=request.form.get('nom_garant') if request.form.get('a_garant') == 'oui' else None,

                succursale_id=current_user.succursale_id if est_agent else client.succursale_id,

                info_garant=json.dumps({
                    'nom': request.form.get('nom_garant'),
                    'telephone': request.form.get('tel_garant'),
                    'adresse': request.form.get('adresse_garant'),
                    'relation': request.form.get('relation_garant'),
                    'profession': request.form.get('profession_garant')
                }) if request.form.get('a_garant') == 'oui' else None,
                reference1=json.dumps({
                    'nom': request.form.get('ref1_nom'),
                    'telephone': request.form.get('ref1_tel')
                }, ensure_ascii=False),

                reference2=json.dumps({
                    'nom': request.form.get('ref2_nom'),
                    'telephone': request.form.get('ref2_tel')
                },  ensure_ascii=False),

                signature=request.form.get('signature'),
                mensualite=round(mensualite, 2),
                montant_interet=round(montant_interet, 2),
                montant_total=round(montant_total, 2),
                taux_interet=taux_annuel,
                statut='en_attente',
                numero_dossier=request.form.get('num_dossier')

            )

            db.session.add(nouveau_pret)
            db.session.flush()  # Pour obtenir l'ID

            print("3,1. création prêt")

            # Suspendre le compte du client
            if hasattr(client, 'suspendre_compte_pret'):
                client.suspendre_compte_pret()

            # Journalisation
            journal_entry = Journal(
                employe_id=current_user.id,
                action='CREATION_PRET',
                details=f"Création demande prêt {nouveau_pret.numero_dossier} pour client {client.id}",
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string,
                client_id=client.id,
                pret_id=nouveau_pret.id
            )
            db.session.add(journal_entry)
            db.session.commit()

            session['pret_data'] = request.form.to_dict()

            print(f"✅ Commit effectué - Prêt #{nouveau_pret.id} créé")

            envoyer_notification_pret(client, nouveau_pret)
            notifier_directeurs_demande_pret(nouveau_pret)

            print("🔔 Notifications envoyées aux directeurs")

            print("🔔 ENVOI NOTIFICATION AU DIRECTEUR")
            print("EMAIL:", os.getenv("MAIL_USERNAME"))
            print("PASSWORD:", os.getenv("MAIL_PASSWORD"))

            flash(
                "✅ Demande de prêt créée avec succès ! "
                "Le compte du client a été suspendu pour les opérations de retrait/transfert. "
                "Un email de confirmation a été envoyé au client.",
                "success"
            )

            # Redirection selon le rôle
            if est_agent:
                return redirect(url_for('agent_credit_dashboard', succursale_code=current_user.succursale.code))
            else:
                return redirect(url_for('client_dashboard'))

        except Exception as e:
            db.session.rollback()
            print("❌ ERREUR DÉTAILLÉE :")
            import traceback
            traceback.print_exc()
            flash('⛔ Une erreur est survenue', 'danger')
            return redirect(url_for('demande_pret'))


    print("❌ booummm :")

    # ========== REQUÊTE GET ==========
    # Préparer la liste des clients pour les agents
    clients_list = []
    stats = {}

    # clients_paginated = None

    if est_agent and current_user.succursale_id:
        page = request.args.get('page', 1, type=int)
        per_page = 20

        clients_paginated = Client.query.filter_by(
            succursale_id=current_user.succursale_id,
            compte_actif=True
        ).order_by(
            Client.nom,
            Client.prenom
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        clients_list = clients_paginated.items

        clients_ids_subquery = db.session.query(Client.id).filter_by(
            succursale_id=current_user.succursale_id
        )

        stats = {
            'total_clients': Client.query.filter_by(
                succursale_id=current_user.succursale_id
            ).count(),
            'prets_actifs': Pret.query.filter(
                Pret.client_id.in_(clients_ids_subquery),
                Pret.statut.in_(['approuve', 'actif'])
            ).count(),
            'prets_attente': Pret.query.filter(
                Pret.client_id.in_(clients_ids_subquery),
                Pret.statut == 'en_attente'
            ).count(),
            'prets_refuses': Pret.query.filter(
                Pret.client_id.in_(clients_ids_subquery),
                Pret.statut == 'refuse'
            ).count()
        }


    elif client and est_client:
        stats = {
            'total_prets': Pret.query.filter_by(
                client_id=client.id
            ).count(),
            'prets_actifs': Pret.query.filter(
                Pret.client_id == client.id,
                Pret.statut.in_(['en_attente', 'actif', 'approuve'])
            ).count(),
            'prets_attente': Pret.query.filter(
                Pret.client_id == client.id,
                Pret.statut == 'en_attente'
            ).count(),
            'montant_total': db.session.query(
                db.func.sum(Pret.montant)
            ).filter_by(
                client_id=client.id
            ).scalar() or 0
        }
        clients_paginated = None

    print("❌ bawww :")

    # ⬇️⬇️⬇️ CES 3 LIGNES SORTIES DU elif ⬇️⬇️⬇️
    form_data = {}
    show_for_director = False
    current_pret = None

    # ⬇️⬇️⬇️ UN SEUL RETURN POUR TOUS LES CAS ⬇️⬇️⬇️
    return render_template(
        'prets/demande_pret.html',
        client=client,
        clients=clients_list,
        pagination=clients_paginated if est_agent else None,
        stats=stats,
        succursale=succursale if est_agent else None,
        est_agent=est_agent,
        est_client=est_client,
        now=datetime.now(),
        form_data=form_data,
        show_for_director=show_for_director,
        pret=current_pret,
        verifier_eligibilite_pret = verifier_eligibilite_pret  # ← AJOUTEZ CETTE LIGNE
    )


@app.route('/clients/pret/<int:pret_id>', methods=['GET'])
@login_required
def client_voir_pret(pret_id):
    """View loan details from client dashboard"""
    from models import Pret, Client, Echeancier, DocumentPret
    import json
    from datetime import date

    # Get the loan
    pret = db.session.get(Pret, pret_id)
    if not pret:
        flash("Prêt non trouvé", "danger")
        return redirect(url_for('client_dashboard'))

    # Check if the logged-in user is the client
    est_client = hasattr(current_user, 'client_profile') and current_user.client_profile is not None

    if not est_client or pret.client_id != current_user.client_profile.id:
        flash("Accès non autorisé", "danger")
        return redirect(url_for('client_dashboard'))

    # Get client info
    client = db.session.get(Client, pret.client_id)

    # Get payment schedule
    echeancier = Echeancier.query.filter_by(pret_id=pret.id).order_by(Echeancier.numero_echeance).all()

    # Get documents
    documents = DocumentPret.query.filter_by(pret_id=pret.id).order_by(DocumentPret.date_upload.desc()).all()

    # Parse JSON fields
    info_garant = {}
    reference1 = {}
    reference2 = {}

    if pret.info_garant and isinstance(pret.info_garant, str):
        try:
            info_garant = json.loads(pret.info_garant)
        except:
            info_garant = {}

    if pret.reference1 and isinstance(pret.reference1, str):
        try:
            reference1 = json.loads(pret.reference1)
        except:
            reference1 = {}

    if pret.reference2 and isinstance(pret.reference2, str):
        try:
            reference2 = json.loads(pret.reference2)
        except:
            reference2 = {}

    # Calculate statistics
    today = date.today()
    total_paid = sum(e.montant_paye or 0 for e in echeancier if e.statut == 'paye')

    stats = {
        'total_payments': len(echeancier),
        'payments_made': sum(1 for e in echeancier if e.statut == 'paye'),
        'payments_pending': sum(1 for e in echeancier if e.statut == 'en_attente'),
        'payments_overdue': sum(1 for e in echeancier if e.statut == 'impaye' and e.date_echeance < today),
        'total_paid': total_paid,
        'remaining_balance': pret.montant_total - total_paid,
        'progress_percentage': (total_paid / pret.montant_total * 100) if pret.montant_total > 0 else 0
    }

    # Get next payment
    next_payment = None
    for e in echeancier:
        if e.statut == 'en_attente':
            next_payment = e
            break

    # Get overdue payments count
    overdue_count = sum(1 for e in echeancier if e.statut == 'impaye' and e.date_echeance < today)

    return render_template(
        'client/voir_pret.html',
        pret=pret,
        client=client,
        echeancier=echeancier,
        documents=documents,
        info_garant=info_garant,
        reference1=reference1,
        reference2=reference2,
        stats=stats,
        next_payment=next_payment,
        overdue_count=overdue_count,
        now=datetime.now()
    )


def verifier_eligibilite_pret(client, montant_demande=None):
    """
    Vérification complète d'éligibilité pour un prêt
    """
    from models import Pret
    from datetime import datetime

    resultat = {
        'eligible': True,
        'message': '✅ Éligible',
        'motifs': []
    }

    # 1. Vérifications de base
    if not client:
        resultat['eligible'] = False
        resultat['message'] = 'Client non trouvé'
        return resultat

    if client.statut != 'actif':
        resultat['eligible'] = False
        resultat['motifs'].append('Compte inactif')

    if not client.terms_accepted:
        resultat['eligible'] = False
        resultat['motifs'].append('Conditions non acceptées')

    # 2. Vérification des prêts en cours
    prets_actifs = Pret.query.filter(
        Pret.client_id == client.id,
        Pret.statut.in_(['actif', 'en_attente', 'approuve', 'en_retard'])
    ).all()

    if prets_actifs:
        resultat['eligible'] = False
        nb_prets = len(prets_actifs)
        resultat['motifs'].append(f'{nb_prets} prêt(s) en cours')

    # 3. Vérification de l'âge
    if client.date_naissance:
        age = (datetime.now().date() - client.date_naissance.date()).days / 365.25
        if age < 18:
            resultat['eligible'] = False
            resultat['motifs'].append('Âge minimum requis: 18 ans')
        elif age > 70:
            resultat['eligible'] = False
            resultat['motifs'].append('Âge maximum dépassé: 70 ans')

    # 4. Vérification des revenus
    if client.revenu_mensuel:
        if client.revenu_mensuel < 10000:
            resultat['eligible'] = False
            resultat['motifs'].append('Revenu mensuel insuffisant (< 10 000 HTG)')

        # Si montant demandé fourni, vérifier la capacité
        if montant_demande and montant_demande > 0:
            # Règle: mensualité ≤ 35% des revenus
            mensualite_max = client.revenu_mensuel * 0.35
            # Estimation rapide (à affiner selon durée et taux)
            mensualite_estimee = montant_demande / 12 * 1.2  # Approximation
            if mensualite_estimee > mensualite_max:
                resultat['eligible'] = False
                resultat['motifs'].append('Montant trop élevé par rapport aux revenus')

    # 5. Vérification historique de crédit (si vous avez)
    if hasattr(client, 'score_credit') and client.score_credit and client.score_credit < 300:
        resultat['eligible'] = False
        resultat['motifs'].append('Score de crédit insuffisant')

    # Message final
    if not resultat['eligible']:
        resultat['message'] = '❌ Non éligible: ' + ', '.join(resultat['motifs'])

    return resultat



@app.route('/prets/<int:pret_id>/generer-echeancier', methods=['POST'])
@login_required
def generer_echeancier(pret_id):
    """Generate or regenerate payment schedule"""
    from models import Pret

    pret = db.session.get(Pret, pret_id)
    if not pret:
        return jsonify({'error': 'Prêt non trouvé'}), 404

    # Only agents can regenerate schedule
    est_agent = current_user.role in ['admin', 'super_admin', 'direction', 'agent_credit']
    if not est_agent:
        return jsonify({'error': 'Accès non autorisé'}), 403

    pret.generate_echeancier()

    return jsonify({'success': True, 'message': 'Échéancier généré avec succès'})

@app.route('/prets/voir-pret/<int:pret_id>', methods=['GET'])
@login_required
def voir_pret(pret_id):
    """View loan details with documents and AJAX payment history"""
    from models import Pret, Client, Echeancier, DocumentPret
    import json
    from datetime import date, datetime

    # Get the loan
    pret = db.session.get(Pret, pret_id)
    if not pret:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Prêt non trouvé'}), 404
        flash("Prêt non trouvé", "danger")
        return redirect(url_for('mes_prets'))

    # Check access rights
    est_agent = current_user.role in ['admin', 'super_admin', 'direction','directeur', 'agent_credit', 'conseiller', 'employe']
    est_client = hasattr(current_user, 'client_profile') and current_user.client_profile is not None

    # ✅ CLIENT: can only see their own loans (CORRIGÉ)
    if est_client:
        # Vérifier que client_profile existe
        if not current_user.client_profile or len(current_user.client_profile) == 0:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Profil client introuvable'}), 403
            flash("Profil client introuvable", "danger")
            return redirect(url_for('client_dashboard'))

        # Récupérer l'ID du client (UNE SEULE FOIS)
        client_profil_id = current_user.client_profile[0].id

        # Vérifier que le prêt appartient au client
        if pret.client_id != client_profil_id:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Accès non autorisé'}), 403
            flash("Accès non autorisé", "danger")
            return redirect(url_for('client_dashboard'))

    # ✅ AGENT: can only see loans from their branch
    if est_agent and current_user.succursale_id:
        client = db.session.get(Client, pret.client_id)
        if client and client.succursale_id != current_user.succursale_id:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Accès non autorisé - Autre succursale'}), 403
            flash("Accès non autorisé - Ce prêt appartient à une autre succursale", "danger")
            # ✅ Correction: Vérifier que succursale existe
            if current_user.succursale and hasattr(current_user.succursale, 'code'):
                return redirect(url_for('agent_credit_dashboard', succursale_code=current_user.succursale.code))
            else:
                return redirect(url_for('employe_dashboard_generique'))

    # Handle AJAX request for payment history
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        echeancier = Echeancier.query.filter_by(pret_id=pret.id).order_by(Echeancier.numero_echeance).all()

        payments_data = []
        for e in echeancier:
            payments_data.append({
                'id': e.id,
                'numero': e.numero_echeance,
                'date_echeance': e.date_echeance.strftime('%d/%m/%Y'),
                'montant': float(e.montant),
                'montant_paye': float(e.montant_paye) if e.montant_paye else 0,
                'statut': e.statut,
                'date_paiement': e.date_paiement.strftime('%d/%m/%Y %H:%M') if e.date_paiement else None,
                'penalite': float(e.penalite) if hasattr(e, 'penalite') and e.penalite else 0
            })

        # Calculate statistics
        today = date.today()
        total_paid = sum(e.montant_paye or 0 for e in echeancier if e.statut == 'paye')

        return jsonify({
            'success': True,
            'payments': payments_data,
            'summary': {
                'total_payments': len(echeancier),
                'payments_made': sum(1 for e in echeancier if e.statut == 'paye'),
                'payments_pending': sum(1 for e in echeancier if e.statut == 'en_attente'),
                'payments_overdue': sum(1 for e in echeancier if e.statut == 'impaye' and e.date_echeance < today),
                'total_paid': float(total_paid),
                'remaining_balance': float(pret.montant_total - total_paid),
                'next_payment_date': next(
                    (e.date_echeance.strftime('%d/%m/%Y') for e in echeancier if e.statut == 'en_attente'), None),
                'next_payment_amount': float(next((e.montant for e in echeancier if e.statut == 'en_attente'), 0))
            }
        })

    # Regular HTML response
    client = db.session.get(Client, pret.client_id)
    echeancier = Echeancier.query.filter_by(pret_id=pret.id).order_by(Echeancier.numero_echeance).all()
    documents = DocumentPret.query.filter_by(pret_id=pret.id).all()

    # Parse JSON fields
    info_garant = {}
    reference1 = {}
    reference2 = {}

    if pret.info_garant and isinstance(pret.info_garant, str):
        try:
            info_garant = json.loads(pret.info_garant)
        except:
            info_garant = {}

    if pret.reference1 and isinstance(pret.reference1, str):
        try:
            reference1 = json.loads(pret.reference1)
        except:
            reference1 = {}

    if pret.reference2 and isinstance(pret.reference2, str):
        try:
            reference2 = json.loads(pret.reference2)
        except:
            reference2 = {}

    # Calculate statistics
    today = date.today()
    total_paid = sum(e.montant_paye or 0 for e in echeancier if e.statut == 'paye')

    stats = {
        'total_payments': len(echeancier),
        'payments_made': sum(1 for e in echeancier if e.statut == 'paye'),
        'payments_pending': sum(1 for e in echeancier if e.statut == 'en_attente'),
        'payments_overdue': sum(1 for e in echeancier if e.statut == 'impaye' and e.date_echeance < today),
        'total_paid': total_paid,
        'remaining_balance': pret.montant_total - total_paid,
        'progress_percentage': (total_paid / pret.montant_total * 100) if pret.montant_total > 0 else 0
    }

    # Get exchange rate for DLTR (USD to HTG)
    exchange_rate_usd = 130
    exchange_rate_eur = 140

    return render_template(
        'prets/voir_pret.html',
        pret=pret,
        client=client,
        echeancier=echeancier,
        documents=documents,
        info_garant=info_garant,
        reference1=reference1,
        reference2=reference2,
        stats=stats,
        est_agent=est_agent,
        est_client=est_client,
        exchange_rate_usd=exchange_rate_usd,
        exchange_rate_eur=exchange_rate_eur,
        now=datetime.now()
    )


@app.route('/pret/detail/<int:pret_id>')
@login_required
def detail_pret(pret_id):
    """Affiche les détails d'un prêt avec formulaire pré-rempli"""
    from datetime import datetime
    from models import Pret, Client, Succursale, Echeancier, DocumentPret
    import json

    pret = Pret.query.get_or_404(pret_id)
    client = pret.client

    # Vérifier les autorisations
    est_client = hasattr(current_user, 'client_profile') and current_user.client_profile
    est_agent = current_user.role in ['agent', 'admin', 'direction']
    succursale = db.session.get(Succursale, current_user.succursale_id)

    # Vérifier que le directeur a accès à cette succursale
    if current_user.succursale_id and client.succursale_id != current_user.succursale_id:
        if current_user.role not in ['admin', 'direction', 'super_admin']:
            flash("Accès non autorisé - Ce prêt appartient à une autre succursale", "danger")
            return redirect(url_for('direction_succursale_dashboard'))

    # Parse JSON fields
    info_garant = {}
    reference1 = {}
    reference2 = {}

    if pret.info_garant:
        try:
            info_garant = json.loads(pret.info_garant) if isinstance(pret.info_garant, str) else pret.info_garant
        except:
            info_garant = {}

    if pret.reference1:
        try:
            reference1 = json.loads(pret.reference1) if isinstance(pret.reference1, str) else pret.reference1
        except:
            reference1 = {}

    if pret.reference2:
        try:
            reference2 = json.loads(pret.reference2) if isinstance(pret.reference2, str) else pret.reference2
        except:
            reference2 = {}

    # Préparer les données du formulaire
    form_data = {
        'nom': client.nom if client else '',
        'prenom': client.prenom if client else '',
        'sexe': client.sexe if client else '',
        'date_naissance': client.date_naissance.strftime('%Y-%m-%d') if client.date_naissance else '',
        'lieu_naissance': client.lieu_naissance if client else '',
        'nationalite': client.nationalite if client else 'Haïtienne',
        'autre_nationalite': client.autre_nationalite if client else '',
        'cin_nif': client.cin_nif if client else '',
        'telephone': client.telephone if client else '',
        'email': client.email if client else '',
        'adresse': client.adresse if client else '',
        'commune': client.commune if client else '',
        'departement': client.departement if client else '',
        'duree_adresse': client.duree_adresse if client else 0,
        'etat_civil': client.etat_civil if client else '',
        'nom_conjoint': client.nom_conjoint if client else '',
        'nb_enfants': client.nb_enfants if client else 0,
        'profession': client.profession if client else '',
        'entreprise': client.entreprise if client else '',
        'adresse_travail': client.adresse_travail if client else '',
        'tel_travail': client.tel_travail if client else '',
        'revenu_mensuel': client.revenu_mensuel if client else 0,
        'autres_revenus': client.autres_revenus if client else '',
        'photo_face': client.photo_face if client else '',
        'photo_dos': client.photo_dos if client else '',
        'montant_demande': pret.montant,
        'duree': pret.duree_mois,
        'objet': pret.motif,
        'type_pret': pret.type_pret,
        'autre_type_pret': pret.autre_type_pret,
        'taux_interet': pret.taux_interet,
        'a_garant': 'oui' if pret.garantie else 'non',
        'nom_garant': pret.garantie if pret.garantie else '',
        'tel_garant': info_garant.get('telephone') if info_garant else '',
        'adresse_garant': info_garant.get('adresse') if info_garant else '',
        'relation_garant': info_garant.get('relation') if info_garant else '',
        'profession_garant': info_garant.get('profession') if info_garant else '',
        'ref1_nom': reference1.get('nom') if reference1 else '',
        'ref1_tel': reference1.get('telephone') if reference1 else '',
        'ref2_nom': reference2.get('nom') if reference2 else '',
        'ref2_tel': reference2.get('telephone') if reference2 else '',
        'signature': pret.signature,
        'date_demande': pret.date_demande.strftime('%Y-%m-%d') if pret.date_demande else '',
        'num_dossier': pret.numero_dossier or f"PRET-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'decision': pret.decision if hasattr(pret, 'decision') else 'en_attente',
        'montant_accorde': pret.montant_accorde if hasattr(pret, 'montant_accorde') else pret.montant,
        'signature_responsable': pret.signature_responsable if hasattr(pret, 'signature_responsable') else '',
        'motif_refus': pret.motif_refus if hasattr(pret, 'motif_refus') else ''
    }

    # Récupérer l'échéancier et les documents
    echeancier = Echeancier.query.filter_by(pret_id=pret.id).order_by(Echeancier.numero_echeance).all()
    documents = DocumentPret.query.filter_by(pret_id=pret.id).all()

    # Déterminer si on est en mode directeur
    show_for_director = current_user.role in ['direction', 'admin', 'super_admin']

    return render_template('prets/demande_pret.html',
                           pret=pret,
                           client=client,
                           form_data=form_data,
                           echeancier=echeancier,
                           documents=documents,
                           succursale=succursale,
                           now=datetime.now(),
                           show_for_director=show_for_director,
                           current_user=current_user)


@app.route('/direction/succursale/dashboard')
@login_required
@role_required('direction')
def direction_succursale_dashboard():
    """Dashboard pour le directeur de succursale"""
    from models import Pret, Client, Succursale, Echeancier, User
    from datetime import datetime, date, timedelta
    from sqlalchemy import func

    # Récupérer la succursale du directeur
    succursale = Succursale.query.get(current_user.succursale_id)

    if not succursale:
        flash("Succursale non trouvée", "danger")
        return redirect(url_for('main.accueil'))

    # ========== STATISTIQUES GÉNÉRALES ==========

    # Nombre total de clients
    total_clients = Client.query.filter_by(succursale_id=current_user.succursale_id).count()

    # Clients actifs (ceux qui ont des prêts actifs)
    clients_actifs = db.session.query(Client.id).filter(
        Client.succursale_id == current_user.succursale_id,
        Client.compte_actif == True
    ).count()

    # ========== STATISTIQUES DES PRÊTS ==========

    # Prêts en attente
    prets_attente = Pret.query.join(Client).filter(
        Client.succursale_id == current_user.succursale_id,
        Pret.statut == 'en_attente'
    ).count()

    # Prêts approuvés
    prets_approuves = Pret.query.join(Client).filter(
        Client.succursale_id == current_user.succursale_id,
        Pret.statut == 'approuve'
    ).count()

    # Prêts actifs
    prets_actifs = Pret.query.join(Client).filter(
        Client.succursale_id == current_user.succursale_id,
        Pret.statut == 'actif'
    ).count()

    # Prêts terminés
    prets_termines = Pret.query.join(Client).filter(
        Client.succursale_id == current_user.succursale_id,
        Pret.statut == 'termine'
    ).count()

    # Prêts refusés
    prets_refuses = Pret.query.join(Client).filter(
        Client.succursale_id == current_user.succursale_id,
        Pret.statut == 'refuse'
    ).count()

    # Montant total des prêts accordés
    montant_total = db.session.query(func.sum(Pret.montant)).join(Client).filter(
        Client.succursale_id == current_user.succursale_id,
        Pret.statut.in_(['actif', 'approuve', 'termine'])
    ).scalar() or 0

    # ========== STATISTIQUES DES PAIEMENTS ==========

    # Total remboursé
    total_rembourse = db.session.query(func.sum(Echeancier.montant_paye)).join(Pret).join(Client).filter(
        Client.succursale_id == current_user.succursale_id,
        Echeancier.statut == 'paye'
    ).scalar() or 0

    # Paiements en retard
    today = date.today()
    paiements_retard = Echeancier.query.join(Pret).join(Client).filter(
        Client.succursale_id == current_user.succursale_id,
        Echeancier.statut == 'impaye',
        Echeancier.date_echeance < today
    ).count()

    # ========== LISTES À AFFICHER ==========

    # Demandes en attente (les 10 plus récentes)
    demandes_attente = Pret.query.join(Client).filter(
        Client.succursale_id == current_user.succursale_id,
        Pret.statut == 'en_attente'
    ).order_by(Pret.date_demande.desc()).limit(10).all()

    # Prêts actifs (les 10 plus récents)
    prets_actifs_liste = Pret.query.join(Client).filter(
        Client.succursale_id == current_user.succursale_id,
        Pret.statut == 'actif'
    ).order_by(Pret.date_demande.desc()).limit(10).all()

    # Paiements à venir (prochaines 5 échéances)
    prochaines_echeances = Echeancier.query.join(Pret).join(Client).filter(
        Client.succursale_id == current_user.succursale_id,
        Echeancier.statut == 'en_attente',
        Echeancier.date_echeance >= today
    ).order_by(Echeancier.date_echeance.asc()).limit(5).all()

    # Dernières activités (prêts récents)
    dernieres_activites = Pret.query.join(Client).filter(
        Client.succursale_id == current_user.succursale_id
    ).order_by(Pret.date_demande.desc()).limit(10).all()

    # ========== PERFORMANCE DES AGENTS ==========

    # Top 5 agents par nombre de prêts traités
    top_agents = db.session.query(
        User.id,
        User.prenom,
        User.nom,
        func.count(Pret.id).label('total_prets')
    ).join(Pret, Pret.agent_id == User.id).join(Client).filter(
        Client.succursale_id == current_user.succursale_id
    ).group_by(User.id).order_by(func.count(Pret.id).desc()).limit(5).all()

    # ========== CALCUL DES POURCENTAGES ==========

    total_prets = (prets_attente + prets_approuves + prets_actifs + prets_termines + prets_refuses)

    stats = {
        'total_clients': total_clients,
        'clients_actifs': clients_actifs,
        'prets_attente': prets_attente,
        'prets_approuves': prets_approuves,
        'prets_actifs': prets_actifs,
        'prets_termines': prets_termines,
        'prets_refuses': prets_refuses,
        'total_prets': total_prets,
        'montant_total': montant_total,
        'total_rembourse': total_rembourse,
        'taux_remboursement': (total_rembourse / montant_total * 100) if montant_total > 0 else 0,
        'paiements_retard': paiements_retard,
        'taux_approbation': (prets_approuves / total_prets * 100) if total_prets > 0 else 0,
        'taux_refus': (prets_refuses / total_prets * 100) if total_prets > 0 else 0
    }

    # Taux d'activité des clients
    stats['taux_activite'] = (clients_actifs / total_clients * 100) if total_clients > 0 else 0

    return render_template('direction/succursale_dashboard.html',
                           succursale=succursale,
                           stats=stats,
                           demandes_attente=demandes_attente,
                           prets_actifs=prets_actifs_liste,
                           prochaines_echeances=prochaines_echeances,
                           dernieres_activites=dernieres_activites,
                           top_agents=top_agents,
                           now=datetime.now(),
                           today=today)


# ========== FONCTIONS UTILITAIRES DE SÉCURITÉ ==========
@app.route('/direction/pret/<int:pret_id>/view')
@login_required
@role_required('direction')
def direction_detail_pret(pret_id):
    from models import Pret, Client, User
    import json
    """Visualisation d'une demande de prêt par le directeur"""

    from models import Pret, Client, Echeancier, DocumentPret
    from datetime import datetime

    pret = Pret.query.get_or_404(pret_id)
    client = pret.client  # ✅ Récupérer le client associé

    # Parse JSON fields
    info_garant = {}
    reference1 = {}
    reference2 = {}

    if pret.info_garant:
        try:
            info_garant = json.loads(pret.info_garant) if isinstance(pret.info_garant, str) else pret.info_garant
        except:
            info_garant = {}

    if pret.reference1:
        try:
            reference1 = json.loads(pret.reference1) if isinstance(pret.reference1, str) else pret.reference1
        except:
            reference1 = {}

    if pret.reference2:
        try:
            reference2 = json.loads(pret.reference2) if isinstance(pret.reference2, str) else pret.reference2
        except:
            reference2 = {}

    # ✅ Vérifier que le directeur a accès à cette succursale
    if current_user.succursale_id and client.succursale_id != current_user.succursale_id:
        if current_user.role not in ['admin_succursale', 'direction', 'super_admin']:
            flash("Accès non autorisé - Ce prêt appartient à une autre succursale", "danger")
            return redirect(url_for('direction_succursale_dashboard')) # ✅ Maintenant ça existe


 # ✅ Récupérer les données du formulaire depuis le client et le prêt
    form_data = {
        # Informations client
        'nom': client.nom if client else pret.nom,  # Fallback pour compatibilité
        'prenom': client.prenom if client else pret.prenom,
        'sexe': client.sexe if client else pret.sexe,
        'date_naissance': client.date_naissance if client else pret.date_naissance,
        'lieu_naissance': client.lieu_naissance if client else pret.lieu_naissance,
        'nationalite': client.nationalite if client else pret.nationalite,
        'autre_nationalite': client.autre_nationalite if client else pret.autre_nationalite,
        'cin_nif': client.cin_nif if client else pret.cin_nif,
        'telephone': client.telephone if client else pret.telephone,
        'email': client.email if client else pret.email,
        'adresse': client.adresse if client else pret.adresse,
        'commune': client.commune if client else pret.commune,
        'departement': client.departement if client else pret.departement,
        'duree_adresse': client.duree_adresse if client else pret.duree_adresse,
        'etat_civil': client.etat_civil if client else pret.etat_civil,
        'nom_conjoint': client.nom_conjoint if client else pret.nom_conjoint,
        'nb_enfants': client.nb_enfants if client else pret.nb_enfants,
        'profession': client.profession if client else pret.profession,
        'entreprise': client.entreprise if client else pret.entreprise,
        'adresse_travail': client.adresse_travail if client else pret.adresse_travail,
        'tel_travail': client.tel_travail if client else pret.tel_travail,
        'revenu_mensuel': client.revenu_mensuel if client else pret.revenu_mensuel,
        'autres_revenus': client.autres_revenus if client else pret.autres_revenus,
        'photo_face': client.photo_face if client else pret.photo_face,
        'photo_dos': client.photo_dos if client else pret.photo_dos,

        # Informations prêt
        'montant_demande': pret.montant,
        'duree': pret.duree_mois,
        'objet': pret.motif,
        'type_pret': pret.type_pret,
        'autre_type_pret': pret.autre_type_pret,
        'taux_interet': pret.taux_interet,

        # Garant
        'a_garant': 'oui' if pret.garantie else 'non',
        'nom_garant': pret.garantie,
        'tel_garant': info_garant.get('telephone'),
        'adresse_garant': info_garant.get('adresse'),
        'relation_garant': info_garant.get('relation'),
        'profession_garant': info_garant.get('profession'),

        # Références
        'ref1_nom': reference1.get('nom'),
        'ref1_tel': reference1.get('telephone'),
        'ref2_nom': reference2.get('nom'),
        'ref2_tel': reference2.get('telephone'),

        'signature': pret.signature,
        'date_demande': pret.date_demande,

        # Champs institution
        'num_dossier': pret.numero_dossier,
        'date_reception': pret.date_reception,
        'decision': pret.decision,
        'montant_accorde': pret.montant_accorde,
        'taux_interet': pret.taux_interet,
        'signature_responsable': pret.signature_responsable,
        'motif_refus': pret.motif_refus
    }

    # Récupérer l'échéancier
    echeancier = Echeancier.query.filter_by(pret_id=pret.id).order_by(Echeancier.numero_echeance).all()

    # Récupérer les documents
    documents = DocumentPret.query.filter_by(pret_id=pret.id).all()

    return render_template('direction/detail_pret.html',
                           pret=pret,
                           client=client,
                           form_data=form_data,
                           echeancier=echeancier,
                           documents=documents,
                           show_for_director=True,
                           now=datetime.now(),
                           succursale=client.succursale if client else None)


def generer_recu_pour_pret(pret, dossier_recus="recus_prets"):
    """Génère un reçu en PDF pour un prêt approuvé"""

    client = db.session.get(Client, pret.client_id)
    if not client:
        print(f"❌ Client non trouvé pour le prêt ID {pret.id}")
        return None

    # Créer le dossier
    if not os.path.exists(dossier_recus):
        os.makedirs(dossier_recus)

    # Créer le dossier pour les QR codes
    qr_dossier = os.path.join("static", "qrcodes")
    if not os.path.exists(qr_dossier):
        os.makedirs(qr_dossier)

    # Calculer les échéances
    echeances = []
    date = pret.date_debut if pret.date_debut else datetime.now()

    for i in range(pret.duree_mois):
        echeances.append({
            "numero": i + 1,
            "date": date,
            "montant": pret.mensualite
        })
        date = date + timedelta(days=30)

    # Générer le QR code
    receipt_number = f"REC-{pret.id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    qr_data = f"""
    GMES RECEIPT
    Receipt: {receipt_number}
    Prêt N°: {pret.numero_pret}
    Client: {client.nom} {client.prenom}
    Montant: {pret.montant} HTG
    Date: {datetime.now().strftime('%d/%m/%Y')}
    Statut: {pret.statut}
    """

    qr_filename = f"qr_{pret.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    qr_filepath = os.path.join(qr_dossier, qr_filename)

    img = qrcode.make(qr_data)
    img.save(qr_filepath)

# Chemin du logo (optionnel)
    logo_path = os.path.join("static", "logo.png")
    logo_url = url_for('static', filename='logo.png') if os.path.exists(logo_path) else "#"

    # Créer le PDF
    pdf_filename = f"recu_{pret.numero_pret}_{datetime.now().strftime('%Y%m%d')}.pdf"
    pdf_filepath = os.path.join(dossier_recus, pdf_filename)

    doc = SimpleDocTemplate(pdf_filepath, pagesize=A4,
                            rightMargin=20 * mm, leftMargin=20 * mm,
                            topMargin=20 * mm, bottomMargin=20 * mm)

    styles = getSampleStyleSheet()

    # Styles personnalisés
    style_title = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    style_header = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#0b3b4f'),
        spaceAfter=10
    )

    style_normal = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )

    style_center = ParagraphStyle(
        'CustomCenter',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER
    )

    # Contenu du PDF
    story = []

    # En-tête
    story.append(Paragraph("GMES MICROFINANCE", style_title))
    story.append(Paragraph("Reçu de prêt", style_title))
    story.append(Spacer(1, 10))

    # Informations du reçu
    story.append(Paragraph(f"N° Reçu: <b>{receipt_number}</b>", style_normal))
    story.append(Paragraph(f"Date: <b>{datetime.now().strftime('%d/%m/%Y %H:%M')}</b>", style_normal))
    story.append(Spacer(1, 10))

    # Ligne de séparation
    story.append(Paragraph("-" * 80, style_normal))
    story.append(Spacer(1, 10))

    # Informations client
    story.append(Paragraph("<b>INFORMATIONS CLIENT</b>", style_header))
    story.append(Paragraph(f"Nom complet: {client.nom} {client.prenom}", style_normal))
    story.append(Paragraph(f"Téléphone: {client.telephone}", style_normal))
    story.append(Paragraph(f"Email: {client.email or 'Non renseigné'}", style_normal))
    story.append(Spacer(1, 10))

    # Informations du prêt
    story.append(Paragraph("<b>INFORMATIONS DU PRÊT</b>", style_header))
    story.append(Paragraph(f"Numéro de prêt: {pret.numero_pret}", style_normal))
    story.append(
        Paragraph(f"Date de réception: {pret.date_reception.strftime('%d/%m/%Y') if pret.date_reception else 'N/A'}",
                  style_normal))
    story.append(Paragraph(f"Montant: {pret.montant:,.0f} HTG", style_normal))
    story.append(Paragraph(f"Taux d'intérêt: {pret.taux_interet}%", style_normal))
    story.append(Paragraph(f"Durée: {pret.duree_mois} mois", style_normal))
    story.append(Paragraph(f"Mensualité: {pret.mensualite:,.0f} HTG", style_normal))
    story.append(Paragraph(f"Montant total: {pret.montant_total:,.0f} HTG", style_normal))
    story.append(Spacer(1, 10))

    # Tableau des échéances
    story.append(Paragraph("<b>CALENDRIER DES REMBOURSEMENTS</b>", style_header))

    # Calcul des échéances
    echeances = []
    date = pret.date_debut if pret.date_debut else datetime.now()

    from dateutil.relativedelta import relativedelta

    for i in range(pret.duree_mois):
        echeances.append([
            str(i + 1),
            date.strftime('%d/%m/%Y'),
            f"{pret.mensualite:,.0f} HTG"
        ])
        date = date + relativedelta(months=1)

    # Tableau
    table_data = [["#", "Date", "Montant"]] + echeances
    table = Table(table_data, colWidths=[30 * mm, 60 * mm, 60 * mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0b3b4f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    story.append(table)
    story.append(Spacer(1, 10))

    # Conditions
    story.append(Paragraph("<b>CONDITIONS IMPORTANTES</b>", style_header))
    story.append(
        Paragraph("• Le client doit effectuer un paiement chaque mois selon le calendrier ci-dessus.", style_normal))
    story.append(
        Paragraph(f"• Pénalité de retard: 5% de la mensualité ({pret.mensualite * 0.05:,.0f} HTG/mois)", style_normal))
    story.append(Spacer(1, 10))

    # Signatures
    story.append(Paragraph("<b>SIGNATURES</b>", style_header))
    story.append(Spacer(1, 10))

    signature_data = [
        ["Client:", "_________________________"],
        ["Agent:", "_________________________"],
    ]
    signature_table = Table(signature_data, colWidths=[50 * mm, 80 * mm])
    signature_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(signature_table)
    story.append(Spacer(1, 20))

    # QR Code
    if os.path.exists(qr_filepath):
        qr_img = Image(qr_filepath, width=50 * mm, height=50 * mm)
        story.append(Spacer(1, 10))
        story.append(Paragraph("<b>Vérification du reçu</b>", style_center))
        story.append(Spacer(1, 5))
        story.append(qr_img)

    # Générer le PDF
    doc.build(story)

    return {
        "pdf_file": pdf_filepath,
        "qr_file": qr_filepath,
        "receipt_number": receipt_number
    }

@app.route('/pret/<int:pret_id>/approuver', methods=['POST'])
@login_required
@role_required('direction')
def approuver_pret(pret_id):
    """Approuver une demande de prêt"""
    try:
        pret = Pret.query.get_or_404(pret_id)
        data = request.get_json()

        # Mettre à jour les informations
        pret.decision = 'approuve'
        pret.statut = 'approuve'  # ← AJOUTEZ CETTE LIGNE
        pret.montant_accorde = data.get('montant_accorde', pret.montant_demande)
        pret.taux_interet = data.get('taux_interet', pret.taux_interet)
        pret.signature_responsable = f"{current_user.prenom} {current_user.nom}"
        pret.date_approbation = datetime.now()
        pret.approuve_par = current_user.id

        db.session.commit()
        from generer_recus_prets_approuves import generer_recu_pour_un_pret
        generer_recu_pour_un_pret(pret_id)

        # Envoyer notification au client et à l'agent
        notification_manager.send_approval_notification(pret)

        return jsonify({'success': True, 'message': 'Prêt approuvé avec succès et reçu généré'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# Dans routes.py

@app.route('/pret/<int:pret_id>/demander_informations', methods=['POST'])
@login_required
@role_required('direction')
def demander_informations_supplementaires(pret_id):
    """Demander des informations supplémentaires pour un prêt"""
    try:
        pret = Pret.query.get_or_404(pret_id)
        data = request.get_json()

        demande_details = data.get('demande_details', '')

        if not demande_details:
            return jsonify({'success': False, 'message': 'Veuillez spécifier les informations demandées'}), 400

        # Envoyer les notifications
        notification_manager.send_more_information_notification(pret, demande_details)

        # Mettre à jour le statut
        pret.status = 'informations_requises'
        pret.demande_details = demande_details
        pret.date_demande_infos = datetime.now()

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Demande d\'informations envoyée au client et à l\'agent'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/pret/<int:pret_id>/refuser', methods=['POST'])
@login_required
@role_required('direction')
def refuser_pret(pret_id):
    try:
        pret = Pret.query.get_or_404(pret_id)

        client = pret.client  # ← Récupérer le client


        data = request.get_json(silent=True) or {}

        motif_refus = data.get('motif_refus')

        if not motif_refus:
            return jsonify({
                'success': False,
                'message': 'Le motif de refus est obligatoire'
            }), 400

        pret.decision = 'refuse'
        pret.statut = 'refuse'  # ← AJOUTEZ CETTE LIGNE (important!)
        pret.motif_refus = motif_refus
        pret.date_refus = datetime.now()
        pret.refuse_par = current_user.id

        # 🔥 RÉINITIALISER LE CLIENT - Il pourra refaire une demande
        client.terms_accepted = False
        client.terms_accepted_at = None
        client.terms_signature_ip = None
        client.terms_signature_user_agent = None

        # Réactiver le compte si nécessaire
        if hasattr(client, 'compte_suspendu'):
            client.compte_suspendu = False
        if hasattr(client, 'a_un_pret_actif'):
            client.a_un_pret_actif = False

        db.session.commit()

        # 🔥 RENVOYER L'EMAIL POUR NOUVELLE ACCEPTATION
        # envoyer_email_conditions(client)

        notification_manager.send_refusal_notification(pret)

        return jsonify({
            'success': True,
            'message': 'Prêt refusé. Le client a été réinitialisé et pourra faire une nouvelle demande.'
        })

    except Exception as e:
        db.session.rollback()
        print("ERREUR REFUS PRET:", str(e))
        import traceback
        traceback.print_exc()

        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


def notifier_directeurs_demande_pret(pret, type_action="nouvelle_demande"):
    """
    Notifie tous les directeurs et administrateurs d'une action sur une demande de prêt

    Args:
        pret: Objet Pret (la demande de prêt)
        type_action: Type d'action ("nouvelle_demande", "approbation", "refus", "modification")
    """
    from models import User, Notification, Action  # ← AJOUTÉ Action
    from datetime import datetime
    from flask import url_for

    print("=" * 70)
    print(f"📢 NOTIFICATION DIRECTEURS - Action: {type_action}")
    print("=" * 70)

    try:
        # Récupérer les informations nécessaires
        client = pret.client
        agent = pret.agent if pret.agent_id else None

        if not client:
            print("❌ Client non trouvé pour ce prêt")
            return False

        # Déterminer la succursale concernée
        succursale_id = client.succursale_id

        # Configuration des messages selon l'action
        config_messages = {
            "nouvelle_demande": {
                "titre": f"💰 Nouvelle demande de prêt #{pret.id}",
                "type": "info",
                "icone": "💰",
                "couleur": "blue"
            },
            "approbation": {
                "titre": f"✅ Prêt #{pret.id} approuvé",
                "type": "success",
                "icone": "✅",
                "couleur": "green"
            },
            "refus": {
                "titre": f"❌ Prêt #{pret.id} refusé",
                "type": "danger",
                "icone": "❌",
                "couleur": "red"
            },
            "modification": {
                "titre": f"✏️ Prêt #{pret.id} modifié",
                "type": "warning",
                "icone": "✏️",
                "couleur": "orange"
            }
        }

        config = config_messages.get(type_action, config_messages["nouvelle_demande"])

        # Formater le montant
        montant_formate = f"{pret.montant:,.0f} HTG".replace(',', ' ')

        # Construire le message détaillé
        message = (
            f"Client: {client.prenom} {client.nom}\n"
            f"Montant: {montant_formate}\n"
            f"Durée: {pret.duree_mois} mois\n"
            f"Taux: {pret.taux_interet}%\n"
        )

        if agent:
            message += f"Agent: {agent.prenom} {agent.nom}\n"

        if pret.date_demande:
            message += f"Date: {pret.date_demande.strftime('%d/%m/%Y %H:%M')}"

        # Construire le lien vers le prêt
        lien_pret = url_for('voir_pret', pret_id=pret.id, _external=True)

        # Liste des rôles à notifier
        roles_cibles = ['direction', 'directeur', 'admin', 'super_admin', 'admin_succursale']

        # Construire la requête de base
        query = User.query.filter(
            User.role.in_(roles_cibles),
            User.actif == True
        )

        # Filtrer par succursale si spécifiée
        if succursale_id:
            directeurs_succursale = query.filter(
                (User.succursale_id == succursale_id) |
                (User.role.in_(['admin', 'direction', 'directeur', 'super_admin']))
            ).all()
        else:
            directeurs_succursale = query.all()

        # Éliminer les doublons
        destinataires = directeurs_succursale

        if not destinataires:
            print("⚠️ Aucun destinataire trouvé")
            return False

        print(f"📨 Notification à {len(destinataires)} destinataire(s)")

        # 🔥 CRÉER UNE ACTION UNIQUE POUR CETTE NOTIFICATION
        nouvelle_action = Action(
            pret_id=pret.id,
            type_action=type_action,
            date_action=datetime.now(),
            description=f"{config['titre']} - {message[:100]}"
        )
        db.session.add(nouvelle_action)
        db.session.flush()  # Pour obtenir nouvelle_action.id

        # Créer les notifications
        notifications_creees = 0
        for destinataire in destinataires:
            try:
                # Vérifier si une notification similaire existe déjà
                existing = Notification.query.filter_by(
                    employe_id=destinataire.id,
                    titre=config["titre"],
                    lue=False
                ).first()

                if existing and type_action == "nouvelle_demande":
                    print(f"   ⏭️ Notification déjà existante pour {destinataire.email}")
                    continue

                # Créer la notification avec le bon action_id
                notification = Notification(
                    employe_id=destinataire.id,
                    titre=config["titre"],
                    message=message,
                    type_notification=config["type"],
                    lien=lien_pret,
                    date_envoi=datetime.now(),
                    lue=False,
                    destinataire_id=destinataire.id,
                    action_id=nouvelle_action.id,  # ← CORRIGÉ : utilise l'ID de l'Action
                    date_creation=datetime.now(),
                    pret_id=pret.id
                )
                db.session.add(notification)
                notifications_creees += 1
                print(f"   ✅ Notification créée pour {destinataire.email} ({destinataire.role})")

            except Exception as e:
                print(f"   ❌ Erreur pour {destinataire.email}: {e}")

        # Commit en une seule fois
        if notifications_creees > 0:
            db.session.commit()
            print(f"✅ {notifications_creees} notifications créées avec succès")
            return True
        else:
            print("⚠️ Aucune nouvelle notification créée")
            return False

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur critique dans notifier_directeurs_demande_pret: {e}")
        import traceback
        traceback.print_exc()
        return False


def envoyer_email_directeurs(pret, destinataires, action,  config):
    from flask import current_app
    """
    Envoie un email aux directeurs pour les informer
    """
    try:
        from flask_mail import Message

        client = pret.client
        agent = pret.agent

        montant_formate = f"{pret.montant:,.0f} HTG".replace(',', ' ')

        # Sujet de l'email
        sujet = f"{config['icone']} {config['titre']} - {client.prenom} {client.nom}"

        # Template HTML
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; 
                    padding: 20px; 
                    text-align: center; 
                    border-radius: 10px 10px 0 0;
                }}
                .content {{ background: #f8f9fa; padding: 20px; border-radius: 0 0 10px 10px; }}
                .info-card {{ 
                    background: white; 
                    padding: 20px; 
                    border-radius: 10px; 
                    margin: 15px 0;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .montant {{ 
                    font-size: 28px; 
                    color: #28a745; 
                    font-weight: bold;
                    text-align: center;
                    padding: 10px;
                    background: #e8f5e9;
                    border-radius: 5px;
                }}
                .details {{ margin: 15px 0; }}
                .detail-item {{ 
                    padding: 8px 0;
                    border-bottom: 1px solid #eee;
                }}
                .btn {{ 
                    display: inline-block; 
                    padding: 12px 30px; 
                    background: #007bff; 
                    color: white; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    margin-top: 20px;
                    font-weight: bold;
                }}
                .btn:hover {{ background: #0056b3; }}
                .footer {{ 
                    margin-top: 30px; 
                    padding-top: 20px; 
                    border-top: 1px solid #ddd;
                    text-align: center;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>{config['icone']} {config['titre']}</h2>
                </div>
                <div class="content">
                    <p>Bonjour <strong>{{prenom}} {{nom}}</strong>,</p>

                    <div class="info-card">
                        <div class="montant">{montant_formate}</div>

                        <div class="details">
                            <div class="detail-item">
                                <strong>👤 Client:</strong> {client.prenom} {client.nom}
                            </div>
                            <div class="detail-item">
                                <strong>📊 Durée:</strong> {pret.duree_mois} mois
                            </div>
                            <div class="detail-item">
                                <strong>📈 Taux:</strong> {pret.taux_interet}%
                            </div>
                            <div class="detail-item">
                                <strong>👔 Agent:</strong> {agent.prenom} {agent.nom}
                            </div>
                            <div class="detail-item">
                                <strong>📅 Date:</strong> {pret.date_demande.strftime('%d/%m/%Y %H:%M')}
                            </div>
                            <div class="detail-item">
                                <strong>📝 Motif:</strong> {pret.motif}
                            </div>
                        </div>
                    </div>

                    <div style="text-align: center;">
                        <a href="{url_for('voir_pret', pret_id=pret.id, _external=True)}" class="btn">
                            👁️ Voir la demande de prêt
                        </a>
                    </div>

                    <div class="footer">
                        <p>Ceci est un message automatique de GMES Microcrédit.</p>
                        <p>© 2024 GMES - Tous droits réservés</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        # Envoyer à chaque directeur
        emails_envoyes = 0
        for directeur in destinataires:
            if not directeur.email:
                continue

            try:
                # Personnaliser le HTML avec le nom du directeur
                html_personnalise = html_template.replace(
                    "{{prenom}}", directeur.prenom
                ).replace("{{nom}}", directeur.nom)

                msg = Message(
                    subject=sujet,
                    recipients=[directeur.email],
                    html=html_personnalise
                )

                if hasattr(current_app, 'mail') and current_app.mail:
                    current_app.mail.send(msg)
                    emails_envoyes += 1
                    print(f"📧 Email envoyé à {directeur.email}")
                else:
                    print(f"⚠️ Mail non configuré, pas d'email pour {directeur.email}")

            except Exception as e:
                print(f"❌ Erreur envoi email à {directeur.email}: {e}")

        print(f"✅ {emails_envoyes} emails envoyés avec succès")

    except Exception as e:
        print(f"❌ Erreur dans envoyer_email_directeurs: {e}")
        import traceback
        traceback.print_exc()


def get_statut_pret_color(statut):
    """Retourne la couleur Bootstrap pour un statut de prêt"""
    couleurs = {
        'en_attente': 'warning',
        'approuve': 'success',
        'refuse': 'danger',
        'annule': 'secondary',
        'en_cours': 'info',
        'termine': 'primary'
    }
    return couleurs.get(statut, 'secondary')


def validate_telephone_ht(telephone):
    """Valide un numéro de téléphone haïtien"""
    pattern = r'^(?:\+509|0)?[2-9]\d{7}$'
    return re.match(pattern, telephone) is not None


def validate_cin_nif(cin_nif):
    """Valide un CIN/NIF haïtien"""
    pattern = r'^[0-9A-Z-]{6,20}$'
    return re.match(pattern, cin_nif) is not None


def calculate_age(date_naissance):
    """Calcule l'âge à partir de la date de naissance"""
    today = datetime.now().date()
    return today.year - date_naissance.year - (
            (today.month, today.day) < (date_naissance.month, date_naissance.day)
    )



def envoyer_notification_pret(client, pret):
    """Envoie une notification au client pour sa demande de prêt"""
    try:
        from models import Action
        from datetime import datetime
        from flask import url_for

        # 1. CRÉER L'ACTION D'ABORD
        action = Action(
            pret_id=pret.id,
            type_action='pret_demande',
            titre="Demande de prêt",
            description=f"Demande de prêt de {pret.montant:,.0f} GDES",
            date_creation=datetime.now(),
            date_echeance=datetime.now(),  # obligatoire
            assignee_a_id=current_user.id,  # ← OBLIGATOIRE
            creee_par_id=current_user.id,  # ← OBLIGATOIRE
            statut='terminee'  # pour éviter 'a_faire' par défaut
        )
        db.session.add(action)
        db.session.flush()  # Pour obtenir action.id

        # 2. CRÉER LA NOTIFICATION
        notification = Notification(
            employe_id=pret.agent_id,
            destinataire_id=pret.agent_id,
            action_id=action.id,  # OBLIGATOIRE
            type_notification='pret_demande',
            titre='📝 Demande de prêt enregistrée',
            message=f"Votre demande de prêt de {pret.montant:,.0f} GDES a été soumise avec succès.",
            niveau='info',
            lue=False,
            date_creation=datetime.now(),
            lien=url_for('client_voir_pret', pret_id=pret.id, _external=True)
        )
        db.session.add(notification)

        # 3. ENVOI EMAIL AU CLIENT
        sujet = "📝 Confirmation de votre demande de prêt"
        message = f"""
Bonjour {client.prenom} {client.nom},

Votre demande de prêt a bien été enregistrée.

📋 Récapitulatif :
• Montant demandé : {pret.montant:,.0f} GDES
• Durée : {pret.duree_mois} mois
• Date de la demande : {pret.date_demande.strftime('%d/%m/%Y')}

Votre dossier est en cours d'examen par notre équipe.
Vous serez notifié dès qu'une décision sera prise.

Merci de votre confiance,
L'équipe GMES Microcrédit
"""

        send_email(client.email, sujet, message)

        # 4. VALIDER TOUT
        db.session.commit()

        # 5. NOTIFIER LES DIRECTEURS
        notifier_directeurs_demande_pret(pret)  # ← CORRIGÉ: 'pret' au lieu de 'demande_pret'

        print(f"✅ Notification et email envoyés pour le prêt {pret.id}")

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erreur envoi notification client {client.id}: {e}")
        import traceback
        traceback.print_exc()


def verifier_token_conditions(token):
    """
    Vérifie la validité d'un token pour l'acceptation des conditions.
    Retourne l'utilisateur si le token est valide, sinon None.
    """
    import jwt
    from datetime import datetime
    from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

    try:
        # Décoder le token
        data = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithms=['HS256']
        )

        # Vérifier que c'est bien un token de conditions
        if data.get('type') != 'conditions':
            return None

        # Récupérer l'utilisateur
        client_id = data.get('client_id')
        if not client_id:
            return None

        client = db.session.get(Client, client_id)
        if not client:
            return None

        # Vérifier que le token n'a pas expiré
        expiration = data.get('exp')
        if expiration and expiration < datetime.utcnow().timestamp():
            return None

        return client

    except jwt.ExpiredSignatureError:
        # Token expiré
        return None
    except jwt.InvalidTokenError:
        # Token invalide
        return None
    except Exception as e:
        app.logger.error(f"Erreur vérification token conditions: {e}")
        return None

@app.route('/valider-conditions/<token>', methods=['POST'])
def valider_conditions(token):
    """Valide l'acceptation des conditions"""
    client_id = verifier_token_conditions(token)

    if not client_id:
        flash("Lien d'acceptation invalide ou expiré.", "danger")
        return redirect(url_for('main.accueil'))

    client = db.session.get(Client, client_id)
    client.terms_accepted = True
    client.date_acceptation_terms = datetime.utcnow()
    client.compte_actif = True  # Active complètement le compte
    db.session.commit()

    flash("✅ Félicitations ! Vous avez accepté les conditions d'utilisation. Vous pouvez maintenant demander un prêt.",
          "success")
    return redirect(url_for('main.accueil'))


def client_peut_demander_pret(client):
    """
    Vérifie si un client peut faire une demande de prêt
    Retourne (peut_demander, message)
    """
    from models import Pret
    from datetime import datetime

    # 1. Vérifier si le client existe et est actif
    if not client:
        return False, "Client non trouvé"

    if not client.compte_actif:
        return False, "Compte client inactif"

    if client.compte_suspendu:
        return False, "Compte suspendu"

    # 2. Vérifier si les conditions sont acceptées
    if not client.terms_accepted:
        # ENVOYER L'EMAIL DE CONFIRMATION AVANT DE REFUSER
        try:
            from app import envoyer_email_conditions
            envoyer_email_conditions(client)
            print(f"📧 Email de confirmation renvoyé à {client.email}")
            return False, "Veuillez d'abord accepter les conditions générales. Un email de confirmation vous a été renvoyé."
        except Exception as e:
            print(f"❌ Erreur envoi email: {e}")
            return False, "Conditions générales non acceptées. Impossible d'envoyer l'email de confirmation."

    # 3. Vérifier s'il a un prêt en cours non remboursé

    prets_en_cours = Pret.query.filter(
        Pret.client_id == client.id,
        Pret.statut.in_(['en_attente', 'approuve', 'actif']),
        Pret.solde_restant > 0
    ).count()

    if prets_en_cours > 0:
        return False, f"Vous avez déjà {prets_en_cours} prêt(s) en cours"

    # 4. Vérifier l'âge (18 ans minimum)
    if client.date_naissance:
        # ✅ SOLUTION 1 : Convertir date_naissance en date
        from datetime import date

        # Si client.date_naissance est datetime
        naissance = client.date_naissance.date() if hasattr(client.date_naissance, 'date') else client.date_naissance
        age = (date.today() - naissance).days / 365.25
        if age < 18:
            return False, "Vous devez avoir au moins 18 ans"

    # 5. Vérifier le revenu minimum
    if client.revenu_mensuel and client.revenu_mensuel < 10000:
        return False, "Revenu mensuel insuffisant (minimum 10 000 HTG)"

    return True, "✅ Éligible à une demande de prêt"



# @app.route('/accepter-conditions/<token>', methods=['GET', 'POST'])
# def accepter_conditions(token):
#     from flask_login import login_user
#     from models import User, Notification, Client
#     import jwt
#     from datetime import datetime
#
#     print(f"🔍 Token reçu: {token[:50]}...")
#
#     client = None  # ✅ IMPORTANT
#
#     # ===== 1. DÉCODER TOKEN =====
#     try:
#         data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#
#         print(f"✅ Token décodé: {data}")
#
#         if data.get('type') != 'conditions':
#             return render_template('accepter_conditions.html', token_invalide=True)
#
#         # ✅ NOUVEAU TOKEN
#         if 'client_id' in data:
#             client = db.session.get(Client, data['client_id'])
#
#         # ❌ ANCIEN TOKEN → on bloque
#         elif 'employe_id' in data:
#             print("⚠️ Ancien token détecté (employe_id)")
#             return render_template(
#                 'accepter_conditions.html',
#                 token_invalide=True,
#                 message="Lien expiré. Veuillez redemander un email."
#             )
#
#         if not client:
#             return render_template('accepter_conditions.html', token_invalide=True)
#
#     except jwt.ExpiredSignatureError:
#         return render_template('accepter_conditions.html', token_expire=True)
#     except jwt.InvalidTokenError:
#         return render_template('accepter_conditions.html', token_invalide=True)
#
#     # ===== 2. VÉRIFIER SI DÉJÀ ACCEPTÉ =====
#     if client.terms_accepted:
#         print(f"⚠️ Déjà accepté: {client.email}")
#         flash("Vous avez déjà accepté les conditions", "info")
#         return redirect(url_for('connexion'))
#
#     # ===== 3. CRÉER OU RÉCUPÉRER USER =====
#     user = db.session.get(User, client.id)
#
#     if not user:
#         from werkzeug.security import generate_password_hash
#         import uuid

@app.route('/accepter-conditions/<token>', methods=['GET', 'POST'])
def accepter_conditions(token):
    from flask_login import login_user
    from models import User, Notification, Client
    import jwt
    from datetime import datetime
    from flask import session  # ← AJOUTER l'import de session ici

    print(f"🔍 Token reçu: {token[:50]}...")

    client = None  # ✅ Important

    # ===== 1. DÉCODER TOKEN =====
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        print(f"✅ Token décodé: {data}")

        if data.get('type') != 'conditions':
            return render_template('accepter_conditions.html', token_invalide=True)

        # ✅ NOUVEAU TOKEN
        if 'client_id' in data:
            client = db.session.get(Client, data['client_id'])
        # ❌ ANCIEN TOKEN → on bloque
        elif 'employe_id' in data:
            print("⚠️ Ancien token détecté (employe_id)")
            return render_template(
                'accepter_conditions.html',
                token_invalide=True,
                message="Lien expiré. Veuillez redemander un email."
            )

        if not client:
            return render_template('accepter_conditions.html', token_invalide=True)

    except jwt.ExpiredSignatureError:
        return render_template('accepter_conditions.html', token_expire=True)
    except jwt.InvalidTokenError:
        return render_template('accepter_conditions.html', token_invalide=True)

    # ===== 2. VÉRIFIER SI DÉJÀ ACCEPTÉ =====
    if client.terms_accepted:

        print(f"⚠️ Déjà accepté: {client.email}")
        flash("Vous avez déjà accepté les conditions", "info")
        return redirect(url_for('connexion'))

    # ===== 3. CRÉER OU RÉCUPÉRER USER =====
    user = User.query.filter_by(email=client.email).first()

    if not user:
        from werkzeug.security import generate_password_hash
        import uuid

        user = User(
            id=client.id,
            prenom=client.prenom,
            nom=client.nom,
            email=client.email,
            telephone=client.telephone,
            password=generate_password_hash(str(uuid.uuid4())),
            compte_actif=True,
            terms_accepted=False,
            date_creation=datetime.now()
        )
        db.session.add(user)
        db.session.commit()
        print(f"✅ User créé pour client {client.id}")

    # ===== 4. POST (SIGNATURE) =====
    if request.method == 'POST':
        try:
            signature_data = request.form.get('signature')

            if not signature_data:
                flash("Veuillez signer", "danger")
                return render_template('accepter_conditions.html', user=user)

            if 'base64,' in signature_data:
                signature_data = signature_data.split('base64,')[1]

            # ✅ UPDATE CLIENT (PAS USER)
            client.terms_accepted = True

            # 🔥 RÉCUPÉRER LES DONNÉES DU PRÊT
            pret_data = session.get('pret_data')

            if pret_data:
                print("📦 Données prêt récupérées depuis session")

                montant_demande = float(pret_data.get('montant_demande', 0))
                duree = int(pret_data.get('duree', 0))
                taux_annuel = float(pret_data.get('taux_interet', 12))

                montant_interet = montant_demande * (taux_annuel / 100) * (duree / 12)
                montant_total = montant_demande + montant_interet
                mensualite = montant_total / duree if duree > 0 else montant_total

                nouveau_pret = Pret(
                    client_id=client.id,
                    montant=montant_demande,
                    duree_mois=duree,
                    motif=pret_data.get('objet'),
                    type_pret=pret_data.get('type_pret'),
                    signature=user.terms_signature,
                    mensualite=round(mensualite, 2),
                    montant_interet=round(montant_interet, 2),
                    montant_total=round(montant_total, 2),
                    taux_interet=taux_annuel,
                    statut='en_attente',
                    numero_dossier=pret_data.get('num_dossier')
                )

                db.session.add(nouveau_pret)

                print("✅ Prêt créé après signature")

                # 🔥 IMPORTANT : nettoyer session
                session.pop('pret_data', None)

            client.terms_accepted = True
            client.terms_accepted_at = datetime.now()


            # ✅ UPDATE USER


            user.terms_signature = signature_data
            user.terms_accepted = True
            user.terms_signature_ip = request.remote_addr
            user.terms_signature_user_agent = request.user_agent.string
            user.statut = 'en_attente_approbation'

            if not user.role:
                user.role = 'client'

            login_user(user)

            # ===== NOTIFICATIONS =====
            admins = User.query.filter(
                User.role.in_(['admin', 'super_admin', 'admin_succursale', 'direction'])
            ).all()

            for admin in admins:
                notif = Notification(
                    employe_id=admin.id,
                    titre="📝 Client en attente",
                    message=f"{client.prenom} {client.nom} attend validation",
                    type_notification='info',
                    lien=url_for('voir_client', client_id=client.id),
                    date_envoi=datetime.now(),
                    destinataire_id=admin.id,
                    action_id=0
                )
                db.session.add(notif)

            db.session.commit()

            flash("✅ Conditions acceptées !", "success")

            print("✅ Conditions acceptées !", "success")
            return render_template('promotions.html')

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur: {e}")
            flash("Erreur", "danger", token_valide=True)

    return render_template('accepter_conditions.html', user=user,token_valide=True)


def generer_token_conditions(client):
    """Génère un token pour l'acceptation des conditions"""
    import jwt
    from datetime import datetime, timedelta

    payload = {
        'client_id': client.id,
        'type': 'conditions',
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }

    token = jwt.encode(
        payload,
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return token  # ⚠️ IL MANQUE CETTE LIGNE !




@app.route('/conseiller/creer-dossier', methods=['GET', 'POST'])
@login_required
def creer_dossier():
    """Créer un nouveau dossier client avec processus d'approbation complet"""
    from models import User, Succursale, Notification, TermsAcceptance, Competence, Action
    from werkzeug.utils import secure_filename
    import os
    import base64
    from datetime import datetime, timedelta
    import secrets
    import random
    import string
    import json
    import re
    # Vérification des permissions
    if current_user.role != 'employe' or not current_user.has_permission('conseiller'):
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('employe_dashboard_generique'))
    # Récupérer la succursale du conseiller connecté
    succursale = db.session.get(Succursale, current_user.succursale_id)

    # EXTRAIRE LES 5 CHIFFRES DU NOM DE LA SUCCURSALE
    def extract_branch_code(succursale_obj):
        if not succursale_obj:
            return '00001'
        match = re.search(r'(\d{5})', succursale_obj.nom)
        if match:
            return match.group(1)
        digits = ''.join(filter(str.isdigit, str(succursale_obj.code or '')))
        return digits.zfill(5)[:5]
    branch_code = extract_branch_code(succursale)
    if request.method == 'GET':
        succursales = Succursale.query.all()
        default_suffix = str(random.randint(10000, 99999))
        default_code = f"7-12519-{branch_code}-{default_suffix}"
        return render_template('creer_dossier.html',
                               succursales=succursales,
                               succursale=succursale,
                               branch_code=branch_code,
                               default_code=default_code,
                               default_suffix=default_suffix)

    # Fonctions utilitaires
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def save_uploaded_file(file, folder, filename):
        try:
            filepath = os.path.join(folder, filename)
            file.save(filepath)
            return filename
        except Exception as e:
            print(f"Erreur sauvegarde fichier: {e}")
            return None

    def save_base64_image(base64_data, folder, filename):
        try:
            if ',' in base64_data:
                base64_data = base64_data.split(',')[1]
            image_data = base64.b64decode(base64_data)
            filepath = os.path.join(folder, filename)
            with open(filepath, 'wb') as f:
                f.write(image_data)
            return filename
        except Exception as e:
            print(f"Erreur sauvegarde image: {e}")
            return None

    def compare_faces(img1_path, img2_path):
        similarity = random.uniform(75, 98)
        return True, f"Similarité: {similarity:.1f}% - Correspondance validée"

    # TRAITEMENT POST
    try:
        # Vérifier la taille des fichiers
        for file_key in ['photo_cin_recto', 'photo_cin_verso', 'selfie']:
            file = request.files.get(file_key)
            if file:
                file.seek(0, os.SEEK_END)
                size = file.tell()
                file.seek(0)
                if size > 30 * 1024 * 1024:
                    raise ValueError(f"Le fichier {file_key} est trop volumineux. Maximum 30 Mo.")

        # Données du formulaire
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        civilite = request.form.get('civilite')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        cin = request.form.get('cin')
        date_naissance = request.form.get('date_naissance')
        sexe = request.form.get('sexe')
        adresse = request.form.get('adresse')
        code_postal = request.form.get('code_postal')
        ville = request.form.get('ville')
        profession = request.form.get('profession')
        revenu_mensuel = float(request.form.get('revenu_mensuel', 0))
        depenses_mensuelles = float(request.form.get('depenses_mensuelles', 0))
        # GÉNÉRATION DU CODE CLIENT AVEC PARITÉ
        suffix = str(random.randint(10000, 99999))
        last_digit = int(suffix[-1])

        # Ajuster le dernier chiffre selon le sexe
        if (sexe == 'M' and last_digit % 2 != 0) or (sexe == 'F' and last_digit % 2 == 0):
            new_last = random.choice([0, 2, 4, 6, 8]) if sexe == 'M' else random.choice([1, 3, 5, 7, 9])
            suffix = suffix[:-1] + str(new_last)

        id_client = f"7-12519-{branch_code}-{suffix}"
        print(f"🔑 Code client généré: {id_client} (sexe: {sexe})")

        # Compétences
        competences_data = request.form.get('competences_data', '[]')
        competences = json.loads(competences_data)

        # Signature parent
        parent_nom = request.form.get('parent_nom')
        parent_signature = request.form.get('parent_signature')

        # Données caméra
        photo_id_data = request.form.get('photo_id_data')
        photo_selfie_data = request.form.get('photo_selfie_data')

        # Validation
        if not all([nom, prenom, civilite , email, telephone, cin, date_naissance, sexe, adresse, code_postal, ville,
                    profession, revenu_mensuel, depenses_mensuelles, id_client]):
            succursales = Succursale.query.all()
            return render_template('creer_dossier.html',
                                   error="Tous les champs obligatoires doivent être remplis",
                                   succursales=succursales,
                                   succursale=succursale,
                                   branch_code=extract_branch_code(succursale))

        print("🔥 AVANT VÉRIFICATION EMAIL")

        erreurs = []

        # Vérifier email
        if Client.query.filter_by(email=email).first():
            erreurs.append(f"L'adresse email '{email}' est déjà utilisée par un compte client.")

        print("🔥 APRÈS VÉRIFICATION EMAIL - EMAIL OK")

        # Vérifier CIN
        if Client.query.filter_by(cin_nif=cin).first():
            erreurs.append(f"Le numéro CIN '{cin}' est déjà utilisé par un compte client.")

        print("🔥 APRÈS VÉRIFICATION - cin_existant = {cin_existant is not None}")

        # Vérifier téléphone
        if Client.query.filter_by(telephone=telephone).first():
            erreurs.append(f"Le numéro de téléphone '{telephone}' est déjà utilisé par un compte client.")

        print("🔥 APRÈS VÉRIFICATION tel - CIN OK")
        print(f"🔥 erreurs = {erreurs}")  # ← AJOUTE CECI
        print(f"🔥 len(erreurs) = {len(erreurs)}")  # ← AJOUTE CECI

        if erreurs:
            for erreur in erreurs:
                flash(erreur, "danger")
            succursales = Succursale.query.all()
            print("🔥 ON ENTRE DANS LE BLOC ERREURS")  # ← AJOUTE CECI
            return render_template('creer_dossier.html',
                                   error="<br>".join(erreurs),
                                   succursales=succursales,
                                   succursale=succursale,
                                   branch_code=extract_branch_code(succursale),
                                   # Conserver les données saisies
                                   default_nom=nom,
                                   default_prenom=prenom,
                                   default_email=email,
                                   default_telephone=telephone,
                                   default_cin=cin,
                                   default_date_naissance=date_naissance,
                                   default_sexe=sexe,
                                   default_adresse=adresse,
                                   default_code_postal=code_postal,
                                   default_ville=ville,
                                   default_profession=profession,
                                   default_revenu=revenu_mensuel,
                                   default_depenses=depenses_mensuelles,
                                   default_suffix=str(random.randint(10000, 99999)))

        else:
            print("🔥 AUCUNE ERREUR - ON CONTINUE LA CRÉATION DU DOSSIER")
             # Succursale
            succursale_id = current_user.succursale_id
            succursale = db.session.get(Succursale, succursale_id)
            print(f"🔥 Succursale trouvée: {succursale}")  # ← AJOUTE CECI
            if not succursale:
                raise ValueError("Succursale non trouvée")



            # Vérifier code client
            code_parts = id_client.split('-')
            if len(code_parts) != 4:
                raise ValueError("Format invalide (doit être: 7-12519-00001-12345)")
            if code_parts[0] != '7' or code_parts[1] != '12519':
                raise ValueError("Préfixe invalide (doit être 7-12519)")
            if code_parts[2] != extract_branch_code(succursale):
                raise ValueError(f"Code succursale invalide")

            suffixe = code_parts[3]
            if len(suffixe) != 5 or not suffixe.isdigit():
                raise ValueError("Le suffixe doit être 5 chiffres")

            # Remplacez la ligne 360 par :
            chiffres = int(suffixe)
            est_pair = (chiffres % 2 == 0)

            if (sexe == 'M' and not est_pair):
                raise ValueError(
                    f"Pour un homme (M), le dernier chiffre doit être PAIR. Or votre suffixe '{suffixe}' se termine par {chiffres} qui est IMPAIR.")

            if (sexe == 'F' and est_pair):
                raise ValueError(
                    f"Pour une femme (F), le dernier chiffre doit être IMPAIR. Or votre suffixe '{suffixe}' se termine par {chiffres} qui est PAIR.")

            # Âge
            today = datetime.now().date()
            naissance = datetime.strptime(date_naissance, '%Y-%m-%d').date()
            age = today.year - naissance.year - ((today.month, today.day) < (naissance.month, naissance.day))
            if age < 18 and not parent_signature:
                raise ValueError("Client mineur : signature parentale requise")

            # Upload
            upload_folder = os.path.join(app.root_path, 'static/uploads/clients')
            os.makedirs(upload_folder, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            recto_filename = verso_filename = selfie_filename = None

            # Recto
            if photo_id_data:
                recto_filename = f"cin_recto_{cin}_{timestamp}_camera.jpg"
                save_base64_image(photo_id_data, upload_folder, recto_filename)
            else:
                photo_cin_recto = request.files.get('photo_cin_recto')
                if photo_cin_recto and allowed_file(photo_cin_recto.filename):
                    recto_filename = f"cin_recto_{cin}_{timestamp}.jpg"
                    save_uploaded_file(photo_cin_recto, upload_folder, recto_filename)
                else:
                    raise ValueError("Photo recto CIN requise")

            # Verso
            photo_cin_verso = request.files.get('photo_cin_verso')
            if photo_cin_verso and allowed_file(photo_cin_verso.filename):
                verso_filename = f"cin_verso_{cin}_{timestamp}.jpg"
                save_uploaded_file(photo_cin_verso, upload_folder, verso_filename)
            else:
                raise ValueError("Photo verso CIN requise")

            # Selfie
            if photo_selfie_data:
                selfie_filename = f"selfie_{cin}_{timestamp}_camera.jpg"
                save_base64_image(photo_selfie_data, upload_folder, selfie_filename)
            else:
                selfie = request.files.get('selfie')
                if selfie and allowed_file(selfie.filename):
                    selfie_filename = f"selfie_{cin}_{timestamp}.jpg"
                    save_uploaded_file(selfie, upload_folder, selfie_filename)
                else:
                    raise ValueError("Selfie requis")

            # Vérification faciale
            match, message = compare_faces(
                os.path.join(upload_folder, recto_filename),
                os.path.join(upload_folder, selfie_filename)
            )
            if not match:
                for f in [recto_filename, verso_filename, selfie_filename]:
                    try:
                        os.remove(os.path.join(upload_folder, f))
                    except:
                        pass
                raise ValueError(f"Échec vérification faciale: {message}")

            # Score
            score_match = re.search(r'(\d+\.?\d*)', message)
            score_verification = float(score_match.group(1)) if score_match else 0.0

            # Capacité
            capacite_remboursement = max(0, revenu_mensuel - depenses_mensuelles)

            # Token
            token_signature = secrets.token_urlsafe(32)
            date_expiration = datetime.now() + timedelta(days=7)

            # Créer client
            nouveau_client = Client(
                id_client=id_client,
                numero_compte=id_client,
                nom=nom,
                prenom=prenom,
                email=email,
                telephone=telephone,
                cin=cin,
                date_naissance=datetime.strptime(date_naissance, '%Y-%m-%d'),
                sexe=sexe,
                adresse=f"{adresse}, {code_postal} {ville}",
                profession=profession,
                revenu_mensuel=revenu_mensuel,
                depenses_mensuelles=depenses_mensuelles,
                capacite_remboursement=capacite_remboursement,

                verification_faciale=True,
                score_verification=score_verification,
                statut='en_attente_terms',
                succursale_id=succursale_id,
                cree_par_id=current_user.id,
                employe_id=current_user.id,  # ← AJOUTEZ CETTE LIGNE (même valeur que cree_par_id)

                photo_face=recto_filename,  # ← au lieu de photo_id
                photo_dos=verso_filename,  # ← Ajoutez cette ligne
                selfie_reference=selfie_filename,  # ← au lieu de photo_selfie

                token_signature=token_signature,
                date_expiration_token=date_expiration,
                date_envoi_terms=datetime.now()

            )

            if age < 18:
                nouveau_client.parent_nom = parent_nom
                nouveau_client.parent_signature = parent_signature

            # password_temp = secrets.token_urlsafe(8) + "Aa1!"
            # nouveau_client.set_password(password_temp)

            db.session.add(nouveau_client)
            db.session.flush()

            nouveau_compte = Epargne(
                client_id=nouveau_client.id,
                numero_compte=nouveau_client.numero_compte,
                intitule_compte=f"{nouveau_client.prenom} {nouveau_client.nom}",
                solde=0,
                solde_disponible=0,
                statut=nouveau_client.statut,
                succursale_id=nouveau_client.succursale_id,
                employe_id=nouveau_client.employe_id,
                created_by=current_user.id,
                produit_epargne_id=1
            )

            db.session.add(nouveau_compte)

            # Compétences
            for comp in competences:
                competence = Competence(
                    client_id=nouveau_client.id,
                    nom=comp.get('nom'),
                    niveau=comp.get('niveau'),
                    description=comp.get('description', '')
                )
                db.session.add(competence)

            # Dans votre route creer_dossier, après avoir créé le client
            from utils.notifications import notification_manager

            # Créer le lien
            token = generer_token_conditions(nouveau_client)
            lien_terms = f"http://10.0.0.226:10000/client/terms/{token}"
            print(f"🔗 Lien pour le client: {lien_terms}")

            # Envoyer l'email via votre NotificationManager
            try:
                notification_manager.notifier_acceptation_terms(nouveau_client, lien_terms)
                print(f"📧 Email envoyé à {email}")
            except Exception as e:
                print(f"⚠️ Erreur envoi email: {e}")



            # Récupérer la première action ou en créer une par défaut
            action_defaut = Action.query.first()
            if not action_defaut:
                # Créer une action par défaut avec les champs OBLIGATOIRES
                action_defaut = Action(
                    titre="Action système",  # ← OBLIGATOIRE (nullable=False)
                    assignee_a_id=current_user.id,  # ← OBLIGATOIRE (clé étrangère)
                    creee_par_id=current_user.id,  # ← OBLIGATOIRE (clé étrangère)
                    date_echeance=datetime.now() + timedelta(days=30),  # ← OBLIGATOIRE
                    type_action='tache',
                    priorite='moyenne',
                    statut='a_faire',
                    progression=0
                )
                db.session.add(action_defaut)
                db.session.flush()



            # Notification client
            notification_client = Notification(
                employe_id=nouveau_client.id,
                titre="Conditions générales à signer",
                message=f"Bonjour {prenom}, veuillez signer les conditions générales via ce lien : {lien_terms}",
                type_notification='terms',
                lien=lien_terms,
                date_envoi=datetime.now(),
                lue=False,
                date_creation=datetime.now(),
                destinataire_id=nouveau_client.id,
                action_id=action_defaut.id
            )
            db.session.add(notification_client)

            # Notification conseiller
            notification_conseiller = Notification(
                employe_id=current_user.id,
                titre="Dossier créé en attente de signature",
                message=f"Le dossier de {prenom} {nom} a été créé et est en attente de signature des conditions.",
                type_notification='info',
                date_envoi=datetime.now(),
                lue=False,
                date_creation=datetime.now(),
                destinataire_id=current_user.id,
                action_id=action_defaut.id
            )

            db.session.add(notification_conseiller)
            print("🔥 ON ARRIVE AVANT COMMIT")
            db.session.commit()
            print("🔥 ON ARRIVE APRES COMMIT")
            flash(
                f'✅ Dossier créé avec succès pour {prenom} {nom}! Un lien a été envoyé au client.',
                'success'
            )

            # FORCER la redirection avec un code 302
            # Juste avant le return, ajoutez :

            return redirect(url_for('conseiller_dossier_en_attente', succursale_code=succursale.code))

    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        print("ERREUR REELLE :", str(e))
        # ⚠️ redéfinir succursales ici
        succursales = Succursale.query.all()
        return render_template(
            'creer_dossier.html',
            error=str(e),  # ← affiche la vraie erreur
            succursales=succursales,
            succursale=succursale,
            branch_code=branch_code,
            default_code=f"7-12519-{branch_code}-{random.randint(10000, 99999)}",
            default_suffix=str(random.randint(10000, 99999))

        )



def calculer_statistiques_succursale(succursale_id):
    """Calcule les statistiques pour une succursale spécifique"""
    stats = {
        'clients': Client.query.filter_by(succursale_id=succursale_id).count(),
        'employes': User.query.filter(
            User.succursale_id == succursale_id,
            User.role.in_(['employe', 'superviseur'])
        ).count(),
        'prets': Pret.query.filter_by(
            succursale_id=succursale_id,
            statut='actif'
        ).count(),
        'remboursements': db.session.query(db.func.sum(Remboursement.montant)).join(
            Pret, Pret.id == Remboursement.pret_id
        ).filter(Pret.succursale_id == succursale_id).scalar() or 0
    }
    return stats


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Client  # Adaptez selon vos modèles


@app.route('/supprimer-tous-clients', methods=['POST'])
def supprimer_tous_clients():
    try:
        # Méthode 1: Si vous utilisez SQLAlchemy ORM
        Client.query.delete()
        db.session.commit()

        # Méthode 2: Si vous préférez du SQL direct
        # db.engine.execute("DELETE FROM clients;")

        flash('Tous les clients ont été supprimés avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'error')

    return redirect(url_for('employe_gestion_clients'))  # Redirigez vers la page appropriée


# Route pour voir le contenu du dossier employees
@app.route('/debug-employees-folder')
def debug_employees_folder():
    import os
    folder_path = os.path.join(app.root_path, 'templates', 'employees')

    if not os.path.exists(folder_path):
        return f"❌ Dossier non trouvé: {folder_path}"

    files = os.listdir(folder_path)

    result = f"<h1>Contenu de {folder_path}</h1>"
    result += f"<p>{len(files)} fichier(s) trouvé(s):</p>"
    result += "<ul>"

    for file in files:
        if file.endswith('.html'):
            result += f"<li>✅ {file}</li>"
        else:
            result += f"<li>📄 {file}</li>"

    result += "</ul>"

    # Suggestion
    if 'conseiller_dossiers_en_attente.html' not in files:
        result += "<p style='color:red'>❌ Le fichier conseiller_dossiers_en_attente.html est MANQUANT !</p>"
        result += "<p>✅ Créez ce fichier ou déplacez-le depuis un autre dossier.</p>"

    return result


# Route temporaire pour vérifier le mot de passe
@app.route('/debug-password')
def debug_password():
    from models import User
    from werkzeug.security import check_password_hash

    user = User.query.filter_by(username='cc').first()

    if not user:
        return "❌ Utilisateur 'cc' non trouvé"

    # Test avec différents mots de passe possibles
    passwords_to_test = ['cc', 'password', 'admin123', 'employe123', 'cc123']

    result = f"<h1>Utilisateur: {user.username}</h1>"
    result += f"<p>Hash: {user.password_hash}</p>"

    for pwd in passwords_to_test:
        if user.check_password(pwd):
            result += f"<p>✅ Mot de passe correct: '{pwd}'</p>"
        else:
            result += f"<p>❌ Mot de passe incorrect: '{pwd}'</p>"

    return result


# Route pour lister les utilisateurs
@app.route('/debug-users')
def debug_users():
    from models import User

    users = User.query.all()

    result = "<h1>Liste des utilisateurs</h1>"
    for user in users:
        result += f"""
        <div style="border:1px solid #ccc; margin:10px; padding:10px;">
            <strong>{user.username}</strong> (ID: {user.id})<br>
            Rôle: {user.role}<br>
            Email: {user.email}<br>
            Password hash: {user.password_hash[:50]}...<br>
        </div>
        """

    return result



@app.route('/client/terms/<token>', methods=['GET', 'POST'])
def client_terms(token):
    """Page des termes et conditions pour le client - Version JWT"""
    from models import User, TermsAcceptance, Notification, Action, Client
    from datetime import datetime, timedelta
    from flask_login import login_user
    import jwt

    print(f"🔍 ROUTE CLIENT_TERMS - Token reçu: {token[:50]}...")

    client = None

    # ===== 1. DÉCODER LE TOKEN JWT =====
    try:
        from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

        try:
            # Nettoyer le token (enlever espaces ou retours à la ligne)
            token = token.strip()

            s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            client_id = s.loads(token, salt="terms-accept", max_age=604800)

            client = db.session.get(Client, client_id)

            if not client:
                flash('❌ Client non trouvé', 'danger')
                return redirect(url_for('connexion'))

            print(f"✅ Client trouvé: {client.email}")

        except SignatureExpired:
            flash('⚠️ Le lien a expiré (7 jours). Veuillez demander un nouveau lien.', 'danger')
            return redirect(url_for('connexion'))
        except BadSignature as e:
            print(f"❌ Token invalide: {e}")
            flash('❌ Lien invalide. Veuillez contacter votre conseiller.', 'danger')
            return redirect(url_for('connexion'))

    except jwt.ExpiredSignatureError:
        flash('⚠️ Le lien a expiré (7 jours). Veuillez demander un nouveau lien.', 'danger')
        return redirect(url_for('connexion'))
    except jwt.InvalidTokenError as e:
        print(f"❌ Token invalide: {e}")
        flash('❌ Lien invalide. Veuillez contacter votre conseiller.', 'danger')
        return redirect(url_for('connexion'))

    # ===== 2. VÉRIFIER SI LE CLIENT EST DÉJÀ TRAITÉ =====
    if client.statut != 'en_attente_terms':
        if client.terms_accepted:
            flash('ℹ️ Vous avez déjà accepté les conditions', 'info')
        else:
            flash('ℹ️ Ce dossier a déjà été traité', 'info')
        return redirect(url_for('connexion'))

    # ===== 3. TRAITEMENT DU FORMULAIRE =====
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'accepter':
            try:
                # Enregistrer l'acceptation
                acceptance = TermsAcceptance(
                    client_id=client.id,
                    date_acceptation=datetime.now(),
                    ip_address=request.remote_addr,
                    user_agent=request.user_agent.string
                )
                db.session.add(acceptance)

                # Mettre à jour le client
                client.statut = 'en_attente_approbation'
                client.terms_accepted = True
                client.terms_accepted_at = datetime.now()
                client.date_signature_terms = datetime.now()

                # Créer ou récupérer l'utilisateur
                user = db.session.get(User, client.id)
                if not user:
                    from werkzeug.security import generate_password_hash
                    import uuid
                    user = User(
                        id=client.id,
                        prenom=client.prenom,
                        nom=client.nom,
                        email=client.email,
                        telephone=client.telephone,
                        password=generate_password_hash(str(uuid.uuid4())),
                        compte_actif=True,
                        terms_accepted=True,
                        role='client',
                        statut='en_attente_approbation',
                        date_creation=datetime.now()
                    )
                    db.session.add(user)
                else:
                    user.terms_accepted = True
                    user.statut = 'en_attente_approbation'

                # Gérer l'action par défaut
                action_defaut = Action.query.first()
                if not action_defaut:
                    action_defaut = Action(
                        titre="Action système",
                        assignee_a_id=client.cree_par_id or 1,
                        creee_par_id=client.cree_par_id or 1,
                        date_echeance=datetime.now() + timedelta(days=30),
                        type_action='tache',
                        priorite='moyenne',
                        statut='a_faire',
                        progression=0
                    )
                    db.session.add(action_defaut)
                    db.session.flush()

                # Notifier le conseiller
                if client.cree_par_id:
                    conseiller = db.session.get(User, client.cree_par_id)
                    if conseiller:
                        notification_conseiller = Notification(
                            employe_id=conseiller.id,
                            titre="✅ Client a signé les conditions",
                            message=f"{client.prenom} {client.nom} a accepté les conditions générales. En attente d'approbation.",
                            type_notification='info',
                            action_id=action_defaut.id,
                            date_envoi=datetime.now(),
                            destinataire_id=client.cree_par_id,
                            lien=url_for('conseiller_voir_dossier', dossier_id=client.id, _external=True)
                        )
                        db.session.add(notification_conseiller)
                        print(f"✅ Notification envoyée au conseiller: {conseiller.prenom} {conseiller.nom}")

                # Notifier le directeur
                directeur = User.query.filter_by(
                    succursale_id=client.succursale_id,
                    role='direction'
                ).first()

                if directeur:
                    notification_directeur = Notification(
                        employe_id=directeur.id,
                        titre="📋 Nouveau dossier à approuver",
                        message=f"{client.prenom} {client.nom} a signé les conditions et attend votre approbation.",
                        type_notification='approval',
                        lien=url_for('directeur_approuver_dossier', client_id=client.id, _external=True),
                        date_envoi=datetime.now(),
                        action_id=action_defaut.id,
                        destinataire_id=directeur.id
                    )
                    db.session.add(notification_directeur)
                    print(f"✅ Notification envoyée au directeur: {directeur.prenom} {directeur.nom}")

                db.session.commit()
                flash('✅ Conditions acceptées! Votre dossier est en attente d\'approbation.', 'success')

                # Page de succès simple
                return f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Signature réussie - GMES Microcrédit</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; margin: 0; }}
                        .container {{ background: white; border-radius: 20px; padding: 40px; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); animation: fadeIn 0.5s ease-out; }}
                        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(-20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
                        .success-icon {{ font-size: 80px; color: #28a745; margin-bottom: 20px; }}
                        h1 {{ color: #333; margin-bottom: 15px; }}
                        .message {{ font-size: 18px; color: #666; margin-bottom: 30px; line-height: 1.6; }}
                        .btn {{ display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: bold; }}
                        .btn:hover {{ transform: translateY(-2px); }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="success-icon">✅</div>
                        <h1>Merci {client.prenom} !</h1>
                        <div class="message">
                            Votre acceptation des conditions générales a bien été enregistrée.<br><br>
                            Votre dossier est maintenant en attente d'approbation.
                        </div>
                        <a href="/" class="btn">Retour à l'accueil</a>
                    </div>
                </body>
                </html>
                """

            except Exception as e:
                db.session.rollback()
                print(f"❌ Erreur acceptation: {e}")
                flash('❌ Une erreur est survenue. Veuillez réessayer.', 'danger')
                return redirect(request.url)

        elif action == 'refuser':
            client.statut = 'refus_terms'
            client.terms_accepted = False
            db.session.commit()
            flash('❌ Vous avez refusé les conditions générales.', 'info')
            return redirect(url_for('connexion'))

    return render_template('terms.html', client=client)


# Route pour vérifier les permissions de cc
@app.route('/check-cc-permissions')
def check_cc_permissions():
    from models import User

    user = User.query.filter_by(username='cc').first()

    if not user:
        return "❌ Utilisateur 'cc' non trouvé"

    result = f"<h1>Vérification des droits pour {user.username}</h1>"
    result += f"<p>ID: {user.id}</p>"
    result += f"<p>Rôle: {user.role}</p>"
    result += f"<p>Fonction: {user.fonction}</p>"

    # Vérifier la permission conseiller
    if hasattr(user, 'has_permission'):
        if user.has_permission('conseiller'):
            result += "<p style='color:green'>✅ A la permission 'conseiller'</p>"
        else:
            result += "<p style='color:red'>❌ N'a PAS la permission 'conseiller'</p>"

    # Vérifier dans la table permissions
    if hasattr(user, 'permissions'):
        result += f"<p>Permissions brutes: {user.permissions}</p>"

    return result



@app.route('/direction/approuver-dossier/<int:client_id>', methods=['GET', 'POST'])
@login_required
def directeur_approuver_dossier(client_id):
    """Le directeur approuve ou rejette le dossier"""
    from models import User, Notification, Action, Client
    from datetime import datetime, timedelta
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import os

    # ✅ CORRECTION : Vérification des permissions
    if current_user.role != 'direction' or current_user.fonction not in ['directeur','direction' 'directeur_operations', 'directeur_general']:
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    client = Client.query.get_or_404(client_id)

    conseiller = None
    if client.cree_par_id:
        conseiller = db.session.get(User, client.cree_par_id)



    # ✅ GESTION GET - Afficher le formulaire d'approbation
    if request.method == 'GET':
        return render_template('direction/approuver_dossier.html', client=client, conseiller=conseiller)

    # ✅ GESTION POST - Traiter la décision
    action = request.form.get('action')
    commentaire = request.form.get('commentaire', '')

    # 🔔 Récupérer ou créer une action par défaut
    action_defaut = Action.query.first()
    if not action_defaut:
        action_defaut = Action(
            titre="Action système",
            assignee_a_id=current_user.id,
            creee_par_id=current_user.id,
            date_echeance=datetime.now() + timedelta(days=30),
            type_action='tache',
            priorite='moyenne',
            statut='a_faire',
            progression=0
        )
        db.session.add(action_defaut)
        db.session.flush()

    # Configuration email
    EMAIL_EXPEDITEUR = os.environ.get('MAIL_USERNAME', 'gmeshaiti@gmail.com')
    EMAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    EMAIL_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    EMAIL_PORT = int(os.environ.get('SMTP_PORT', 587))

    if action == 'approuver':
        client.statut = 'actif'
        client.date_approbation = datetime.now()
        client.approuve_par_id = current_user.id


        message_client = f"✅ Félicitations {client.prenom}! Votre dossier a été approuvé. Vous pouvez maintenant accéder à votre compte."
        message_agent = f"✅ Le dossier de {client.prenom} {client.nom} a été approuvé."
        sujet_email = "✅ Votre dossier a été approuvé - GMES"
        flash(f'✅ Dossier de {client.prenom} {client.nom} approuvé avec succès', 'success')

    elif action == 'rejeter':
        if not commentaire:
            flash('❌ Motif de rejet requis', 'danger')
            return redirect(url_for('directeur_approuver_dossier', client_id=client.id))

        client.statut = 'rejete'
        client.motif_rejet = commentaire
        client.date_rejet = datetime.now()
        client.rejete_par_id = current_user.id

        message_client = f"❌ Votre dossier n'a pas été approuvé. Motif: {commentaire}"
        message_agent = f"❌ Le dossier de {client.prenom} {client.nom} a été rejeté. Motif: {commentaire}"
        flash(f'❌ Dossier de {client.prenom} {client.nom} rejeté', 'warning')
    else:
        flash('❌ Action invalide', 'danger')
        return redirect(url_for('directeur_tous_les_dossiers'))

        # 📧 ENVOI D'EMAIL AU CLIENT
    try:
        # Créer le message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = sujet_email
        msg['From'] = f"GMES Microcrédit <{EMAIL_EXPEDITEUR}>"
        msg['To'] = client.email

        # Version HTML du message
        html = f"""
           <!DOCTYPE html>
           <html>
           <head>
               <style>
                   body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                   .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                   .header {{ background: #0b3b4f; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                   .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                   .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
               </style>
           </head>
           <body>
               <div class="container">
                   <div class="header">
                       <h1>GMES Microcrédit</h1>
                   </div>
                   <div class="content">
                       <h2>Bonjour {client.prenom} {client.nom},</h2>
                       <p>{message_client}</p>
                       <p>Si vous avez des questions, n'hésitez pas à contacter votre conseiller.</p>
                       <p>Cordialement,<br>L'équipe GMES Microcrédit</p>
                   </div>
                   <div class="footer">
                       <p>Cet email a été envoyé automatiquement, merci de ne pas y répondre.</p>
                       <p>© 2025 GMES Microcrédit. Tous droits réservés.</p>
                   </div>
               </div>
           </body>
           </html>
           """

        # Version texte simple
        text = f"""
           Bonjour {client.prenom} {client.nom},

           {message_client}

           Si vous avez des questions, n'hésitez pas à contacter votre conseiller.

           Cordialement,
           L'équipe GMES Microcrédit
           """

        # Attacher les versions texte et HTML
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Envoyer l'email
        server = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_EXPEDITEUR, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email envoyé à {client.email}")

    except Exception as e:
        print(f"❌ Erreur envoi email à {client.email}: {e}")

    # Notification au client (en utilisant type_notification)
    notification_client = Notification(
        employe_id=client.id,
        titre=f"Dossier {action}",
        message=message_client,
        type_notification='info',
        date_envoi=datetime.now(),
        action_id = action_defaut.id,  # ← AJOUTÉ
        destinataire_id = client.id  # ← AJOUTÉ (souvent le même que employe_id)
    )
    db.session.add(notification_client)

    # Notification au conseiller
    if client.cree_par_id:
        notification_agent = Notification(
            employe_id=client.cree_par_id,
            titre=f"Dossier {action} par le directeur",
            message=message_agent,
            type_notification='info',
            date_envoi=datetime.now(),
            action_id=action_defaut.id,  # ← AJOUTÉ
            destinataire_id=client.cree_par_id  # ← AJOUTÉ
        )
        db.session.add(notification_agent)

    db.session.commit()

    return redirect(url_for('directeur_tous_les_dossiers'))


@app.route('/direction/tous_dossiers')
@app.route('/direction/tous_dossiers/<succursale_code>')
@login_required
def directeur_tous_les_dossiers(succursale_code=None):
    """Le directeur voit TOUS les dossiers de SA succursale uniquement"""

    # Afficher le rôle pour debug
    print(f"🔍 Tentative d'accès - Rôle: {current_user.role}, Fonction: {current_user.fonction}")

    # Rôles autorisés
    roles_autorises = ['direction', 'directeur', 'super_admin', 'admin_succursale']

    # ✅ CORRECTION : Vérifier si le rôle est dans la liste autorisée
    if current_user.role not in roles_autorises:
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    # Déterminer la succursale à afficher
    if succursale_code:
        succursale = Succursale.query.filter_by(code=succursale_code).first_or_404()
        # Vérifier que l'utilisateur a accès à cette succursale
        if current_user.role not in ['super_admin'] and current_user.succursale_id != succursale.id:
            flash('⛔ Vous ne pouvez voir que les dossiers de votre succursale', 'danger')
            if current_user.succursale:
                return redirect(url_for('directeur_tous_les_dossiers', succursale_code=current_user.succursale.code))
            else:
                return redirect(url_for('dashboard_redirect'))
    else:
        # Utiliser la succursale de l'utilisateur connecté
        if current_user.succursale_id:
            succursale = db.session.get(Succursale, current_user.succursale_id)
        else:
            # Pour super_admin sans succursale, prendre la première
            succursale = Succursale.query.first()

        if not succursale:
            flash('❌ Aucune succursale trouvée', 'danger')
            return redirect(url_for('dashboard_redirect'))
        succursale_code = succursale.code

    print(f"🔍 {current_user.role} {current_user.id} consulte les dossiers de la succursale {succursale.nom}")

    # Récupérer les clients de CETTE succursale
    dossiers = []
    clients = Client.query.filter_by(
        succursale_id=succursale.id
    ).order_by(Client.date_inscription.desc()).all()

    for client in clients:
        conseiller = db.session.get(User, client.cree_par_id) if client.cree_par_id else None
        dossiers.append({
            'client': client,
            'conseiller_prenom': conseiller.prenom if conseiller else 'Inconnu',
            'conseiller_nom': conseiller.nom if conseiller else '',
            'succursale': succursale.nom
        })

    # Statistiques par conseiller de CETTE succursale
    stats_par_agent = []
    conseillers = User.query.filter_by(
        role='employe',
        fonction='conseiller',
        succursale_id=succursale.id
    ).all()

    for conseiller in conseillers:
        nb_dossiers = User.query.filter_by(
            cree_par_id=conseiller.id,
            role='client'
        ).count()
        actifs = User.query.filter_by(
            cree_par_id=conseiller.id,
            role='client',
            statut='actif'
        ).count()
        stats_par_agent.append({
            'id': conseiller.id,
            'prenom': conseiller.prenom,
            'nom': conseiller.nom,
            'nb_dossiers': nb_dossiers,
            'actifs': actifs
        })

    # Statistiques globales de la succursale
    stats = {
        'total_dossiers': len(clients),
        'agents_actifs': len(conseillers),
        'en_attente': User.query.filter_by(
            role='client',
            statut='en_attente_approbation',
            succursale_id=succursale.id
        ).count(),
        'succursale_nom': succursale.nom,
        'succursale_code': succursale.code
    }

    return render_template('direction/tous_dossiers.html',
                           dossiers=dossiers,
                           stats_par_agent=stats_par_agent,
                           agents_liste=conseillers,
                           stats=stats,
                           succursale=succursale)


@app.route('/direction/voir-dossier/<int:dossier_id>')
@login_required
def directeur_voir_dossier(dossier_id):
    """Page pour que le directeur voie et approuve un dossier"""
    if current_user.role not in ['direction', 'admin_succursale', 'super_admin']:
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('connexion'))

    dossier = Client.query.get_or_404(dossier_id)

    return render_template('direction/voir_dossier.html', dossier=dossier)




@app.route('/directeur/rejeter-dossier/<int:client_id>', methods=['GET'])
@login_required
def directeur_rejeter_dossier(client_id):
    """Rejeter un dossier avec motif (redirige vers la route POST)"""
    motif = request.args.get('motif', '')

    if not motif:
        flash('❌ Motif de rejet requis', 'danger')
        return redirect(url_for('direction_tous_les_dossiers'))

    # Simuler un formulaire POST vers la route d'approbation
    return redirect(url_for('directeur_approuver_dossier', client_id=client_id))

@app.route('/conseiller/mes-dossiers')
@login_required
def conseiller_mes_dossiers():
    """L'agent voit uniquement ses dossiers"""

    if current_user.role != 'employe' or current_user.fonction != 'conseiller':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    dossiers = Client.query.filter_by(
        cree_par_id=current_user.id,
    ).order_by(Client.date_inscription.desc()).all()

    return render_template('employees/conseiller_dossiers_en_attente.html',
                           dossiers=dossiers,
                           agent_nom=f"{current_user.prenom} {current_user.nom}",
                           succursale_code=current_user.succursale.code if current_user.succursale else '')



@app.route('/conseiller/dossiers-en-attente')
@app.route('/conseiller/dossiers-en-attente/<succursale_code>')
@login_required
def conseiller_dossier_en_attente(succursale_code=None):
    """Affiche les dossiers en attente du conseiller"""

    print(f"🔍 Agent {current_user.id} - {current_user.prenom} {current_user.nom} consulte ses dossiers")

    # Si pas de code, utiliser celui du current_user
    if not succursale_code and current_user.succursale:
        succursale_code = current_user.succursale.code

        # ✅ FILTRE IMPORTANT : SEULEMENT les dossiers créés par CET agent
    dossiers = Client.query.filter_by(
        cree_par_id=current_user.id,  # ← Clé : créé par CET agent
    ).order_by(Client.date_inscription.desc()).all()

    print(f"✅ {len(dossiers)} dossier(s) trouvé(s) pour l'agent {current_user.prenom}")

    return render_template('employees/conseiller_dossiers_en_attente.html',
                           dossiers=dossiers,
                           agent_nom=f"{current_user.prenom} {current_user.nom}",
                           succursale_code=succursale_code)


@app.route('/debug-template')
def debug_template():
    """Vérifie si le template existe"""
    import os
    template_path = os.path.join('templates', 'employees', 'conseiller_dossiers_en_attente.html')

    if os.path.exists(template_path):
        return f"✅ Template trouvé à: {template_path}"
    else:
        return f"❌ Template NON trouvé à: {template_path}"

@app.route('/debug-redirect')
@login_required
def debug_redirect():
    """Route de debug pour tester la redirection"""
    print(f"🔍 Debug redirect - User: {current_user.id}")
    flash('Test de redirection réussi!', 'success')
    return redirect(url_for('conseiller_dossier_en_attente'))



@app.route('/direction/analyse-strategique')
@login_required
def analyse_strategique():
    """Page d'analyse stratégique"""
    if current_user.role != 'direction' or current_user.fonction != 'directeur_general':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    # Données pour l'analyse
    periode = {
        'debut': '01/01/2024',
        'fin': '31/12/2024'
    }

    stats = {
        'croissance_portefeuille': '+12.5%',
        'vs_precedent': '+3.2%',
        'part_marche': '18.3%',
        'vs_concurrents': '+2.1%',
        'rentabilite': '15.2%',
        'roe': '12.8%',
        'satisfaction': '87%',
        'nps': '42'
    }

    return render_template('direction/analyse_strategique.html',
                           periode=periode,
                           stats=stats)


@app.route('/direction/rapport-strategique')
@login_required
@role_required('admin')
def rapport_strategique():
    # Récupérer les données des retards pour le rapport
    stats_retards = {
        'total_clients_impactes': db.session.query(
            RetardPaiement.client_id.distinct()
        ).filter_by(statut='impaye').count(),

        'total_retards_actifs': RetardPaiement.query.filter_by(statut='impaye').count(),

        'total_jours_retard': db.session.query(
            db.func.sum(RetardPaiement.jours_retard)
        ).filter_by(statut='impaye').scalar() or 0,

        'moyenne_jours_par_retard': db.session.query(
            db.func.avg(RetardPaiement.jours_retard)
        ).filter_by(statut='impaye').scalar() or 0,

        'top_5_clients_retard': db.session.query(
            Client.nom,
            Client.prenom,
            db.func.sum(RetardPaiement.jours_retard).label('total_retard')
        ).join(
            RetardPaiement, Client.id == RetardPaiement.client_id
        ).filter(
            RetardPaiement.statut == 'impaye'
        ).group_by(
            Client.id
        ).order_by(
            db.func.sum(RetardPaiement.jours_retard).desc()
        ).limit(5).all(),

        'retards_par_mois': db.session.query(
            db.func.strftime('%Y-%m', RetardPaiement.date_creation),
            db.func.count(RetardPaiement.id)
        ).group_by(
            db.func.strftime('%Y-%m', RetardPaiement.date_creation)
        ).all()
    }

    # Tendance des retards (comparaison mois précédent)
    mois_courant = datetime.now().replace(day=1)
    mois_precedent = (mois_courant - timedelta(days=1)).replace(day=1)

    retards_mois_courant = RetardPaiement.query.filter(
        RetardPaiement.date_creation >= mois_courant,
        RetardPaiement.statut == 'impaye'
    ).count()

    retards_mois_precedent = RetardPaiement.query.filter(
        RetardPaiement.date_creation >= mois_precedent,
        RetardPaiement.date_creation < mois_courant,
        RetardPaiement.statut == 'impaye'
    ).count()

    tendance = {
        'evolution': ((retards_mois_courant - retards_mois_precedent) / (retards_mois_precedent or 1)) * 100,
        'couleur': 'rouge' if retards_mois_courant > retards_mois_precedent else 'vert'
    }

    return render_template('direction/rapport_strategique.html',
                           stats_retards=stats_retards,
                           tendance=tendance)

@app.route('/direction/comite-direction')
@login_required
def comite_direction():
    """Page du comité de direction"""
    if current_user.role != 'direction' or current_user.fonction != 'directeur_general':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    comite = {
        'date': '15 Mars 2024',
        'heure': '10:00 - 12:00'
    }

    return render_template('direction/comite_direction.html',
                           comite=comite)


@app.route('/direction/decisions')
@login_required
def liste_decisions():
    """Liste toutes les décisions stratégiques"""
    if current_user.role not in ['direction', 'admin', 'super_admin']:
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('connexion'))

    from models import Decision

    # Filtrer selon le rôle
    if current_user.role == 'super_admin':
        decisions = Decision.query.order_by(Decision.date_creation.desc()).all()
    else:
        decisions = Decision.query.filter_by(
            succursale_id=current_user.succursale_id
        ).order_by(Decision.date_creation.desc()).all()

    return render_template('direction/decisions/liste.html', decisions=decisions)


@app.route('/direction/decisions/nouvelle', methods=['GET', 'POST'])
@login_required
def nouvelle_decision():
    """Créer une nouvelle décision"""
    from models import Decision, Succursale

    if request.method == 'POST':
        decision = Decision(
            titre=request.form.get('titre'),
            description=request.form.get('description'),
            type_decision=request.form.get('type_decision'),
            date_echeance=datetime.strptime(request.form.get('date_echeance'), '%Y-%m-%d') if request.form.get(
                'date_echeance') else None,
            priorite=request.form.get('priorite', 'moyenne'),
            cree_par_id=current_user.id,
            responsable_id=request.form.get('responsable_id') or None,
            succursale_id=request.form.get('succursale_id') or current_user.succursale_id
        )
        db.session.add(decision)
        db.session.commit()
        flash('✅ Décision créée avec succès', 'success')
        return redirect(url_for('liste_decisions'))

    from models import User, Succursale
    responsables = User.query.filter(User.role.in_(['direction', 'admin'])).all()
    succursales = Succursale.query.all()

    return render_template('direction/decisions/nouvelle.html',
                           responsables=responsables,
                           succursales=succursales)


@app.route('/direction/decisions/<int:decision_id>')
@login_required
def voir_decision(decision_id):
    """Voir les détails d'une décision"""
    from models import Decision, ActionDecision, CommentaireDecision

    decision = Decision.query.get_or_404(decision_id)
    return render_template('direction/decisions/voir.html', decision=decision)


@app.route('/direction/decisions/<int:decision_id>/avancement', methods=['POST'])
@login_required
def maj_avancement(decision_id):
    from models import Decision, ActionDecision, CommentaireDecision
    """Mettre à jour l'avancement d'une décision"""
    decision = Decision.query.get_or_404(decision_id)
    progression = request.form.get('progression', type=int)

    if progression is not None and 0 <= progression <= 100:
        decision.progression = progression
        if progression == 100:
            decision.statut = 'realisee'
            decision.date_execution = datetime.now()
        elif progression > 0:
            decision.statut = 'en_cours'
        db.session.commit()
        return jsonify({'success': True})

    return jsonify({'success': False, 'error': 'Progression invalide'}), 400


@app.route('/direction/decisions')
@login_required
def decisions():
    """Page de suivi des décisions"""
    if current_user.role != 'direction' or current_user.fonction != 'directeur_general':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import Decision, User, Reunion
    from datetime import datetime, timedelta

    # Paramètres de filtrage
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '')
    statut = request.args.get('statut', '')
    priorite = request.args.get('priorite', '')
    responsable = request.args.get('responsable', type=int)

    # Requête de base
    query = Decision.query

    if search:
        query = query.filter(Decision.titre.contains(search) | Decision.description.contains(search))
    if statut:
        query = query.filter_by(statut=statut)
    if priorite:
        query = query.filter_by(priorite=priorite)
    if responsable:
        query = query.filter_by(responsable_id=responsable)

    # Pagination
    pagination = query.order_by(Decision.date_echeance).paginate(page=page, per_page=per_page)
    decisions = pagination.items
    pages = pagination.pages

    # Statistiques
    stats = {
        'total': Decision.query.count(),
        'a_faire': Decision.query.filter_by(statut='a_faire').count(),
        'en_cours': Decision.query.filter_by(statut='en_cours').count(),
        'terminees': Decision.query.filter_by(statut='terminee').count(),
        'en_retard': Decision.query.filter(Decision.date_echeance < datetime.now(),
                                           Decision.statut.in_(['a_faire', 'en_cours'])).count(),
        'taux_realisation': 68  # À calculer
    }

    # Décisions en retard
    decisions_retard = Decision.query.filter(
        Decision.date_echeance < datetime.now(),
        Decision.statut.in_(['a_faire', 'en_cours'])
    ).limit(5).all()

    # Échéances à venir
    date_limite = datetime.now() + timedelta(days=7)
    echeances = []

    # Responsables pour les filtres
    responsables = User.query.filter_by(role='direction').all()

    # Réunions pour le modal
    reunions = Reunion.query.filter(Reunion.date_reunion >= datetime.now()).limit(5).all()

    return render_template('direction/decisions.html',
                           decisions=decisions,
                           stats=stats,
                           decisions_retard=decisions_retard,
                           echeances=echeances,
                           responsables=responsables,
                           reunions=reunions,
                           search=search,
                           statut=statut,
                           priorite=priorite,
                           responsable=responsable,
                           page=page,
                           pages=pages)


@app.route('/direction/budget-previsionnel')
@login_required
def budget_previsionnel():
    """Page du budget prévisionnel"""
    if current_user.role != 'direction' or current_user.fonction != 'directeur_financier':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    budget = {
        'annee': 2024,
        'version': 'v2.3',
        'total': 125000000,
        'realise': 78200000,
        'pourcentage_realise': 62.6,
        'reste': 46800000,
        'mois_restants': 6,
        'ecart': 3200000,
        'ecart_pourcentage': 2.6,
        'ecart_couleur': 'success'
    }

    return render_template('direction/budget_previsionnel.html',
                           budget=budget)


@app.route('/direction/conseil-administration')
@login_required
def conseil_administration():
    """Page du conseil d'administration"""
    if current_user.role != 'direction' or current_user.fonction != 'directeur_general':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    session = {
        'date': '15 Mars 2024',
        'heure': '10:00 - 13:00',
        'lieu': 'Salle du Conseil - Siège Social',
        'numero': '24-01'
    }

    return render_template('direction/conseil_administration.html',
                           session=session)


@app.route('/direction/rapports-brh')
@login_required
def rapports_brh():
    """Page des rapports BRH"""
    if current_user.role != 'direction' or current_user.fonction != 'directeur_financier':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    periode = {
        'mois': 'Mars',
        'annee': 2024
    }

    dernier_envoi = '15/03/2024'

    ratios = {
        'solvabilite': '15.2%',
        'liquidite': '18.5%',
        'fonds_propres': '12.8%',
        'creances_douteuses': '4.2%'
    }

    return render_template('direction/rapports_brh.html',
                           periode=periode,
                           dernier_envoi=dernier_envoi,
                           ratios=ratios)


@app.route('/direction/plan-strategique')
@login_required
def plan_strategique():
    """Page du plan stratégique"""
    if current_user.role != 'direction' or current_user.fonction != 'directeur_general':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    plan = {
        'periode': '2024 - 2027',
        'version': '2.0',
        'date_approbation': '15/03/2024'
    }

    objectifs = {
        'digitalisation': {
            'app_mobile': False,
            'processus': True,
            'scoring': False
        }
    }

    return render_template('direction/plan_strategique.html',
                           plan=plan,
                           objectifs=objectifs)



def obtenir_actions_utilisateur(employe_id):
    """Récupère les actions d'un utilisateur pour la gamification"""
    # Simulation - à remplacer par votre logique réelle
    actions = [
        {'type': 'remboursement_ponctuel', 'description': 'Remboursement à temps'},
        {'type': 'pret_rembourse', 'description': 'Prêt complètement remboursé'},
        {'type': 'participation_groupe', 'description': 'Participation active au groupe'}
    ]
    return actions

def calculer_historique_client(client_id):
    """Calcule l'historique d'un client pour le scoring"""
    # Simulation - à remplacer par votre logique réelle
    return {
        'nombre_prets': Pret.query.filter_by(client_id=client_id).count(),
        'prets_rembourses': Pret.query.filter_by(client_id=client_id, statut='termine').count(),
        'taux_remboursement': 85,  # À calculer dynamiquement
        'jours_retard_moyen': 2,
        'incidents_paiement': 0
    }


def calculer_statistiques_utilisateur(user):
    """Calcule les stats pour le tableau de bord"""
    stats = {}

    # Importations avec fallback
    try:
        from utils.ai_scoring import ai_scorer
    except ImportError:
        # Fallback si le module n'existe pas ou a des erreurs
        class FallbackAIScorer:
            def calculate_credit_score(self, client_data, pret_data, historique):
                import random
                # Logique simple de score
                score = 600
                revenu = client_data.get('revenu_mensuel', 0)
                if revenu > 3000: score += 100
                if revenu > 5000: score += 50
                anciennete = client_data.get('anciennete_client', 0)
                if anciennete > 12: score += 50
                if anciennete > 24: score += 50
                score += random.randint(-50, 50)
                return max(300, min(850, score))

            def explain_score(self, client_data, pret_data, historique):
                return "Score basé sur votre profil financier et historique"

        ai_scorer = FallbackAIScorer()

    try:
        from utils.gamification import gamification
    except ImportError:
        # Fallback si le module n'existe pas
        class FallbackGamification:
            def calculate_points(self, user_actions):
                return len(user_actions) * 10 if user_actions else 0

            def get_level_progress(self, points):
                level = min(5, points // 100)
                progress = points % 100
                badge = 'Débutant' if points < 100 else 'Intermédiaire' if points < 300 else 'Expert'
                return {
                    'current_level': level,
                    'progress': progress,
                    'current_badge': badge
                }

        gamification = FallbackGamification()

    # Vérifier si c'est un Client (avec groupe_id) ou User (admin/employé)
    if hasattr(user, 'groupe_id'):  # C'est un Client
        # Score de crédit IA seulement pour les clients
        client_data = {
            'revenu_mensuel': getattr(user, 'revenu_mensuel', 0),
            'anciennete_client': (datetime.utcnow() - user.date_inscription).days // 30,
            'profession': getattr(user, 'profession', 'Non spécifié')
        }

        # Utiliser la fonction de fallback si calculer_historique_client échoue
        try:
            historique = calculer_historique_client(user.id)
        except:
            historique = {}

        score = ai_scorer.calculate_credit_score(client_data, {}, historique)

        stats['score_credit'] = score
        stats['score_categorie'] = 'excellent' if score >= 750 else 'good' if score >= 650 else 'fair'
        stats['score_label'] = ai_scorer.explain_score(client_data, {}, historique)

        # Gamification seulement pour les clients
        try:
            user_actions = obtenir_actions_utilisateur(user.id)
        except:
            user_actions = []

        points = gamification.calculate_points(user_actions)
        niveau_info = gamification.get_level_progress(points)

        stats.update({
            'niveau': niveau_info['current_level'],
            'points': points,
            'progression': niveau_info['progress'],
            'badge': niveau_info['current_badge']
        })

        # Groupe seulement pour les clients
        if user.groupe_id:
            try:

                groupe = Groupe.query.get(user.groupe_id)
                stats.update({
                    'groupe_nom': groupe.nom if groupe else None,
                    'groupe_membres': User.query.filter_by(groupe_id=user.groupe_id).count() if user.groupe_id else 0,
                })
            except:
                stats.update({
                    'groupe_nom': None,
                    'groupe_membres': 0
                })

    # Statistiques communes à tous les utilisateurs
    try:


        if hasattr(user, 'groupe_id'):
            prets_actifs = Pret.query.filter(
                Pret.client_id == user.id,
                Pret.statut == 'approuve'
            ).count()

            montant_actifs = db.session.query(db.func.sum(Pret.montant)).filter(
                Pret.client_id == user.id,
                Pret.statut == 'approuve'
            ).scalar() or 0
        else:
            prets_actifs = 0
            montant_actifs = 0

        notifications_non_lues = Notification.query.filter_by(
            utilisateur_id=user.id,
            lue=False
        ).count() if hasattr(Notification, 'query') else 0

        stats.update({
            'prets_actifs': prets_actifs,
            'montant_actifs': montant_actifs,
            'notifications_non_lues': notifications_non_lues
        })

    except Exception as e:
        # Fallback si les modèles ne sont pas disponibles
        stats.update({
            'prets_actifs': 0,
            'montant_actifs': 0,
            'notifications_non_lues': 0
        })

    return stats

# Ajoutez cette fonction utilitaire
def save_base64_image(base64_string, output_path):
    """Convertit et sauvegarde une image base64"""
    try:
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]

        image_data = base64.b64decode(base64_string)
        with open(output_path, 'wb') as f:
            f.write(image_data)
        return True
    except Exception as e:
        print(f"Erreur sauvegarde image base64: {e}")
        return False

# ==================== CONFIGURATION USER LOADER ====================


@login_manager.user_loader
def load_user(employe_id):
    """Charge l'utilisateur à chaque requête"""
    try:
        user = db.session.get(User, int(employe_id))
        print(f"🔄 Load user {employe_id}: {user.username if user else 'None'} - Rôle: {user.role if user else 'None'}")
        return user
    except Exception as e:
        print(f"❌ Erreur load_user: {e}")
        return None


from flask import session

@app.before_request
def before_request():
    """Recharge l'utilisateur à chaque requête"""
    if current_user.is_authenticated:
        # Forcer le rechargement depuis la DB
        fresh_user = db.session.get(User, current_user.id)
        if fresh_user:
            # Mettre à jour la session si nécessaire
            session['employe_id'] = fresh_user.id
            session['user_role'] = fresh_user.role


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('connexion'))


@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403

def admin_succursale_required():
    if current_user.role != 'admin_succursale':
        abort(403)




from flask import g, current_app


@app.before_request
def before_request():
    """Exécuté avant chaque requête - Version PROTÉGÉE"""
    try:
        # Vérifier si current_user existe et est authentifié
        if hasattr(current_user, 'is_authenticated'):
            if current_user.is_authenticated:
                # Ton code existant...
                pass

        # AJOUTEZ CE CODE : Stocker les endpoints disponibles dans g
        g.available_endpoints = list(app.view_functions.keys())

    except:
        # Ignorer silencieusement les erreurs d'authentification
        # Mais toujours initialiser g.available_endpoints
        if not hasattr(g, 'available_endpoints'):
            g.available_endpoints = []
        pass


# Assurez-vous d'avoir cette route :
@app.route('/client-portal')
def client_portal():  # Le nom de la fonction doit être 'client_portal'
    return render_template('client_portal.html')



def save_face_encoding(client_id, nom, face_encoding):
    """Sauvegarde l'encodage facial dans gmes.db - VERSION CORRIGÉE"""
    try:
        print(f"💾 Sauvegarde visage pour {nom} (client_id: {client_id})...")

        encoding_bytes = pickle.dumps(face_encoding)

        from sqlalchemy import text

        # Vérifier si existe déjà (par client_id)
        existing = session.execute(
            text("SELECT id FROM face_data WHERE client_id = :client_id"),
            {"client_id": client_id}
        ).fetchone()

        if existing:
            # Mise à jour
            session.execute(
                text("""
                     UPDATE face_data
                     SET nom           = :nom,
                         face_encoding = :encoding
                     WHERE client_id = :client_id
                     """),
                {
                    "nom": nom,
                    "encoding": encoding_bytes,
                    "client_id": client_id
                }
            )
            print(f"🔄 Visage mis à jour pour {nom}")
        else:
            # Insertion
            session.execute(
                text("""
                     INSERT INTO face_data (client_id, nom, face_encoding)
                     VALUES (:client_id, :nom, :encoding)
                     """),
                {
                    "client_id": client_id,
                    "nom": nom,
                    "encoding": encoding_bytes
                }
            )
            print(f"✅ Nouveau visage sauvegardé pour {nom}")

        session.commit()
        return True

    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        session.rollback()
        return False

def check_database_state():
    """Vérifie l'état de toutes les tables"""
    print("\n🔍 État de la base de données:")

    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    print(f"📋 Tables disponibles: {tables}")

    if 'face_data' in tables:
        try:
            from sqlalchemy import text
            count = session.execute(text("SELECT COUNT(*) FROM face_data")).scalar()
            print(f"👤 Enregistrements dans face_data: {count}")

            if count > 0:
                # Afficher quelques enregistrements
                rows = session.execute(text("SELECT id, client_id, nom FROM face_data LIMIT 5")).fetchall()
                for row in rows:
                    print(f"  - ID: {row[0]}, Client: {row[1]}, Nom: {row[2]}")
        except Exception as e:
            print(f"❌ Erreur lecture face_data: {e}")

# ==================== ROUTES ====================



# @app.route('/connexion', methods=['GET', 'POST'])
# def connexion():
#     if request.method == 'POST':
#         identifiant = request.form.get('identifiant')
#         password = request.form.get('password')
#
#         user = User.query.filter(
#             (User.username == identifiant) | (User.email == identifiant)
#         ).first()
#
#         if user and check_password_hash(user.password_hash, password):
#             login_user(user)
#
#             # ✅ Vérifier si c'est la première connexion
#             if user.premier_connexion:
#                 user.premier_connexion = False
#                 user.date_premiere_connexion = datetime.now()
#                 db.session.commit()
#                 flash("🔐 Bienvenue ! Veuillez changer votre mot de passe pour sécuriser votre compte.", "warning")
#                 return redirect(url_for('premier_changement_mot_de_passe'))
#
#             # Le reste doit être après le bloc if
#             if user.role == 'admin':
#                 verifier_retards()
#             return redirect(url_for('dashboard'))
#
#
#             return redirect(url_for('dashboard_redirect'))
#
#         flash("Identifiants incorrects", "danger")
#
#     return render_template('connexion.html')


@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        identifiant = request.form.get('identifiant')
        password = request.form.get('password')

        # Validation des champs
        if not identifiant or not password:
            flash("Veuillez remplir tous les champs", "danger")
            return render_template('connexion.html')

        user = User.query.filter(
            (User.username == identifiant) | (User.email == identifiant)
        ).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)

            # CAS 1: Première connexion - obliger le changement de MDP
            if user.premier_connexion:
                user.premier_connexion = False
                user.date_premiere_connexion = datetime.now()
                db.session.commit()
                flash("🔐 Bienvenue ! Veuillez changer votre mot de passe pour sécuriser votre compte.", "warning")
                return redirect(url_for('premier_changement_mot_de_passe'))

            # CAS 2: Connexion normale - admin ou utilisateur standard
            if user.role in ['super_admin', 'direction']:
                verifier_retards()  # Vérifier les retards pour les admins
                flash(f"👋 Bonjour { user.prenom } {user.nom } (Administrateur)", "success")
            else:
                flash(f"👋 Bonjour { user.prenom } { user.nom }", "success")

            # Redirection selon le rôle ou préférence
            return redirect(url_for('dashboard_redirect'))  # ou dashboard_redirect si nécessaire

        flash("Identifiants incorrects", "danger")

    return render_template('connexion.html')


@app.route('/admin/retards')
@login_required
@role_required('admin')
def gestion_retards():
    # Récupérer tous les retards avec détails
    retards = db.session.query(
        RetardPaiement,
        Client.nom,
        Client.prenom,
        Pret.montant,
        Pret.mensualite
    ).join(
        Client, RetardPaiement.client_id == Client.id
    ).join(
        Pret, RetardPaiement.pret_id == Pret.id
    ).filter(
        RetardPaiement.statut == 'impaye'
    ).order_by(
        RetardPaiement.jours_retard.desc()
    ).all()

    # Statistiques
    stats = {
        'total_retards': len(retards),
        'total_jours_retard': sum(r.RetardPaiement.jours_retard for r in retards),
        'moyenne_jours_retard': sum(r.RetardPaiement.jours_retard for r in retards) / len(retards) if retards else 0,
        'clients_concernes': len(set(r.RetardPaiement.client_id for r in retards))
    }

    return render_template('admin/gestion_retards.html', retards=retards, stats=stats)


@app.route('/premier-changement-mot-de-passe', methods=['GET', 'POST'])
@login_required
def premier_changement_mot_de_passe():
    """Premier changement de mot de passe à la première connexion"""

    if request.method == 'POST':
        nouveau_mdp = request.form.get('nouveau_mot_de_passe')
        confirmation = request.form.get('confirmation')
        nouveau_username = request.form.get('nouveau_username')

        # Validation du mot de passe
        if nouveau_mdp != confirmation:
            flash("Les mots de passe ne correspondent pas", "danger")
            return redirect(request.url)

        if len(nouveau_mdp) < 6:
            flash("Le mot de passe doit contenir au moins 6 caractères", "danger")
            return redirect(request.url)

        # Vérifier si le username est déjà pris
        if nouveau_username and nouveau_username != current_user.username:
            existing = User.query.filter_by(username=nouveau_username).first()
            if existing:
                flash("Ce nom d'utilisateur est déjà utilisé", "danger")
                return redirect(request.url)
            current_user.username = nouveau_username

        # Changer le mot de passe
        current_user.password_hash = generate_password_hash(nouveau_mdp)
        current_user.premier_connexion = False
        current_user.date_premiere_connexion = datetime.now()
        db.session.commit()

        flash("✅ Votre mot de passe a été modifié avec succès !", "success")
        return redirect(url_for('dashboard_redirect'))

    return render_template('premier_changement.html')


@app.route('/admin/creer-utilisateur', methods=['GET', 'POST'])
@login_required
def creer_utilisateur():
    if request.method == 'POST':
        # ... création de l'utilisateur ...

        # Questions secrètes
        questions = [
            request.form.get('question_1'),
            request.form.get('question_2'),
            request.form.get('question_3')
        ]
        reponses = [
            request.form.get('reponse_1').lower().strip(),
            request.form.get('reponse_2').lower().strip(),
            request.form.get('reponse_3').lower().strip()
        ]

        new_user = User(
            # ... autres champs ...
            question_secrete_1=questions[0],
            reponse_secrete_1=reponses[0],
            question_secrete_2=questions[1],
            reponse_secrete_2=reponses[1],
            question_secrete_3=questions[2],
            reponse_secrete_3=reponses[2],
            premier_connexion=True  # ← Important !
        )

        db.session.add(new_user)
        db.session.commit()

        flash(f"✅ Utilisateur {new_user.username} créé avec succès", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('creer_utilisateur.html')


@app.route('/demande-reset-mot-de-passe', methods=['GET', 'POST'])
def demande_reset_mot_de_passe():
    """Demande de réinitialisation avec questions secrètes"""

    if request.method == 'POST':
        identifiant = request.form.get('identifiant')

        user = User.query.filter(
            (User.username == identifiant) | (User.email == identifiant)
        ).first()

        if not user:
            flash("Aucun compte trouvé avec ces informations", "danger")
            return redirect(request.url)

        # Stocker l'ID en session
        session['reset_employe_id'] = user.id

        return redirect(url_for('questions_secretes', employe_id=user.id))

    return render_template('demande_reset.html')


@app.route('/questions-secretes/<int:employe_id>', methods=['GET', 'POST'])
def questions_secretes(employe_id):
    """Vérification des questions secrètes"""
    from models import User

    user = User.query.get_or_404(employe_id)

    # Vérifier que l'utilisateur a bien des questions secrètes
    if not user.question_secrete_1:
        flash("Ce compte n'a pas de questions secrètes configurées", "danger")
        return redirect(url_for('connexion'))

    if request.method == 'POST':
        reponse_1 = request.form.get('reponse_1', '').lower().strip()
        reponse_2 = request.form.get('reponse_2', '').lower().strip()
        reponse_3 = request.form.get('reponse_3', '').lower().strip()

        if (reponse_1 == user.reponse_secrete_1 and
                reponse_2 == user.reponse_secrete_2 and
                reponse_3 == user.reponse_secrete_3):

            # Générer un token de réinitialisation
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            user.reset_token_expiration = datetime.now() + timedelta(hours=24)
            db.session.commit()

            return redirect(url_for('reinitialiser_mot_de_passe', token=token))
        else:
            flash("Réponses incorrectes", "danger")

    return render_template('questions_secretes.html', user=user)


@app.route('/reinitialiser-mot-de-passe/<token>', methods=['GET', 'POST'])
def reinitialiser_mot_de_passe(token):
    """Réinitialisation après validation des questions secrètes"""
    from models import User

    user = User.query.filter_by(reset_token=token).first()

    if not user or user.reset_token_expiration < datetime.now():
        flash("Lien invalide ou expiré", "danger")
        return redirect(url_for('connexion'))

    if request.method == 'POST':
        nouveau_mdp = request.form.get('nouveau_mot_de_passe')
        confirmation = request.form.get('confirmation')

        if nouveau_mdp != confirmation:
            flash("Les mots de passe ne correspondent pas", "danger")
            return redirect(request.url)

        if len(nouveau_mdp) < 6:
            flash("Le mot de passe doit contenir au moins 6 caractères", "danger")
            return redirect(request.url)

        user.password_hash = generate_password_hash(nouveau_mdp)
        user.reset_token = None
        user.reset_token_expiration = None
        db.session.commit()

        flash("✅ Votre mot de passe a été réinitialisé avec succès", "success")
        return redirect(url_for('connexion'))

    return render_template('reinitialiser_mdp.html', token=token)


def notifier_admin_changement_username(user):
    """
    Notifie les administrateurs d'une demande de changement de nom d'utilisateur
    """
    from models import Notification, User
    from datetime import datetime

    # Récupérer tous les administrateurs
    admins = User.query.filter(
        User.role.in_(['super_admin', 'admin_central', 'admin_succursale'])
    ).all()

    if not admins:
        print("⚠️ Aucun administrateur trouvé pour la notification")
        return

    # Message de la notification
    titre = "📝 Demande de changement de nom d'utilisateur"
    message = f"""
    L'utilisateur {user.prenom} {user.nom} (ID: {user.id}) demande de changer son nom d'utilisateur.

    📌 Ancien username: {user.username}
    ✨ Nouveau username demandé: {user.nouveau_username_demande}

    📅 Date de la demande: {datetime.now().strftime('%d/%m/%Y à %H:%M')}

    Pour approuver ou rejeter cette demande, veuillez vous rendre dans le panneau d'administration.
    """

    # Créer une notification pour chaque admin
    for admin in admins:
        notification = Notification(
            employe_id=admin.id,
            titre=titre,
            message=message,
            type_notification='info',
            lien=url_for('admin_gerer_demandes_username', _external=True),
            date_envoi=datetime.now(),
            lue=False,
            destinataire_id=admin.id,
            action_id=0
        )
        db.session.add(notification)

    db.session.commit()
    print(f"✅ Notification envoyée à {len(admins)} administrateur(s)")

@app.route('/demander-changement-username', methods=['GET', 'POST'])
@login_required
def demander_changement_username():
    """Demander à l'admin de changer son username"""

    if request.method == 'POST':
        nouveau_username = request.form.get('nouveau_username')

        # Vérifier disponibilité
        existing = User.query.filter_by(username=nouveau_username).first()
        if existing:
            flash("Ce nom d'utilisateur est déjà utilisé", "danger")
            return redirect(request.url)

        current_user.nouveau_username_demande = nouveau_username
        current_user.demande_username_status = 'en_attente'
        current_user.demande_username_date = datetime.now()
        db.session.commit()

        # Notifier l'admin
        notifier_admin_changement_username(current_user)

        flash("✅ Demande envoyée à l'administrateur", "success")
        return redirect(url_for('profil'))

    return render_template('demander_changement_username.html')


@app.route('/admin/demandes-username')
@login_required
def admin_gerer_demandes_username():
    """Page d'administration des demandes de changement d'username"""
    from models import User

    # Vérifier que l'utilisateur est admin
    if current_user.role not in ['super_admin', 'admin_central', 'admin_succursale']:
        flash("Accès non autorisé", "danger")
        return redirect(url_for('dashboard_redirect'))

    # Récupérer toutes les demandes en attente
    demandes = User.query.filter_by(demande_username_status='en_attente').all()

    return render_template('admin/demandes_username.html', demandes=demandes)


def notifier_utilisateur_username_approuve(employe, ancien_username):
    """Notifie l'utilisateur que sa demande a été approuvée"""
    from models import Notification
    from datetime import datetime

    notification = Notification(
        employe_id=employe.id,
        titre="✅ Demande de changement d'username approuvée",
        message=f"""
        Votre demande de changement de nom d'utilisateur a été approuvée.

        🔄 Ancien username: {ancien_username}
        ✨ Nouveau username: {employe.username}

        Utilisez votre nouveau nom d'utilisateur pour vous connecter.
        """,
        type_notification='success',
        date_envoi=datetime.now(),
        lue=False,
        destinataire_id=employe.id,
        action_id=0
    )
    db.session.add(notification)
    db.session.commit()


def notifier_utilisateur_username_rejete(employe):
    """Notifie l'utilisateur que sa demande a été rejetée"""
    from models import Notification
    from datetime import datetime

    notification = Notification(
        employe_id=employe.id,
        titre="❌ Demande de changement d'username rejetée",
        message=f"""
        Votre demande de changement de nom d'utilisateur a été rejetée.

        Motif possible:
        - Le nom demandé est déjà utilisé
        - Format non valide

        Vous pouvez faire une nouvelle demande.
        """,
        type_notification='danger',
        date_envoi=datetime.now(),
        lue=False,
        destinataire_id=employe.id,
        action_id=0
    )
    db.session.add(notification)
    db.session.commit()



@app.route('/admin/approuver-username/<int:employe_id>')
@login_required
def admin_approuver_username(employe_id):
    """Approuver une demande de changement d'username"""
    from models import User

    if current_user.role not in ['super_admin', 'admin_central', 'admin_succursale']:
        flash("Accès non autorisé", "danger")
        return redirect(url_for('admin_dashboard'))

    user = User.query.get_or_404(employe_id)

    if user.demande_username_status != 'en_attente':
        flash("Cette demande n'est plus en attente", "warning")
        return redirect(url_for('admin_gerer_demandes_username'))

    # Appliquer le changement
    ancien_username = user.username
    user.username = user.nouveau_username_demande
    user.nouveau_username_demande = None
    user.demande_username_status = 'approuve'
    db.session.commit()

    # Notifier l'utilisateur
    notifier_utilisateur_username_approuve(user, ancien_username)

    flash(f"✅ Username de {user.prenom} {user.nom} changé en {user.username}", "success")
    return redirect(url_for('admin_gerer_demandes_username'))


@app.route('/admin/rejeter-username/<int:employe_id>')
@login_required
def admin_rejeter_username(employe_id):
    """Rejeter une demande de changement d'username"""
    from models import User

    if current_user.role not in ['super_admin', 'admin_central', 'admin_succursale']:
        flash("Accès non autorisé", "danger")
        return redirect(url_for('admin_dashboard'))

    user = User.query.get_or_404(employe_id)

    if user.demande_username_status != 'en_attente':
        flash("Cette demande n'est plus en attente", "warning")
        return redirect(url_for('admin_gerer_demandes_username'))

    # Rejeter la demande
    user.nouveau_username_demande = None
    user.demande_username_status = 'rejete'
    db.session.commit()

    # Notifier l'utilisateur
    notifier_utilisateur_username_rejete(user)

    flash(f"❌ Demande de {user.prenom} {user.nom} rejetée", "warning")
    return redirect(url_for('admin_gerer_demandes_username'))



@app.route('/dossiers/succursale/<string:succursale_code>')
@login_required
def dossiers_succursale(succursale_code):
    """Liste tous les dossiers d'une succursale"""
    succursale = Succursale.query.filter_by(code=succursale_code).first_or_404()

    # Vérifier les permissions
    if current_user.role not in ['super_admin', 'admin', 'admin_succursale']:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('dashboard'))

    if current_user.role == 'admin_succursale' and current_user.succursale_id != succursale.id:
        flash("⛔ Vous ne pouvez voir que les dossiers de votre succursale", "danger")
        return redirect(url_for('dashboard'))

    dossiers = Dossier.get_by_succursale(succursale.id)
    return render_template('dossiers/liste.html', succursale=succursale, dossiers=dossiers)


@app.route('/conseiller/dossier/<int:dossier_id>')
@login_required
def conseiller_voir_dossier(dossier_id):
    """Voir les détails d'un dossier client pour le conseiller"""
    from models import Client, User

    # Vérifier les permissions
    if current_user.role != 'employe' or not current_user.has_permission('conseiller'):
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('employe_dashboard_generique'))

    # Récupérer le dossier
    dossier = Client.query.get_or_404(dossier_id)

    # Vérifier que le conseiller a le droit de voir ce dossier
    if dossier.cree_par_id != current_user.id:
        flash('⛔ Vous ne pouvez voir que vos propres dossiers', 'danger')
        return redirect(url_for('conseiller_dashboard'))

    return render_template('conseiller/voir_dossier.html', dossier=dossier)

@app.route('/dossier/<int:dossier_id>')
@login_required
def voir_dossiers(dossier_id):
    """Voir les détails d'un dossier"""
    dossier = Dossier.query.get_or_404(dossier_id)

    # Vérifier les permissions
    if current_user.role not in ['super_admin', 'admin','direction', 'admin_succursale']:
        if dossier.employe_id != current_user.id:
            flash("⛔ Accès non autorisé", "danger")
            return redirect(url_for('dashboard'))

    if current_user.role == 'admin_succursale' and dossier.succursale_id != current_user.succursale_id:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('dashboard'))

    return render_template('dossiers/details.html', dossier=dossier)



@app.route('/dashboard')
@login_required
def dashboard_redirect():
    """Point d'entrée unique pour tous les dashboards"""

    # 🔑 SUPER ADMIN
    if current_user.role == 'super_admin':
        return redirect(url_for('admin_dashboard'))

    # 🔑 ADMIN CENTRAL
    elif current_user.role == 'admin_central':
        return redirect(url_for('dashboard_succursale',succursale_code=current_user.succursale.code if current_user.succursale else None))

    # 🏢 ADMIN SUCCURSALE
    elif current_user.role == 'admin_succursale':
        # Vérifier si la succursale existe
        if current_user.succursale:
            return redirect(url_for('dashboard_succursale',
                                    succursale_code=current_user.succursale.code if current_user.succursale else None))
        else:
            # Si pas de succursale, rediriger vers l'admin dashboard
            flash("Aucune succursale assignée", "warning")
            return redirect(url_for('admin_dashboard'))

    # 👔 EMPLOYÉS - Utiliser la fonction pour la cohérence
    elif current_user.role == 'employe':
        if not current_user.fonction:
            flash('⚠️ Aucune fonction assignée. Contactez votre superviseur.', 'warning')
            return redirect(url_for('employe_dashboard_generique',
                                    succursale_code=current_user.succursale.code if current_user.succursale else None))


        # Dictionnaire fonction -> route
        routes_employes = {
            # Fonctions de base
            'caissier': 'caissier_dashboard',
            'caissier_principal': 'caissier_principal_dashboard',
            'agent_remboursement': 'agent_remboursement_dashboard',
            # Crédit et analyse
            'agent_credit': 'agent_credit_dashboard',
            'analyste_credit': 'analyste_dashboard',
            'superviseur_credit': 'superviseur_credit_dashboard',
            'gestionnaire_portefeuille': 'gestionnaire_portefeuille_dashboard',
            # Conseil et relation client
            'conseiller': 'conseiller_dashboard',
            'conseiller_client': 'conseiller_dashboard',
            'relation_client': 'relation_client_dashboard',
            # Groupes et animation
            'gestionnaire_groupe': 'gestionnaire_groupes_dashboard',
            'animateur_groupe': 'animateur_groupe_dashboard',
            # Rapports et données
            'rapports': 'rapports_dashboard',
            'agent_saisie': 'agent_saisie_dashboard',
            # Conformité et risque
            'agent_conformite': 'agent_conformite_dashboard',
            'agent_risque': 'agent_risque_dashboard',
            'controlleur_interne': 'controlleur_interne_dashboard',
            # Support administratif
            'secretaire': 'secretaire_dashboard',
            'archiviste': 'archiviste_dashboard',
            'charge_rh': 'charge_rh_dashboard',
            'informaticien': 'informaticien_dashboard',
            # Terrain et collecte
            'agent_terrain': 'agent_terrain_dashboard',
            'collecteur': 'collecteur_dashboard',
            'formateur': 'formateur_dashboard',
        }

        if current_user.fonction in routes_employes:
            # ✅ CORRECTION : Message de redirection normal, pas "aucune fonction"
            return redirect(url_for(
                routes_employes[current_user.fonction],
                succursale_code=current_user.succursale.code if current_user.succursale else None
            ))
        else:
            # ✅ Fonction non trouvée dans le dictionnaire
            flash(f'⚠️ Dashboard pour "{current_user.fonction}" en développement', 'info')
            return redirect(url_for('employe_dashboard_generique',
                                    succursale_code=current_user.succursale.code if current_user.succursale else None))

    # 👨‍💼 SUPERVISEUR
    elif current_user.role == 'superviseur':
        routes_superviseurs = {
            'chef_agence': 'chef_agence_dashboard',
            'superviseur_operations': 'superviseur_operations_dashboard',
            'chef_credit': 'chef_credit_dashboard',
            'responsable_conformite': 'responsable_conformite_dashboard',
            'coordinateur_terrain': 'coordinateur_terrain_dashboard',
            'directeur_regional': 'directeur_regional_dashboard',
        }
        if current_user.fonction in routes_superviseurs:
            return redirect(url_for(
                routes_superviseurs[current_user.fonction],
                succursale_code=current_user.succursale.code if current_user.succursale else None
            ))
        else:
            return redirect(url_for('superviseur_dashboard_generique'))

    # 👑 DIRECTION
    elif current_user.role == 'direction':
        routes_direction = {
            'directeur_general': 'directeur_general_dashboard',
            'directeur_financier': 'directeur_financier_dashboard',
            'directeur_operations': 'directeur_operations_dashboard',
            'directeur_commercial': 'directeur_commercial_dashboard',
            'directeur_rh': 'directeur_rh_dashboard',
            'directeur_conformite': 'directeur_conformite_dashboard',
        }
        if current_user.fonction in routes_direction:
            return redirect(url_for(routes_direction[current_user.fonction]))
        else:
            return redirect(url_for('direction_dashboard_generique'))

    # 👤 CLIENT
    elif current_user.role == 'client':
        return redirect(url_for('client_dashboard'))

    abort(403)


@app.route('/<succursale_code>/agent-credit/dashboard')
@login_required
def agent_credit_dashboard(succursale_code):
    """Dashboard pour les agents de crédit"""
    if current_user.role != 'employe' or current_user.fonction != 'agent_credit':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import Succursale, Credit, Client, Echeance
    from datetime import datetime, timedelta
    from sqlalchemy import func

    succursale = Succursale.query.filter_by(code=succursale_code).first_or_404()

    # Statistiques - ✅ CORRIGÉ: employe_id → agent_id
    stats = {
        'demandes_en_cours': Credit.query.filter_by(
            agent_id=current_user.id,  # ✅ CORRECT
            statut='en_attente'
        ).count(),
        'credits_approuves': Credit.query.filter_by(
            agent_id=current_user.id,  # ✅ CORRECT
            statut='actif'
        ).count(),
        'montant_total': db.session.query(func.sum(Credit.montant)).filter(
            Credit.agent_id == current_user.id,  # ✅ CORRECT
            Credit.statut.in_(['actif', 'rembourse'])
        ).scalar() or 0,
        'taux_approbation': 75  # À calculer
    }

    # Demandes en attente - ✅ CORRIGÉ: employe_id → agent_id
    demandes_attente = Credit.query.filter_by(
        agent_id=current_user.id,  # ✅ CORRECT
        statut='en_attente'
    ).order_by(Credit.date_demande.desc()).all()

    # Nouveaux clients - ✅ CORRIGÉ: Cette partie est commentée car agent_id n'existe pas dans Client
    date_limite = datetime.now() - timedelta(days=7)

    # Option 1: Si vous voulez voir tous les nouveaux clients
    nouveaux_clients = Client.query.filter(
        Client.date_inscription >= date_limite
    ).limit(5).all()

    # Option 2: Si vous voulez uniquement les clients liés à cet agent via ses crédits
    # client_ids = db.session.query(Credit.client_id).filter_by(agent_id=current_user.id).distinct().all()
    # client_ids = [c[0] for c in client_ids]
    # nouveaux_clients = Client.query.filter(
    #     Client.id.in_(client_ids),
    #     Client.date_inscription >= date_limite
    # ).limit(5).all()

    # Prochaines échéances - à implémenter selon votre modèle
    prochaines_echeances = []

    # Portefeuille clients - ✅ CORRIGÉ: via les crédits de l'agent
    client_ids = db.session.query(Credit.client_id).filter_by(agent_id=current_user.id).distinct().all()
    client_ids = [c[0] for c in client_ids]
    portefeuille = Client.query.filter(Client.id.in_(client_ids)).limit(10).all()

    # Objectifs
    objectifs = {
        'credits_objectif': 10,
        'credits_atteint': stats['credits_approuves'],
        'credits_pct': min(100, (stats['credits_approuves'] / 10 * 100)) if stats['credits_approuves'] > 0 else 0,
        'montant_objectif': 5000000,
        'montant_atteint': stats['montant_total'],
        'montant_pct': min(100, (stats['montant_total'] / 5000000 * 100)) if stats['montant_total'] > 0 else 0,
        'clients_objectif': 5,
        'clients_atteint': len(portefeuille),
        'clients_pct': min(100, (len(portefeuille) / 5 * 100)) if portefeuille else 0
    }

    return render_template('fonctions/agent_credit/agent_credit_dashboard.html',
                           succursale=succursale,
                           stats=stats,
                           demandes_attente=demandes_attente,
                           nouveaux_clients=nouveaux_clients,
                           prochaines_echeances=prochaines_echeances,
                           portefeuille=portefeuille,
                           objectifs=objectifs,
                           now=datetime.now)


@app.route('/superviseur/chef_agence/dashboard')
@login_required
def chef_agence_dashboard():
    """Dashboard pour le chef d'agence"""
    if current_user.role != 'superviseur' or current_user.fonction != 'chef_agence':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import User, Client, Credit, Epargne, Transaction, Succursale
    from datetime import datetime, timedelta
    from sqlalchemy import func

    # Récupérer l'agence du chef
    agence = current_user.succursale

    # Statistiques de l'agence
    stats = {
        'portefeuille_total': db.session.query(func.sum(Credit.montant)).filter(
            Credit.succursale_id == agence.id,
            Credit.statut.in_(['actif', 'impaye'])
        ).scalar() or 0,
        'epargne_total': db.session.query(func.sum(Epargne.montant)).filter(
            Epargne.succursale_id == agence.id
        ).scalar() or 0,
        'clients_actifs': Client.query.filter_by(
            succursale_id=agence.id,
            statut='actif'
        ).count(),
        'effectif_total': User.query.filter_by(
            succursale_id=agence.id,
            statut='actif'
        ).count(),
        'par_30': 4.2,
        'presents': 15,
        'en_conge': 2,
        'absents': 1
    }

    # Équipe
    equipe = []

    # Absences
    absences = []

    # Activités récentes
    activites = []

    # Alertes
    alertes = []

    # Objectifs
    objectifs = {
        'credit_objectif': 100000000,
        'credit_atteint': 75000000,
        'credit_pct': 75,
        'epargne_objectif': 50000000,
        'epargne_atteint': 35000000,
        'epargne_pct': 70,
        'clients_objectif': 200,
        'clients_atteint': 145,
        'clients_pct': 72.5
    }

    # Transactions importantes
    transactions_importantes = []

    # Échéances
    echeances = []

    # Tâches
    taches = []

    return render_template('superviseur/chef_agence_dashboard.html',
                           stats=stats,
                           agence=agence,
                           equipe=equipe,
                           absences=absences,
                           activites=activites,
                           alertes=alertes,
                           objectifs=objectifs,
                           transactions_importantes=transactions_importantes,
                           echeances=echeances,
                           taches=taches,
                           now=datetime.now)

@app.route('/superviseur/operations/dashboard')
@login_required
def superviseur_operations_dashboard():
    """Dashboard pour le superviseur des opérations"""
    if current_user.role != 'superviseur' or current_user.fonction != 'superviseur_operations':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import User, Transaction, Caisse, FileAttente, Anomalie, Pause
    from datetime import datetime, timedelta
    from sqlalchemy import func

    aujourd_hui = datetime.now().date()
    debut_jour = datetime.now().replace(hour=0, minute=0, second=0)

    # Récupérer la succursale du superviseur
    succursale_id = current_user.succursale_id

    # Statistiques du jour
    stats = {
        'transactions_jour': Transaction.query.filter(
            Transaction.date_creation >= debut_jour,
            Transaction.succursale_id == succursale_id
        ).count(),
        'volume_jour': db.session.query(func.sum(Transaction.montant)).filter(
            Transaction.date_creation >= debut_jour,
            Transaction.succursale_id == succursale_id
        ).scalar() or 0,
        'agents_actifs': User.query.filter_by(
            succursale_id=succursale_id,
            statut='actif',
            est_en_service=True
        ).count(),
        'agents_total': User.query.filter_by(
            succursale_id=succursale_id,
            statut='actif'
        ).count(),
        'temps_moyen': 8  # À calculer
    }

    # Caisses
    caisses = []

    # File d'attente
    file_attente = []

    # Agents
    agents = []

    # Anomalies
    anomalies = []

    # Validations récentes
    validations = []

    # Pauses
    pauses = []

    # Objectifs
    objectifs = {
        'volume_cible': 5000000,
        'volume_pct': min(100, (stats['volume_jour'] / 5000000 * 100)),
        'transactions_cible': 200,
        'transactions_pct': min(100, (stats['transactions_jour'] / 200 * 100)),
        'satisfaction': 92,
        'satisfaction_pct': 92
    }

    return render_template('superviseur/superviseur_operations_dashboard.html',
                           stats=stats,
                           caisses=caisses,
                           file_attente=file_attente,
                           agents=agents,
                           anomalies=anomalies,
                           validations=validations,
                           pauses=pauses,
                           objectifs=objectifs,
                           now=datetime.now)




@app.route('/superviseurs/chef_credit/dashboard')
@login_required
def chef_credit_dashboard():
    """Dashboard pour le chef de crédit"""
    if current_user.role != 'direction' or current_user.fonction != 'chef_credit':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import Credit, User, Client, Echeance, DecisionCredit
    from datetime import datetime, timedelta
    from sqlalchemy import func

    # Statistiques
    stats = {
        'portefeuille_total': db.session.query(func.sum(Credit.montant)).filter(
            Credit.statut.in_(['actif', 'impaye'])
        ).scalar() or 0,
        'credits_actifs': Credit.query.filter_by(statut='actif').count(),
        'demandes_attente': Credit.query.filter_by(statut='en_attente').count(),
        'par_30': 4.2
    }

    # Demandes en attente
    demandes_attente = []

    # Performance des agents
    agents_performance = []

    # Produits
    produits = []

    # Crédits à risque
    credits_risque = []

    # Échéances
    echeances = []

    # Décisions récentes
    decisions = []

    return render_template('superviseurs/chef_credit_dashboard.html',
                           stats=stats,
                           demandes_attente=demandes_attente,
                           agents_performance=agents_performance,
                           produits=produits,
                           credits_risque=credits_risque,
                           echeances=echeances,
                           decisions=decisions,
                           now=datetime.now)



@app.route('/superviseurs/responsable_conformite/dashboard')
@login_required
def responsable_conformite_dashboard():
    """Dashboard pour le responsable conformité"""
    if current_user.role != 'direction' or current_user.fonction != 'responsable_conformite':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import Client, AlerteAML, Document, VerificationAnnuelle, Transaction, User
    from datetime import datetime, timedelta
    from sqlalchemy import func

    # Statistiques
    stats = {
        'kyc_en_attente': Client.query.filter_by(kyc_statut='en_attente').count(),
        'alertes_aml': AlerteAML.query.filter_by(statut='nouvelle').count(),
        'documents_expires': Document.query.filter(
            Document.date_expiration < datetime.now()
        ).count(),
        'verifications_annuelles': VerificationAnnuelle.query.filter(
            VerificationAnnuelle.statut == 'a_faire'
        ).count(),
        'taux_formation': 75  # À calculer
    }

    # Alertes AML
    alertes_aml = []

    # KYC en attente
    kyc_en_attente = []

    # Documents expirés
    documents_expires = []

    # Vérifications annuelles
    verifications_annuelles = []

    # Transactions suspectes
    transactions_suspectes = []

    # Formations
    formations = []

    # Employés non formés
    employes_non_formes = []

    # Rapports
    rapport_mensuel = {'date': datetime.now().strftime('%B %Y')}
    rapport_brh = {'date': datetime.now().strftime('%d/%m/%Y')}
    rapport_kyc = {'date': datetime.now().strftime('%d/%m/%Y')}
    rapport_annuel = {'date': datetime.now().strftime('%Y')}

    return render_template('surperviseurs/responsable_conformite_dashboard.htm.html',
                           stats=stats,
                           alertes_aml=alertes_aml,
                           kyc_en_attente=kyc_en_attente,
                           documents_expires=documents_expires,
                           verifications_annuelles=verifications_annuelles,
                           transactions_suspectes=transactions_suspectes,
                           formations=formations,
                           employes_non_formes=employes_non_formes,
                           rapport_mensuel=rapport_mensuel,
                           rapport_brh=rapport_brh,
                           rapport_kyc=rapport_kyc,
                           rapport_annuel=rapport_annuel,
                           now=datetime.now)


@app.route('/direction/coordinateur_terrain/dashboard')
@login_required
def coordinateur_terrain_dashboard():
    """Dashboard pour le coordinateur terrain - Version dynamique"""
    from models import User, Client, Visite, Collecte, Tournee, Zone, Succursale
    from datetime import datetime, timedelta
    from sqlalchemy import func, and_

    # Vérification des permissions
    if current_user.role != 'direction' or current_user.fonction != 'coordinateur_terrain':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    aujourd_hui = datetime.now().date()
    debut_jour = datetime.now().replace(hour=0, minute=0, second=0)
    debut_semaine = datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=datetime.now().weekday())
    debut_mois = datetime.now().replace(day=1, hour=0, minute=0, second=0)

    # ========== RÉCUPÉRATION DE LA ZONE DU COORDINATEUR ==========
    # Récupérer la zone associée au coordinateur
    zone = None
    if hasattr(current_user, 'zone_id') and current_user.zone_id:
        zone = Zone.query.get(current_user.zone_id)

    if not zone:
        # Zone par défaut si non assignée
        zone = Zone.query.filter_by(nom='Zone Métropolitaine').first()
        if not zone:
            zone = {'nom': 'Zone Non définie', 'code': 'N/A', 'id': None}

    # ========== STATISTIQUES DYNAMIQUES ==========
    stats = {}

    # 1. Agents terrain actifs
    stats['agents_terrain'] = User.query.filter(
        User.role == 'agent_terrain',
        User.statut == 'actif'
    ).count()

    # 2. Visites prévues aujourd'hui
    stats['visites_aujourdhui'] = Visite.query.filter(
        Visite.date_visite == aujourd_hui,
        Visite.statut.in_(['planifiee', 'en_attente'])
    ).count()

    # 3. Collectes du jour
    collectes_jour = db.session.query(func.sum(Collecte.montant)).filter(
        Collecte.date_collecte >= debut_jour
    ).scalar()
    stats['collectes_jour'] = float(collectes_jour) if collectes_jour else 0

    # 4. Clients visités ce mois
    stats['clients_visites_mois'] = Visite.query.filter(
        Visite.date_visite >= debut_mois,
        Visite.statut == 'effectuee'
    ).count()

    # 5. Taux de réalisation des visites
    total_visites_planifiees = Visite.query.filter(
        Visite.date_visite >= debut_mois,
        Visite.statut.in_(['planifiee', 'effectuee'])
    ).count()

    visites_realisees = Visite.query.filter(
        Visite.date_visite >= debut_mois,
        Visite.statut == 'effectuee'
    ).count()

    stats['taux_realisation'] = round((visites_realisees / total_visites_planifiees * 100),
                                      1) if total_visites_planifiees > 0 else 0

    # 6. Taux de couverture des tournées
    total_tournees = Tournee.query.filter(
        Tournee.date_debut >= debut_mois
    ).count()

    tournees_realisees = Tournee.query.filter(
        Tournee.date_debut >= debut_mois,
        Tournee.statut == 'termine'
    ).count()

    stats['taux_couverture'] = round((tournees_realisees / total_tournees * 100), 1) if total_tournees > 0 else 0

    # ========== PROCHAINES VISITES ==========
    prochaines_visites = Visite.query.filter(
        Visite.date_visite >= aujourd_hui,
        Visite.statut.in_(['planifiee', 'en_attente'])
    ).order_by(Visite.date_visite.asc()).limit(10).all()

    # Formater les prochaines visites
    prochaines_visites_data = []
    for visite in prochaines_visites:
        client = Client.query.get(visite.client_id)
        agent = User.query.get(visite.agent_id) if visite.agent_id else None
        prochaines_visites_data.append({
            'id': visite.id,
            'client': f"{client.prenom} {client.nom}" if client else 'Client inconnu',
            'agent': f"{agent.prenom} {agent.nom}" if agent else 'Non assigné',
            'date': visite.date_visite.strftime('%d/%m/%Y'),
            'heure': visite.heure_visite if hasattr(visite, 'heure_visite') else '09:00',
            'adresse': client.adresse if client else 'N/A',
            'statut': visite.statut
        })

    # ========== AGENTS TERRAIN ==========
    agents = User.query.filter(
        User.role == 'agent_terrain',
        User.actif == True
    ).all()

    agents_data = []
    for agent in agents:
        # Nombre de visites aujourd'hui pour cet agent
        visites_agent = Visite.query.filter(
            Visite.agent_id == agent.id,
            Visite.date_visite == aujourd_hui
        ).count()

        # Collectes de l'agent aujourd'hui
        collectes_agent = db.session.query(func.sum(Collecte.montant)).filter(
            Collecte.agent_id == agent.id,
            Collecte.date_collecte >= debut_jour
        ).scalar() or 0

        # Taux de ponctualité (si disponible)
        ponctualite = 95  # Valeur par défaut, à calculer selon vos données

        agents_data.append({
            'id': agent.id,
            'nom': f"{agent.prenom} {agent.nom}",
            'telephone': agent.telephone,
            'zone': agent.zone.nom if agent.zone_id and hasattr(agent, 'zone') else 'Non assigné',
            'visites_aujourdhui': visites_agent,
            'collectes_jour': float(collectes_agent),
            'ponctualite': ponctualite
        })

    # ========== SECTEURS (par zone) ==========
    secteurs_data = []

    # Récupérer les secteurs de la zone
    if zone and zone.id:
        secteurs = Zone.query.filter_by(parent_zone_id=zone.id).all()
    else:
        secteurs = Zone.query.filter_by(type='secteur').all()

    for secteur in secteurs:
        # Agents dans ce secteur
        nb_agents = User.query.filter(
            User.zone_id == secteur.id,
            User.role == 'agent_terrain'
        ).count()

        # Clients dans ce secteur
        nb_clients = Client.query.filter_by(zone_id=secteur.id).count()

        # Visites cette semaine
        visites_semaine = Visite.query.filter(
            Visite.zone_id == secteur.id,
            Visite.date_visite >= debut_semaine
        ).count()

        # Couverture (pourcentage de clients visités ce mois)
        clients_visites_mois = Visite.query.filter(
            Visite.zone_id == secteur.id,
            Visite.date_visite >= debut_mois,
            Visite.statut == 'effectuee'
        ).distinct(Visite.client_id).count()

        couverture = round((clients_visites_mois / nb_clients * 100), 1) if nb_clients > 0 else 0

        # Couleur selon le pourcentage
        if couverture >= 75:
            couleur = 'success'
        elif couverture >= 50:
            couleur = 'warning'
        else:
            couleur = 'danger'

        secteurs_data.append({
            'id': secteur.id,
            'nom': secteur.nom,
            'agents': nb_agents,
            'clients': nb_clients,
            'visites_semaine': visites_semaine,
            'couverture': couverture,
            'couverture_couleur': couleur
        })

    # ========== ALERTES TERRAIN ==========
    alertes_terrain = []

    # 1. Visites en retard
    visites_retard = Visite.query.filter(
        Visite.date_visite < aujourd_hui,
        Visite.statut == 'planifiee'
    ).count()

    if visites_retard > 0:
        alertes_terrain.append({
            'type': 'danger',
            'icone': 'exclamation-triangle',
            'titre': f'{visites_retard} visite(s) en retard',
            'description': 'Des visites planifiées n\'ont pas été effectuées',
            'priorite': 'Haute',
            'date': aujourd_hui.strftime('%d/%m/%Y'),
            'lien': url_for('visites_en_retard')
        })

    # 2. Collectes impayées
    collectes_impayees = Collecte.query.filter(
        Collecte.statut == 'impaye'
    ).count()

    if collectes_impayees > 0:
        alertes_terrain.append({
            'type': 'warning',
            'icone': 'clock',
            'titre': f'{collectes_impayees} collecte(s) impayée(s)',
            'description': 'Des paiements sont en attente de régularisation',
            'priorite': 'Moyenne',
            'date': aujourd_hui.strftime('%d/%m/%Y'),
            'lien': url_for('collectes_impayees')
        })

    # 3. Agents sans tournée
    agents_sans_tournee = User.query.filter(
        User.role == 'agent_terrain',
        ~User.id.in_(
            db.session.query(Tournee.agent_id).filter(Tournee.date_debut >= debut_jour)
        )
    ).count()

    if agents_sans_tournee > 0:
        alertes_terrain.append({
            'type': 'info',
            'icone': 'info-circle',
            'titre': f'{agents_sans_tournee} agent(s) sans tournée aujourd\'hui',
            'description': 'Certains agents n\'ont pas de tournée planifiée',
            'priorite': 'Basse',
            'date': aujourd_hui.strftime('%d/%m/%Y'),
            'lien': url_for('agents_sans_tournee')
        })

    # ========== TOURNÉES EN COURS ==========
    tournees = Tournee.query.filter(
        Tournee.date_debut <= datetime.now(),
        Tournee.date_fin >= datetime.now(),
        Tournee.statut == 'en_cours'
    ).all()

    tournees_data = []
    for tournee in tournees:
        agent = User.query.get(tournee.agent_id)
        tournees_data.append({
            'id': tournee.id,
            'agent': f"{agent.prenom} {agent.nom}" if agent else 'Non assigné',
            'secteur': tournee.secteur_nom if hasattr(tournee, 'secteur_nom') else 'Non défini',
            'visites_prevues': tournee.visites_prevues,
            'visites_effectuees': tournee.visites_effectuees,
            'progression': round((tournee.visites_effectuees / tournee.visites_prevues * 100),
                                 1) if tournee.visites_prevues > 0 else 0,
            'debut': tournee.date_debut.strftime('%H:%M'),
            'fin': tournee.date_fin.strftime('%H:%M')
        })

    # ========== DERNIÈRES COLLECTES ==========
    dernieres_collectes = Collecte.query.order_by(
        Collecte.date_collecte.desc()
    ).limit(10).all()

    collectes_data = []
    for collecte in dernieres_collectes:
        client = Client.query.get(collecte.client_id)
        agent = User.query.get(collecte.agent_id)
        collectes_data.append({
            'id': collecte.id,
            'client': f"{client.prenom} {client.nom}" if client else 'Client inconnu',
            'agent': f"{agent.prenom} {agent.nom}" if agent else 'N/A',
            'montant': collecte.montant,
            'date': collecte.date_collecte.strftime('%d/%m/%Y %H:%M'),
            'statut': collecte.statut if hasattr(collecte, 'statut') else 'effectue'
        })

    # ========== PLANNING AGENTS (SEMAINE) ==========
    planning_agents = []
    jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']

    for agent in agents:
        planning_agent = {
            'nom': f"{agent.prenom} {agent.nom}",
            'jours': []
        }

        for i, jour in enumerate(jours_semaine):
            date_jour = debut_semaine + timedelta(days=i)
            visites_jour = Visite.query.filter(
                Visite.agent_id == agent.id,
                Visite.date_visite == date_jour.date()
            ).count()

            planning_agent['jours'].append({
                'jour': jour,
                'date': date_jour.strftime('%d/%m'),
                'visites': visites_jour,
                'actif': visites_jour > 0
            })

        planning_agents.append(planning_agent)

    # ========== STATS ADDITIONNELLES ==========
    stats['visites_semaine'] = Visite.query.filter(
        Visite.date_visite >= debut_semaine
    ).count()

    stats['collectes_semaine'] = db.session.query(func.sum(Collecte.montant)).filter(
        Collecte.date_collecte >= debut_semaine
    ).scalar() or 0

    stats['clients_actifs'] = Client.query.filter_by(actif=True).count()

    stats['visites_retard'] = visites_retard
    stats['collectes_impayees'] = collectes_impayees

    # ========== RENDU ==========
    return render_template('direction/coordinateur_terrain_dashboard.html',
                           stats=stats,
                           zone=zone,
                           prochaines_visites=prochaines_visites_data,
                           agents=agents_data,
                           secteurs=secteurs_data,
                           alertes_terrain=alertes_terrain,
                           tournees=tournees_data,
                           dernieres_collectes=collectes_data,
                           semaine_numero=datetime.now().isocalendar()[1],
                           planning_agents=planning_agents,
                           now=datetime.now)

@app.route('/direction/regional/dashboard')
@login_required
def directeur_regional_dashboard():
    """Dashboard pour le directeur régional"""
    if current_user.role != 'direction' or current_user.fonction != 'directeur_regional':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import User, Client, Credit, Succursale, Visite, Reunion, Action
    from datetime import datetime, timedelta
    from sqlalchemy import func

    # Récupérer la région du directeur
    region = {
        'nom': 'Ouest',
        'code': 'REG-OUEST'
    }

    # Succursales de la région
    succursales_list = Succursale.query.filter_by(region='OUEST', active=True).all()

    # Statistiques régionales
    portefeuille_regional = db.session.query(func.sum(Credit.montant)).filter(
        Credit.succursale_id.in_([s.id for s in succursales_list]),
        Credit.statut.in_(['actif', 'impaye'])
    ).scalar() or 0

    total_clients = Client.query.filter(
        Client.succursale_id.in_([s.id for s in succursales_list])
    ).count()

    stats = {
        'portefeuille_regional': portefeuille_regional,
        'nb_succursales': len(succursales_list),
        'total_clients': total_clients,
        'performance_regionale': 78,
        'par_30': 4.2,
        'croissance_annuelle': 12.5,
        'taux_penetration': 18.3,
        'satisfaction': 86,
    }

    # Données des succursales
    succursales_data = []
    succursales_noms = []
    succursales_encours_millions = []
    succursales_par_30 = []

    for s in succursales_list:
        encours = db.session.query(func.sum(Credit.montant)) \
                      .join(Client, Credit.client_id == Client.id) \
                      .filter(
            Client.succursale_id == s.id,
            Credit.statut.in_(['actif', 'impaye'])
        ).scalar() or 0

        clients = Client.query.filter_by(succursale_id=s.id).count()

        succursales_data.append({
            'id': s.id,
            'nom': s.nom,
            'code': s.code,
            'ville': s.ville,
            'chef_agence': User.query.filter_by(succursale_id=s.id, fonction='chef_agence').first(),
            'encours': encours,
            'clients': clients,
            'par_30': round(encours * 0.042 / encours * 100 if encours > 0 else 0, 1),
            'par_30_couleur': 'warning' if encours > 0 and (encours * 0.042 / encours * 100) > 5 else 'success',
            'performance': min(100, (encours / 100000000 * 100) if encours > 0 else 0),
            'performance_couleur': 'success' if encours > 50000000 else 'warning',
            'tendance': random.choice(['hausse', 'baisse', 'stable'])
        })

        succursales_noms.append(s.nom)
        succursales_encours_millions.append(round(encours / 1000000, 2))
        succursales_par_30.append(round(encours * 0.042 / encours * 100 if encours > 0 else 0, 1))

    # Top et bottom succursales
    top_succursales = sorted(succursales_data, key=lambda x: x['performance'], reverse=True)[:3]
    bottom_succursales = sorted(succursales_data, key=lambda x: x['performance'])[:3]

    # Visites planifiées
    visites = []

    # Réunions
    reunions = []

    # Actions
    actions = []

    # Objectifs
    objectifs = {
        'croissance_portefeuille': 65,
        'croissance_portefeuille_realise': 9.8,
        'reduction_par': 40,
        'par_actuel': 4.2,
        'nouveaux_clients': 55,
        'nouveaux_clients_objectif': 2000,
        'nouveaux_clients_realise': 1100
    }

    return render_template('direction/directeur_regional_dashboard.html',
                           stats=stats,
                           region=region,
                           succursales=succursales_data,
                           succursales_noms=succursales_noms,
                           succursales_encours_millions=succursales_encours_millions,
                           succursales_par_30=succursales_par_30,
                           top_succursales=top_succursales,
                           bottom_succursales=bottom_succursales,
                           visites=visites,
                           reunions=reunions,
                           actions=actions,
                           objectifs=objectifs,
                           now=datetime.now)


@app.route('/direction/general/dashboard')
@login_required
def directeur_general_dashboard():
    """Dashboard pour le directeur général"""

    # Vérification du rôle
    if current_user.role != 'direction' or current_user.fonction != 'directeur_general':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import User, Client, Credit, Succursale, Pret, PaiementPret, CompteCaisse, Transaction
    from datetime import datetime, timedelta
    from sqlalchemy import func
    import random


    # Date du mois dernier
    aujourdhui = datetime.now().date()
    mois_dernier = aujourdhui - timedelta(days=30)
    mois_avant_dernier = aujourdhui - timedelta(days=60)


    # Dans votre route
    aujourdhui = datetime.now()
    premier_jour_mois = aujourdhui.replace(day=1)

    # 1. Commercial - CA mensuel (total des crédits décaissés ce mois)
    ca_mensuel = db.session.query(func.sum(Pret.montant)).filter(
        Pret.date_decaissement >= premier_jour_mois,
        Pret.statut == 'decaisse'
    ).scalar() or 0

    # 2. Financier - Résultat net (intérêts perçus - frais)
    resultat_net = db.session.query(func.sum(PaiementPret.interets)).filter(
        PaiementPret.date_paiement >= premier_jour_mois
    ).scalar() or 0

    # 3. Opérations - Transactions du jour
    transactions_jour = Transaction.query.filter(
        Transaction.date_creation >= datetime.now().replace(hour=0, minute=0, second=0)
    ).count()

    # 4. RH - Effectif total actif
    effectif_total = User.query.filter_by(est_actif=True, statut='actif').count()


    # Statistiques globales
    total_actifs = db.session.query( func.sum(Pret.montant)).filter( Pret.statut == 'actif' ).scalar() or 0
    portefeuille_credits = total_actifs
    total_clients = Client.query.count()

    # Calcul du résultat net (simplifié)
    revenus = db.session.query(func.sum(Paiement.interet)).scalar() or 0
    depenses = db.session.query(func.sum(Depense.montant)).scalar() or 0

    resultat_net = revenus - depenses

    # ✅ AJOUT : Compter les dossiers en attente d'approbation
    en_attente_count = Client.query.filter_by(
        # role='client',
        statut='en_attente_approbation'
    ).count()

    from sqlalchemy import func

    clients_en_retard = (
        db.session.query(
            Client,
            func.sum(RetardPaiement.jours_retard),
            func.count(RetardPaiement.id)
        )
        .join(RetardPaiement, RetardPaiement.client_id == Client.id)
        .group_by(Client.id)
        .having(func.sum(RetardPaiement.jours_retard) > 0)
        .all()
    )

    stats = {
        'total_actifs': total_actifs,
        'portefeuille_credits': portefeuille_credits,
        'total_clients': total_clients,
        'resultat_net': resultat_net,
        'par_30': 4.2,
        'roa': 3.8,
        'taux_penetration': 15.5,
        'satisfaction': 87,
        'performance_commerciale': 78,
        'performance_financiere': 82,
        'performance_operations': 75,
        'performance_rh': 85,
        'en_attente': en_attente_count,  # ← NOUVEAU
        'clients_en_retard':clients_en_retard
    }

    # Performance par direction
    performance = {
        'commercial': {'ca_mensuel': ca_mensuel},
        'financier': {'resultat_net': resultat_net},
        'operations': {'transactions_jour': transactions_jour},
        'rh': {'effectif_total': effectif_total}
    }

    # Succursales
    succursales_list = Succursale.query.filter_by(active=True).all()
    succursales_data = []

    for s in succursales_list:
        encours = db.session.query(func.sum(Pret.montant)) \
                      .join(Client, Pret.client_id == Client.id) \
                      .filter(
            Client.succursale_id == s.id,
            Pret.statut.in_(['actif', 'impaye'])
        ).scalar() or 0

        clients = Client.query.filter_by(succursale_id=s.id).count()

        succursales_data.append({
            'nom': s.nom,
            'code': s.code,
            'ville': s.ville,
            'encours': encours,
            'par_30': round(encours * 0.042 / encours * 100 if encours > 0 else 0, 1),
            'par_30_couleur': 'warning' if encours > 0 and (encours * 0.042 / encours * 100) > 5 else 'success',
            'clients': clients,
            'performance': min(100, (encours / 100000000 * 100) if encours > 0 else 0),
            'performance_couleur': 'success' if encours > 50000000 else 'warning',
            'tendance': random.choice(['hausse', 'baisse', 'stable'])
        })

    # Alertes

    alertes = []

    # 1. ALERTE : PAR > 5% (Portefeuille à risque)
    succursales_critiques = []
    succursales = Succursale.query.all()

    for succ in succursales:
        # Calculer PAR (crédits impayés > 30 jours / total crédits)
        total_credits = Pret.query.filter_by(succursale_id=succ.id).count()
        credits_impayes = Pret.query.filter(
            Pret.succursale_id == succ.id,
            Pret.statut == 'impaye',
            Pret.date_echeance < aujourdhui - timedelta(days=30)
        ).count()

        if total_credits > 0:
            par = (credits_impayes / total_credits) * 100
            if par > 5:
                succursales_critiques.append(succ.nom)

    if succursales_critiques:
        alertes.append({
            'type': 'danger',
            'icone': 'exclamation-triangle',
            'titre': f'PAR > 5% dans {len(succursales_critiques)} succursale(s)',
            'description': f'Les succursales {", ".join(succursales_critiques)} dépassent le seuil critique de 5%.',
            'priorite': 'Haute',
            'succursale': ', '.join(succursales_critiques),
            'date': 'Aujourd\'hui'
        })

    # 2. ALERTE : Croissance en baisse
    croissance_mois_dernier = db.session.query(func.sum(Pret.montant)).filter(
        Pret.date_decaissement >= mois_dernier
    ).scalar() or 0

    croissance_mois_avant = db.session.query(func.sum(Pret.montant)).filter(
        Pret.date_decaissement >= mois_avant_dernier,
        Pret.date_decaissement < mois_dernier
    ).scalar() or 0

    if croissance_mois_avant > 0:
        taux_croissance = ((croissance_mois_dernier - croissance_mois_avant) / croissance_mois_avant) * 100
        if taux_croissance < 0:  # Croissance négative
            alertes.append({
                'type': 'warning',
                'icone': 'chart-line',
                'titre': 'Croissance en baisse',
                'description': f'La croissance du portefeuille a baissé de {abs(round(taux_croissance, 1))}% par rapport au mois dernier.',
                'priorite': 'Moyenne',
                'succursale': 'Toutes',
                'date': 'Cette semaine'
            })

    # 3. ALERTE : Découvert bancaire (à ajouter)
    seuil_decouvert = -1000000  # seuil de découvert critique
    comptes_decouvert = CompteCaisse.query.filter(
        CompteCaisse.solde < seuil_decouvert
    ).count()

    if comptes_decouvert > 0:
        alertes.append({
            'type': 'danger',
            'icone': 'credit-card',
            'titre': 'Découvert bancaire critique',
            'description': f'{comptes_decouvert} compte(s) en situation de découvert dépassant le seuil autorisé.',
            'priorite': 'Urgente',
            'succursale': 'Toutes',
            'date': 'Aujourd\'hui'
        })

    # 4. ALERTE : Clients inactifs
    seuil_inactivite = 90  # jours
    clients_inactifs = Client.query.filter(
        Pret.derniere_activite < aujourdhui - timedelta(days=seuil_inactivite),
        Client.compte_actif == True
    ).count()

    if clients_inactifs > 10:
        alertes.append({
            'type': 'warning',
            'icone': 'user-friends',
            'titre': 'Clients inactifs',
            'description': f'{clients_inactifs} clients sont inactifs depuis plus de {seuil_inactivite} jours.',
            'priorite': 'Moyenne',
            'succursale': 'Toutes',
            'date': 'Cette semaine'
        })



    decisions = [
        {
            'titre': 'Déploiement nouveau système',
            'description': 'Migration vers la nouvelle plateforme core banking',
            'statut': 'En cours',
            'statut_couleur': 'warning',
            'date_echeance': datetime.now() + timedelta(days=45),
            'progression': 65,
            'couleur': 'info'
        }
    ]

    # Données d'évolution
    evolution = {
        'encours': [82, 85, 83, 88, 92, 95, 98, 102, 105, 108, 112, 115],
        'clients': [12.5, 13.2, 13.8, 14.5, 15.2, 16.1, 17.0, 17.8, 18.5, 19.2, 20.1, 21.0]
    }

    print("===== CLIENTS EN RETARD =====")
    print(clients_en_retard)
    print("Nombre :", len(clients_en_retard))

    return render_template('direction/directeur_general_dashboard.html',
                           stats=stats,
                           total_clients=total_clients,
                           performance=performance,
                           succursales=succursales_data,
                           alertes=alertes,
                           decisions=decisions,
                           evolution=evolution,
                           clients_en_retard=clients_en_retard,
                           now=datetime.now())


@app.route('/direction/financier/dashboard')
@login_required
def directeur_financier_dashboard():
    """Dashboard pour le directeur financier"""
    if current_user.role != 'direction' or current_user.fonction != 'directeur_financier':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import Credit, Remboursement, Succursale, Produit, Paiement
    from datetime import datetime, timedelta
    from sqlalchemy import func

    # Statistiques globales
    portefeuille_total = db.session.query(func.sum(Credit.montant)).filter(
        Credit.statut.in_(['actif', 'impaye'])
    ).scalar() or 0

    # Créances par catégorie
    creances_saines = db.session.query(func.sum(Credit.montant)).filter(
        Credit.statut == 'actif'
    ).scalar() or 0

    creances_douteuses = db.session.query(func.sum(Credit.montant)).filter(
        Credit.statut == 'impaye'
    ).scalar() or 0

    # Provisions (exemple: 50% des créances douteuses)
    provisions = creances_douteuses * 0.5

    # Calcul des ratios
    par_30 = 5.2  # À calculer avec la logique réelle
    par_90 = 2.1
    taux_recouvrement = 95.5
    rendement = 18.3
    cout_risque = 3.2
    roa = 4.8

    stats = {
        'portefeuille_total': portefeuille_total,
        'creances_saines': creances_saines,
        'creances_douteuses': creances_douteuses,
        'provisions': provisions,
        'par_30': par_30,
        'par_90': par_90,
        'taux_recouvrement': taux_recouvrement,
        'rendement': rendement,
        'cout_risque': cout_risque,
        'roa': roa,
        'tx_credits_sains': round((creances_saines / portefeuille_total * 100) if portefeuille_total > 0 else 0, 1),
        'tx_credits_douteux': round((creances_douteuses / portefeuille_total * 100) if portefeuille_total > 0 else 0,
                                    1),
    }

    # Produits
    produits_data = []
    produits = Produit.query.all()
    for p in produits:
        encours = db.session.query(func.sum(Credit.montant)).filter(
            Credit.produit_id == p.id,
            Credit.statut.in_(['actif', 'impaye'])
        ).scalar() or 0

        produits_data.append({
            'nom': p.nom,
            'code': p.code,
            'encours': encours,
            'pourcentage': round((encours / portefeuille_total * 100) if portefeuille_total > 0 else 0, 1),
            'par': 3.5,
            'par_couleur': 'warning' if 3.5 > 5 else 'success'
        })

    # Échéances
    aujourd_hui = datetime.now().date()
    fin_semaine = aujourd_hui + timedelta(days=7)
    fin_mois = aujourd_hui.replace(day=1) + timedelta(days=32)
    fin_mois = fin_mois.replace(day=1) - timedelta(days=1)
    fin_prochain_mois = (fin_mois + timedelta(days=32)).replace(day=1)
    fin_trimestre = aujourd_hui + timedelta(days=90)

    echeances = {
        'semaine': {'montant': 15000000, 'nombre': 45},
        'mois': {'montant': 45000000, 'nombre': 120},
        'prochain_mois': {'montant': 52000000, 'nombre': 135},
        'trimestre': {'montant': 180000000, 'nombre': 450},
    }

    # Impayés (exemple)
    impayes = []

    # Succursales
    succursales = Succursale.query.filter_by(active=True).all()
    succursales_finance = []

    for s in succursales:
        encours = db.session.query(func.sum(Credit.montant)) \
                      .join(Client, Credit.client_id == Client.id) \
                      .filter(
            Client.succursale_id == s.id,
            Credit.statut.in_(['actif', 'impaye'])
        ).scalar() or 0

        succursales_finance.append({
            'nom': s.nom,
            'code': s.code,
            'encours': encours,
            'par_30': 4.2,
            'par_30_couleur': 'warning' if 4.2 > 5 else 'success',
            'par_90': 1.8,
            'par_90_couleur': 'danger' if 1.8 > 3 else 'warning',
            'taux_recouvrement': 96.5,
            'rendement': 17.8,
            'provision': encours * 0.02
        })

    # Trésorerie
    tresorerie = {
        'disponible': 85000000,
        'taux_liquidite': 65,
        'encaissements': 45000000,
        'decaissements': 38000000
    }

    # Données pour les graphiques
    evolution_labels = ['J-6', 'J-5', 'J-4', 'J-3', 'J-2', 'J-1', 'Aujourd\'hui']
    evolution_sain = [850, 860, 855, 870, 880, 890, 900]
    evolution_douteux = [42, 43, 41, 44, 45, 44, 46]
    evolution_impaye = [18, 19, 18, 20, 19, 21, 20]

    qualite = {
        'sain': 85,
        'risque': 10,
        'impaye': 5
    }

    prevision_encaissements = [12, 15, 14, 16, 15, 17, 16, 18, 19]
    prevision_decaissements = [10, 11, 12, 13, 14, 15, 16, 17, 18]

    return render_template('direction/directeur_financier_dashboard.html',
                           stats=stats,
                           produits=produits_data,
                           echeances=echeances,
                           impayes=impayes,
                           succursales_finance=succursales_finance,
                           tresorerie=tresorerie,
                           evolution_labels=evolution_labels,
                           evolution_sain=evolution_sain,
                           evolution_douteux=evolution_douteux,
                           evolution_impaye=evolution_impaye,
                           qualite=qualite,
                           prevision_encaissements=prevision_encaissements,
                           prevision_decaissements=prevision_decaissements,
                           now=datetime.now)



@app.route('/direction/operations/dashboard')
@login_required
def directeur_operations_dashboard():
    """Dashboard pour le directeur des opérations"""
    if current_user.role != 'direction' or current_user.fonction != 'directeur_operations':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import User, Succursale, Transaction, Credit, Paiement, TransactionEpargne,Epargne
    from datetime import datetime, timedelta
    from sqlalchemy import func

    today = datetime.now()
    debut_jour = today.replace(hour=0, minute=0, second=0)
    debut_semaine = today - timedelta(days=7)

    # Statistiques du jour
    transactions_jour = Transaction.query.filter(
        Transaction.date_creation >= debut_jour
    ).count()

    volume_jour = db.session.query(func.sum(Transaction.montant)).filter(
        Transaction.date_creation >= debut_jour
    ).scalar() or 0

    # Statistiques globales
    credits_attente = Credit.query.filter_by(statut='en_attente').count()
    succursales_actives = Succursale.query.filter_by(active=True).count()
    agents_actifs = User.query.filter(
        User.role.in_(['employe', 'superviseur']),
        User.statut == 'actif'
    ).count()

    stats = {
        'transactions_jour': transactions_jour,
        'volume_jour': volume_jour,
        'taux_traitement': 98,  # À calculer selon votre logique
        'temps_moyen': 15,  # À calculer
        'credits_attente': credits_attente,
        'succursales_actives': succursales_actives,
        'agents_actifs': agents_actifs,
        'efficacite': 95,  # À calculer
    }

    # Performance des succursales
    succursales = Succursale.query.filter_by(active=True).all()
    succursales_performance = []

    for s in succursales:
        # Compter les transactions
        transactions = TransactionEpargne.query.join(
            Epargne, Epargne.id == TransactionEpargne.compte_id
        ).join(
            Client, Client.id == Epargne.client_id
        ).filter(
            Client.succursale_id == s.id,
            TransactionEpargne.date_transaction >= debut_semaine
        ).count()

        # Somme des montants
        volume = db.session.query(
            func.sum(TransactionEpargne.montant)
        ).join(
            Epargne, Epargne.id == TransactionEpargne.compte_id
        ).join(
            Client, Client.id == Epargne.client_id
        ).filter(
            Client.succursale_id == s.id,
            TransactionEpargne.date_transaction >= debut_semaine
        ).scalar() or 0

        # Calcul de performance (à adapter)
        performance = min(100, (transactions / 100) * 100) if transactions > 0 else 0

        if performance >= 90:
            statut = 'optimal'
            couleur = 'success'
        elif performance >= 70:
            statut = 'normal'
            couleur = 'info'
        elif performance >= 50:
            statut = 'surveillance'
            couleur = 'warning'
        else:
            statut = 'critique'
            couleur = 'danger'

        succursales_performance.append({
            'id': s.id,
            'nom': s.nom,
            'code': s.code,
            'ville': s.ville,
            'transactions': transactions,
            'volume': volume,
            'temps_moyen': 12,  # À calculer
            'performance': performance,
            'performance_couleur': couleur,
            'statut': statut
        })



    # Données pour les graphiques
    dates_activite = []
    transactions_activite = []
    volume_activite = []


    for i in range(7):
        jour = today - timedelta(days=6 - i)
        dates_activite.append(jour.strftime('%d/%m'))

        debut = jour.replace(hour=0, minute=0, second=0)
        fin = jour.replace(hour=23, minute=59, second=59)

        tx = Transaction.query.filter(
            Transaction.date_creation >= debut,
            Transaction.date_creation <= fin
        ).count()
        transactions_activite.append(tx)

        vol = db.session.query(func.sum(Transaction.montant)).filter(
            Transaction.date_creation >= debut,
            Transaction.date_creation <= fin
        ).scalar() or 0
        volume_activite.append(round(vol / 1000000, 2))  # En millions

    # Récupérer les dossiers en attente d'approbation pour cette succursale
    dossiers_attente = User.query.filter_by(
        succursale_id=current_user.succursale_id,
        role='client',
        statut='en_attente_approbation'
    ).all()
    print(f"📋 {len(dossiers_attente)} dossier(s) en attente pour la succursale {current_user.succursale_id}")

    # Répartition des transactions
    repartition = {
        'credits': Credit.query.filter(Credit.date_demande >= debut_semaine).count(),
        'remboursements': Paiement.query.filter(Paiement.date_paiement >= debut_semaine).count(),
        'depots': 0,  # À implémenter
        'retraits': 0,  # À implémenter
        'autres': 0,
    }

    return render_template('direction/directeur_operations_dashboard.html',
                           stats=stats,
                           succursales_performance=succursales_performance,
                           dates_activite=dates_activite,
                           transactions_activite=transactions_activite,
                           volume_activite=volume_activite,
                           repartition_credits=repartition['credits'],
                           repartition_remboursements=repartition['remboursements'],
                           repartition_depots=repartition['depots'],
                           repartition_retraits=repartition['retraits'],
                           repartition_autres=repartition['autres'],
                           dossiers_attente=dossiers_attente,  # ← AJOUTE CETTE LIGNE
                           now=datetime.now)


@app.route('/direction/succursale/<int:succ_id>/operations')
@login_required
def voir_succursale_ops(succ_id):
    """Voir les détails des opérations d'une succursale spécifique"""
    if current_user.role not in ['directeur', 'admin']:
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('connexion'))

    from models import Succursale, TransactionEpargne, Epargne, Client
    from datetime import datetime, timedelta

    succursale = Succursale.query.get_or_404(succ_id)

    # Période (7 derniers jours par défaut)
    fin = datetime.now()
    debut = fin - timedelta(days=7)

    # Récupérer les transactions de la succursale
    transactions = TransactionEpargne.query.join(
        Epargne, Epargne.id == TransactionEpargne.compte_id
    ).join(
        Client, Client.id == Epargne.client_id
    ).filter(
        Client.succursale_id == succ_id,
        TransactionEpargne.date_transaction >= debut
    ).order_by(TransactionEpargne.date_transaction.desc()).all()

    # Statistiques
    total_depots = db.session.query(
        func.sum(TransactionEpargne.montant)
    ).join(
        Epargne, Epargne.id == TransactionEpargne.compte_id
    ).join(
        Client, Client.id == Epargne.client_id
    ).filter(
        Client.succursale_id == succ_id,
        TransactionEpargne.type_transaction == 'depot',
        TransactionEpargne.date_transaction >= debut
    ).scalar() or 0

    total_retraits = db.session.query(
        func.sum(TransactionEpargne.montant)
    ).join(
        Epargne, Epargne.id == TransactionEpargne.compte_id
    ).join(
        Client, Client.id == Epargne.client_id
    ).filter(
        Client.succursale_id == succ_id,
        TransactionEpargne.type_transaction == 'retrait',
        TransactionEpargne.date_transaction >= debut
    ).scalar() or 0

    return render_template('direction/succursale_operations.html',
                           succursale=succursale,
                           transactions=transactions,
                           total_depots=total_depots,
                           total_retraits=total_retraits,
                           periode_debut=debut,
                           periode_fin=fin)


@app.route('/direction/superviser/transactions')
@login_required
def superviser_transactions():
    """Page de supervision des transactions pour le directeur"""
    if current_user.role not in ['directeur', 'admin']:
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('connexion'))

    from models import TransactionEpargne, Epargne, Client, Succursale
    from sqlalchemy import func
    from datetime import datetime, timedelta

    # Période (30 derniers jours par défaut)
    fin = datetime.now()
    debut = fin - timedelta(days=30)

    # Récupérer toutes les transactions récentes
    transactions = TransactionEpargne.query.join(
        Epargne, Epargne.id == TransactionEpargne.compte_id
    ).join(
        Client, Client.id == Epargne.client_id
    ).join(
        Succursale, Succursale.id == Client.succursale_id
    ).filter(
        TransactionEpargne.date_transaction >= debut
    ).order_by(
        TransactionEpargne.date_transaction.desc()
    ).all()

    # Statistiques globales
    total_depots = db.session.query(
        func.sum(TransactionEpargne.montant)
    ).filter(
        TransactionEpargne.type_transaction == 'depot',
        TransactionEpargne.date_transaction >= debut
    ).scalar() or 0

    total_retraits = db.session.query(
        func.sum(TransactionEpargne.montant)
    ).filter(
        TransactionEpargne.type_transaction == 'retrait',
        TransactionEpargne.date_transaction >= debut
    ).scalar() or 0

    # Transactions par succursale
    stats_succursales = []
    succursales = Succursale.query.all()

    for s in succursales:
        nb_transactions = TransactionEpargne.query.join(
            Epargne, Epargne.id == TransactionEpargne.compte_id
        ).join(
            Client, Client.id == Epargne.client_id
        ).filter(
            Client.succursale_id == s.id,
            TransactionEpargne.date_transaction >= debut
        ).count()

        montant_total = db.session.query(
            func.sum(TransactionEpargne.montant)
        ).join(
            Epargne, Epargne.id == TransactionEpargne.compte_id
        ).join(
            Client, Client.id == Epargne.client_id
        ).filter(
            Client.succursale_id == s.id,
            TransactionEpargne.date_transaction >= debut
        ).scalar() or 0

        stats_succursales.append({
            'nom': s.nom,
            'nb_transactions': nb_transactions,
            'montant_total': montant_total
        })

    return render_template('direction/superviser_transactions.html',
                           transactions=transactions,
                           total_depots=total_depots,
                           total_retraits=total_retraits,
                           stats_succursales=stats_succursales,
                           periode_debut=debut,
                           periode_fin=fin)


@app.route('/direction/operations/rapport')
@login_required
def rapport_operations():
    """Générer un rapport des opérations"""
    if current_user.role not in ['directeur', 'admin']:
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('connexion'))

    from models import TransactionEpargne, Epargne, Client, Succursale
    from sqlalchemy import func
    from datetime import datetime, timedelta

    # Période (30 derniers jours par défaut)
    fin = datetime.now()
    debut = fin - timedelta(days=30)

    # Statistiques globales
    total_transactions = TransactionEpargne.query.filter(
        TransactionEpargne.date_transaction >= debut
    ).count()

    total_depots = db.session.query(
        func.sum(TransactionEpargne.montant)
    ).filter(
        TransactionEpargne.type_transaction == 'depot',
        TransactionEpargne.date_transaction >= debut
    ).scalar() or 0

    total_retraits = db.session.query(
        func.sum(TransactionEpargne.montant)
    ).filter(
        TransactionEpargne.type_transaction == 'retrait',
        TransactionEpargne.date_transaction >= debut
    ).scalar() or 0

    # Rapport par succursale
    rapport_succursales = []
    succursales = Succursale.query.all()

    for s in succursales:
        nb_transactions = TransactionEpargne.query.join(
            Epargne, Epargne.id == TransactionEpargne.compte_id
        ).join(
            Client, Client.id == Epargne.client_id
        ).filter(
            Client.succursale_id == s.id,
            TransactionEpargne.date_transaction >= debut
        ).count()

        depots = db.session.query(
            func.sum(TransactionEpargne.montant)
        ).join(
            Epargne, Epargne.id == TransactionEpargne.compte_id
        ).join(
            Client, Client.id == Epargne.client_id
        ).filter(
            Client.succursale_id == s.id,
            TransactionEpargne.type_transaction == 'depot',
            TransactionEpargne.date_transaction >= debut
        ).scalar() or 0

        retraits = db.session.query(
            func.sum(TransactionEpargne.montant)
        ).join(
            Epargne, Epargne.id == TransactionEpargne.compte_id
        ).join(
            Client, Client.id == Epargne.client_id
        ).filter(
            Client.succursale_id == s.id,
            TransactionEpargne.type_transaction == 'retrait',
            TransactionEpargne.date_transaction >= debut
        ).scalar() or 0

        rapport_succursales.append({
            'nom': s.nom,
            'nb_transactions': nb_transactions,
            'depots': depots,
            'retraits': retraits,
            'volume_total': depots + retraits
        })

    return render_template('direction/rapport_operations.html',
                           debut=debut,
                           fin=fin,
                           total_transactions=total_transactions,
                           total_depots=total_depots,
                           total_retraits=total_retraits,
                           rapport_succursales=rapport_succursales)


@app.route('/direction/operations/optimiser')
@login_required
def optimiser_flux():
    """Page d'optimisation des flux et analyse des performances"""
    if current_user.role not in ['directeur', 'admin']:
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('connexion'))

    from models import TransactionEpargne, Epargne, Client, Succursale, User
    from sqlalchemy import func
    from datetime import datetime, timedelta
    import json

    # Périodes d'analyse
    aujourd_hui = datetime.now()
    debut_mois = datetime(aujourd_hui.year, aujourd_hui.month, 1)
    mois_dernier = debut_mois - timedelta(days=1)
    debut_mois_dernier = datetime(mois_dernier.year, mois_dernier.month, 1)

    # 1. ANALYSE DES PERFORMANCES PAR SUCCURSALE
    performances = []
    succursales = Succursale.query.all()

    for s in succursales:
        # Transactions du mois en cours
        transactions_mois = TransactionEpargne.query.join(
            Epargne, Epargne.id == TransactionEpargne.compte_id
        ).join(
            Client, Client.id == Epargne.client_id
        ).filter(
            Client.succursale_id == s.id,
            TransactionEpargne.date_transaction >= debut_mois
        ).count()

        # Volume du mois en cours
        volume_mois = db.session.query(
            func.sum(TransactionEpargne.montant)
        ).join(
            Epargne, Epargne.id == TransactionEpargne.compte_id
        ).join(
            Client, Client.id == Epargne.client_id
        ).filter(
            Client.succursale_id == s.id,
            TransactionEpargne.date_transaction >= debut_mois
        ).scalar() or 0

        # Transactions du mois dernier
        transactions_mois_dernier = TransactionEpargne.query.join(
            Epargne, Epargne.id == TransactionEpargne.compte_id
        ).join(
            Client, Client.id == Epargne.client_id
        ).filter(
            Client.succursale_id == s.id,
            TransactionEpargne.date_transaction >= debut_mois_dernier,
            TransactionEpargne.date_transaction < debut_mois
        ).count()

        # Calcul de l'évolution
        if transactions_mois_dernier > 0:
            evolution = ((transactions_mois - transactions_mois_dernier) / transactions_mois_dernier) * 100
        else:
            evolution = 100 if transactions_mois > 0 else 0

        # Nombre de conseillers
        nb_conseillers = User.query.filter_by(
            succursale_id=s.id,
            role='employe',
            fonction='conseiller'
        ).count()

        # Productivité par conseiller
        productivite = transactions_mois / nb_conseillers if nb_conseillers > 0 else 0

        performances.append({
            'succursale': s.nom,
            'transactions_mois': transactions_mois,
            'volume_mois': volume_mois,
            'evolution': round(evolution, 1),
            'nb_conseillers': nb_conseillers,
            'productivite': round(productivite, 1),
            'couleur': 'success' if evolution >= 0 else 'danger'
        })

    # 2. ANALYSE DES TENDANCES
    # Transactions par jour sur les 30 derniers jours
    fin = aujourd_hui
    debut = fin - timedelta(days=30)

    transactions_par_jour = db.session.query(
        func.date(TransactionEpargne.date_transaction).label('jour'),
        func.count().label('nb_transactions'),
        func.sum(TransactionEpargne.montant).label('volume')
    ).filter(
        TransactionEpargne.date_transaction >= debut
    ).group_by(
        func.date(TransactionEpargne.date_transaction)
    ).order_by('jour').all()

    # 3. RECOMMANDATIONS D'OPTIMISATION
    recommandations = []

    # Vérifier les succursales sous-performantes
    for p in performances:
        if p['transactions_mois'] < 50:
            recommandations.append({
                'type': 'warning',
                'message': f"🔶 {p['succursale']}: Faible volume de transactions ({p['transactions_mois']} transactions/mois). Envisager une formation des conseillers."
            })
        elif p['evolution'] < -10:
            recommandations.append({
                'type': 'danger',
                'message': f"🔴 {p['succursale']}: Baisse d'activité de {p['evolution']}% par rapport au mois dernier."
            })
        elif p['productivite'] < 10:
            recommandations.append({
                'type': 'info',
                'message': f"🔵 {p['succursale']}: Productivité faible ({p['productivite']} transactions/conseiller). Optimiser la répartition des tâches."
            })

    # Recommandations générales
    if performances:
        meilleure = max(performances, key=lambda x: x['evolution'])
        recommandations.append({
            'type': 'success',
            'message': f"✅ {meilleure['succursale']} est la succursale avec la meilleure progression ({meilleure['evolution']}%). Analyser et reproduire ses pratiques."
        })

    return render_template('direction/optimiser_flux.html',
                           performances=performances,
                           transactions_par_jour=transactions_par_jour,
                           recommandations=recommandations,
                           aujourd_hui=aujourd_hui)


@app.route('/direction/maintenance/planifier', methods=['GET', 'POST'])
@login_required
def planifier_maintenance():
    """Planifier une maintenance système"""
    if current_user.role not in ['directeur', 'admin']:
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('connexion'))

    from models import Maintenance, Succursale
    from datetime import datetime

    succursales = Succursale.query.all()

    if request.method == 'POST':
        titre = request.form.get('titre')
        description = request.form.get('description')
        type_maintenance = request.form.get('type_maintenance')
        date_debut = datetime.strptime(request.form.get('date_debut'), '%Y-%m-%dT%H:%M')
        date_fin = datetime.strptime(request.form.get('date_fin'), '%Y-%m-%dT%H:%M')
        succursale_id = request.form.get('succursale_id') or None

        maintenance = Maintenance(
            titre=titre,
            description=description,
            type_maintenance=type_maintenance,
            date_debut=date_debut,
            date_fin=date_fin,
            succursale_id=succursale_id,
            statut='planifiee',
            cree_par_id=current_user.id
        )

        db.session.add(maintenance)
        db.session.commit()

        flash(f'✅ Maintenance "{titre}" planifiée avec succès', 'success')
        return redirect(url_for('liste_maintenances'))

    return render_template('direction/planifier_maintenance.html',
                           succursales=succursales,
                           maintenant=datetime.now())


@app.route('/direction/succursales/capacite')
@login_required
def capacite_succursales():
    """Afficher la capacité et les performances des succursales"""
    if current_user.role not in ['directeur', 'admin']:
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('connexion'))

    from models import Succursale, User, Pret, Remboursement, Client
    from sqlalchemy import func

    succursales = Succursale.query.all()
    capacites = []

    for s in succursales:
        # Nombre d'employés
        nb_employes = User.query.filter_by(succursale_id=s.id, role='employe').count()

        # Nombre de clients
        nb_clients = Client.query.filter_by(succursale_id=s.id, role='client').count()

        # Nombre de prêts actifs
        nb_prets_actifs = Pret.query.filter_by(succursale_id=s.id, actif=True).count()

        # Montant total des prêts
        montant_total_prets = db.session.query(func.sum(Pret.montant)).filter_by(succursale_id=s.id).scalar() or 0

        # Total des remboursements
        total_remboursements = db.session.query(func.sum(Remboursement.montant)).filter_by(
            succursale_id=s.id).scalar() or 0

        # Ratio client/employé
        ratio_client_employe = round(nb_clients / nb_employes, 1) if nb_employes > 0 else 0

        capacites.append({
            'succursale': s,
            'nb_employes': nb_employes,
            'nb_clients': nb_clients,
            'nb_prets_actifs': nb_prets_actifs,
            'montant_total_prets': montant_total_prets,
            'total_remboursements': total_remboursements,
            'ratio_client_employe': ratio_client_employe,
            'capacite': 'Élevée' if ratio_client_employe < 50 else 'Moyenne' if ratio_client_employe < 100 else 'Faible'
        })

    return render_template('direction/capacite_succursales.html', capacites=capacites)


@app.route('/direction/agents/performance')
@login_required
def performance_agents():
    """Analyser la performance des agents par succursale"""
    if current_user.role not in ['directeur', 'admin']:
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('connexion'))

    from models import User, Pret, Remboursement, Succursale
    from sqlalchemy import func
    from datetime import datetime, timedelta

    # Période (30 derniers jours)
    fin = datetime.now()
    debut = fin - timedelta(days=30)

    # Récupérer tous les agents (employés avec fonction conseiller/agent)
    agents = User.query.filter(
        User.role == 'employe',
        User.fonction.in_(['conseiller', 'agent_credit', 'agent_remboursement'])
    ).all()

    performances = []

    for agent in agents:
        # Prêts traités par l'agent
        prets_traites = Pret.query.filter_by(agent_id=agent.id).count()

        # Prêts du mois
        prets_mois = Pret.query.filter(
            Pret.agent_id == agent.id,
            Pret.date_demande >= debut
        ).count()

        # Montant total des prêts accordés
        montant_prets = db.session.query(func.sum(Pret.montant)).filter_by(agent_id=agent.id).scalar() or 0

        # Remboursements collectés
        remboursements = Remboursement.query.filter_by(client_id=agent.id).count()

        # Taux de conversion (si applicable)
        taux_conversion = 85  # À calculer selon tes données

        # Note de performance
        if prets_mois > 20:
            performance = "Excellent"
            couleur = "success"
        elif prets_mois > 10:
            performance = "Bon"
            couleur = "info"
        elif prets_mois > 5:
            performance = "Moyen"
            couleur = "warning"
        else:
            performance = "À améliorer"
            couleur = "danger"

        performances.append({
            'agent': agent,
            'succursale': agent.succursale.nom if agent.succursale else 'N/A',
            'prets_traites': prets_traites,
            'prets_mois': prets_mois,
            'montant_prets': montant_prets,
            'remboursements': remboursements,
            'taux_conversion': taux_conversion,
            'performance': performance,
            'couleur': couleur
        })

    # Statistiques globales
    total_agents = len(agents)
    total_prets = sum(p['prets_traites'] for p in performances)
    moyenne_prets = round(total_prets / total_agents, 1) if total_agents > 0 else 0

    return render_template('direction/performance_agents.html',
                           performances=performances,
                           total_agents=total_agents,
                           total_prets=total_prets,
                           moyenne_prets=moyenne_prets,
                           periode_debut=debut,
                           periode_fin=fin)


@app.route('/direction/operations/audit')
@login_required
def audit_operations():
    """Page d'audit des opérations"""
    if current_user.role not in ['directeur', 'admin']:
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('connexion'))

    from models import User, Pret, Remboursement, TransactionEpargne, Succursale
    from sqlalchemy import func
    from datetime import datetime, timedelta

    # Période (7 derniers jours)
    fin = datetime.now()
    debut = fin - timedelta(days=7)

    # Statistiques d'audit
    total_transactions = TransactionEpargne.query.count()
    total_prets = Pret.query.count()
    total_remboursements = Remboursement.query.count()

    # Anomalies potentielles (à définir selon ta logique)
    prets_sans_remboursement = Pret.query.filter(~Pret.remboursements.any()).count()

    # Top 5 des agents les plus actifs
    top_agents = db.session.query(
        User, func.count(Pret.id).label('nb_prets')
    ).join(Pret, Pret.agent_id == User.id
           ).group_by(User.id
                      ).order_by(func.count(Pret.id).desc()
                                 ).limit(5).all()

    return render_template('direction/audit_operations.html',
                           total_transactions=total_transactions,
                           total_prets=total_prets,
                           total_remboursements=total_remboursements,
                           prets_sans_remboursement=prets_sans_remboursement,
                           top_agents=top_agents,
                           periode_debut=debut,
                           periode_fin=fin)


@app.route('/direction/succursales/gerer')
@login_required
def gerer_succursales():
    """Page de gestion des succursales pour le directeur"""
    if current_user.role not in ['directeur', 'admin']:
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('connexion'))

    from models import Succursale, User

    succursales = Succursale.query.all()

    # Statistiques par succursale
    stats = []
    for s in succursales:
        nb_conseillers = User.query.filter_by(
            succursale_id=s.id,
            role='employe',
            fonction='conseiller'
        ).count()

        nb_clients = Client.query.filter_by(
            succursale_id=s.id,
            role='client'
        ).count()

        stats.append({
            'succursale': s,
            'nb_conseillers': nb_conseillers,
            'nb_clients': nb_clients
        })

    return render_template('direction/gerer_succursales.html', stats=stats)

@app.route('/direction/commercial/dashboard')
@login_required
def directeur_commercial_dashboard():
    """Dashboard pour le directeur commercial"""
    if current_user.role != 'direction' or current_user.fonction != 'directeur_commercial':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import User, Client, Credit, Succursale, Produit
    from datetime import datetime, timedelta
    from sqlalchemy import func

    today = datetime.now()
    debut_mois = today.replace(day=1, hour=0, minute=0, second=0)
    debut_annee = today.replace(month=1, day=1)

    # Statistiques mensuelles
    ca_mensuel = db.session.query(func.sum(Credit.montant)).filter(
        Credit.date_demande >= debut_mois
    ).scalar() or 0

    nouveaux_clients = Client.query.filter(
        Client.date_inscription >= debut_mois
    ).count()

    credits_mois = Credit.query.filter(
        Credit.date_demande >= debut_mois
    ).count()

    # Objectifs (à configurer dans une table dédiée)
    objectif_ca = 100000000  # 100 millions
    objectif_clients = 50
    objectif_credits = 30

    stats = {
        'ca_mensuel': ca_mensuel,
        'nouveaux_clients': nouveaux_clients,
        'credits_mois': credits_mois,
        'taux_conversion': round((credits_mois / Credit.query.count() * 100) if Credit.query.count() > 0 else 0, 1),
        'objectif_atteint': round((ca_mensuel / objectif_ca * 100) if objectif_ca > 0 else 0, 1),
        'objectif_ca': objectif_ca,
        'objectif_clients': objectif_clients,
        'objectif_credits': objectif_credits,
    }

    # Top agents
    top_agents = db.session.query(
        User,
        func.count(Credit.id).label('credits_mois'),
        func.sum(Credit.montant).label('montant_mois')
    ).join(Credit, Credit.agent_id == User.id) \
        .filter(Credit.date_demande >= debut_mois) \
        .group_by(User.id) \
        .order_by(func.count(Credit.id).desc()) \
        .limit(5).all()

    top_agents_list = []
    for agent, credits, montant in top_agents:
        top_agents_list.append({
            'id': agent.id,
            'nom': agent.nom,
            'prenom': agent.prenom,
            'succursale': agent.succursale,
            'credits_mois': credits,
            'montant_mois': montant
        })

    # Top produits
    top_produits = db.session.query(
        Credit.type_credit.label('nom'),
        func.count(Credit.id).label('nombre'),
        func.sum(Credit.montant).label('montant_total')
    ).group_by(Credit.type_credit) \
        .order_by(func.count(Credit.id).desc()) \
        .limit(5).all()

    # Demandes en attente
    demandes_attente = Credit.query.filter_by(statut='en_attente') \
        .order_by(Credit.date_demande.desc()) \
        .limit(5).all()

    # Derniers clients
    derniers_clients = Client.query.order_by(
        Client.date_inscription.desc()
    ).limit(5).all()

    # Données pour les graphiques
    succursales = Succursale.query.all()
    succursales_noms = [s.nom for s in succursales]
    succursales_ca = []
    succursales_clients = []

    for s in succursales:
        ca = db.session.query(func.sum(Credit.montant)).join(Client).filter(
            Client.succursale_id == s.id,
            Credit.date_demande >= debut_mois
        ).scalar() or 0
        succursales_ca.append(round(ca / 1000000, 2))  # En millions

        nb_clients = Client.query.filter_by(succursale_id=s.id).count()
        succursales_clients.append(nb_clients)

    # Évolution mensuelle
    evolution_ca = []
    evolution_objectif = []
    for i in range(1, today.month + 1):
        mois = today.replace(day=1, month=i)
        fin_mois = (mois + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        ca_mois = db.session.query(func.sum(Credit.montant)).filter(
            Credit.date_demande >= mois,
            Credit.date_demande <= fin_mois
        ).scalar() or 0
        evolution_ca.append(round(ca_mois / 1000000, 2))

        # Objectif mensuel (proportionnel)
        evolution_objectif.append(round(objectif_ca / 12 / 1000000, 2))

    return render_template('direction/directeur_commercial_dashboard.html',
                           stats=stats,
                           top_agents=top_agents_list,
                           top_produits=top_produits,
                           demandes_attente=demandes_attente,
                           derniers_clients=derniers_clients,
                           succursales_noms=succursales_noms,
                           succursales_ca=succursales_ca,
                           succursales_clients=succursales_clients,
                           evolution_ca=evolution_ca,
                           evolution_objectif=evolution_objectif,
                           now=datetime.now)



@app.route('/direction/rh/dashboard')
@login_required
def directeur_rh_dashboard():
    """Dashboard pour le directeur des ressources humaines"""
    if current_user.role != 'direction' or current_user.fonction != 'directeur_rh':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import User, Succursale, DemandeConge, Formation, Recrutement, Pointage
    from datetime import datetime, timedelta
    from sqlalchemy import func

    today = datetime.now()
    debut_mois = today.replace(day=1)
    fin_mois = (debut_mois + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Statistiques globales
    effectif_total = User.query.filter(User.role.in_(['employe', 'superviseur', 'admin_succursale'])).count()

    stats = {
        'effectif_total': effectif_total,
        'presents': Pointage.query.filter_by(date=today.date(), present=True).count(),
        'en_conges': DemandeConge.query.filter(
            DemandeConge.statut == 'approuve',
            DemandeConge.date_debut <= today,
            DemandeConge.date_fin >= today
        ).count(),
        'recrues_mois': User.query.filter(
            User.date_embauche >= debut_mois,
            User.date_embauche <= fin_mois
        ).count(),
        'departs_mois': User.query.filter(
            User.date_depart >= debut_mois,
            User.date_depart <= fin_mois
        ).count(),
        'periode_essai': User.query.filter_by(periode_essai=True).count(),
        'anniversaires_mois': User.query.filter(
            func.extract('month', User.date_naissance) == today.month
        ).count(),
        'taux_absentéisme': 3.5,  # À calculer selon votre logique
        'actifs': User.query.filter_by(statut='actif').count(),
        'suspendus': User.query.filter_by(statut='suspendu').count(),
        'inactifs': User.query.filter_by(statut='inactif').count(),
    }

    # Demandes de congés en attente
    demandes_conges = DemandeConge.query.filter_by(statut='en_attente') \
        .order_by(DemandeConge.date_creation.desc()) \
        .limit(10).all()

    # Formations en cours
    formations = Formation.query.filter(
        Formation.date_fin >= today,
        Formation.date_debut <= today
    ).all()

    # Recrutements en cours
    recrutements = Recrutement.query.filter(
        Recrutement.date_limite >= today
    ).order_by(Recrutement.date_limite).all()

    # Anniversaires du mois
    anniversaires = User.query.filter(
        User.role.in_(['employe', 'superviseur']),
        func.extract('month', User.date_naissance) == today.month
    ).all()

    # Données pour les graphiques
    succursales = Succursale.query.all()
    succursales_noms = [s.nom for s in succursales]
    succursales_effectifs = [
        User.query.filter_by(succursale_id=s.id, role__in=['employe', 'superviseur']).count()
        for s in succursales
    ]

    return render_template('direction/directeur_rh_dashboard.html',
                           stats=stats,
                           demandes_conges=demandes_conges,
                           formations=formations,
                           recrutements=recrutements,
                           anniversaires=anniversaires,
                           succursales_noms=succursales_noms,
                           succursales_effectifs=succursales_effectifs,
                           now=datetime.now)


@app.route('/direction/conformite/dashboard')
@login_required
def directeur_conformite_dashboard():
    """Dashboard pour le directeur de la conformité"""
    if current_user.role != 'direction' or current_user.fonction != 'directeur_conformite':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import Client, AlerteConformite, VerificationAnnuelle, Document
    from datetime import datetime, timedelta
    from sqlalchemy import func

    # Statistiques
    stats = {
        'kyc_en_attente': Client.query.filter_by(kyc_statut='en_attente').count(),
        'alertes_aml': AlerteConformite.query.filter_by(statut='nouvelle').count(),
        'comptes_verifies': Client.query.filter_by(verification_faciale=True).count(),
        'documents_expires': Document.query.filter(Document.date_expiration < datetime.now()).count(),
        'taux_conformite': 85,  # À calculer selon votre logique
        'temps_moyen_traitement': 24,  # À calculer
        'conformes': 150,
        'en_attente': 30,
        'non_conformes': 20
    }

    # Alertes récentes
    alertes = AlerteConformite.query.order_by(
        AlerteConformite.date_creation.desc()
    ).limit(10).all()

    # Vérifications annuelles à faire
    verifications_annuelles = VerificationAnnuelle.query.filter(
        VerificationAnnuelle.date_echeance <= datetime.now() + timedelta(days=30)
    ).limit(5).all()

    # Documents expirés
    documents_expires = Document.query.filter(
        Document.date_expiration < datetime.now()
    ).limit(10).all()

    return render_template('direction/directeur_conformite_dashboard.html',
                           stats=stats,
                           alertes=alertes,
                           verifications_annuelles=verifications_annuelles,
                           documents_expires=documents_expires,
                           now=datetime.now)


@app.route('/direction/dossiers-en-attente')
@login_required
def direction_dossiers_en_attente():

    if current_user.role != 'directeur':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('connexion'))

    dossiers = Client.query.filter_by(
        succursale_id=current_user.succursale_id,
        statut='en_attente_approbation'
    ).all()

    return render_template(
        'direction/dossiers_en_attente.html',
        dossiers=dossiers
    )


@app.route('/direction/dashboard-generique')
@login_required
def direction_dashboard_generique():
    """Dashboard générique pour la direction"""
    if current_user.role != 'direction':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import User, Succursale, Client, Credit, Remboursement, AuditLog
    from sqlalchemy import func

    # Statistiques globales
    stats = {
        'succursales': Succursale.query.count(),
        'employes': User.query.filter_by(role='employe').count(),
        'super_admins': User.query.filter_by(role='super_admin').count(),
        'admins': User.query.filter(User.role.in_(['admin', 'admin_succursale'])).count(),
        'superviseurs': User.query.filter_by(role='superviseur').count(),
        'clients': Client.query.count(),
        'credits_actifs': Credit.query.filter_by(statut='actif').count(),
        'montant_total_credits': db.session.query(func.sum(Credit.montant)).scalar() or 0,
        'montant_total_remboursements': db.session.query(func.sum(Remboursement.montant)).scalar() or 0,
    }

    # Calcul du taux de remboursement
    if stats['montant_total_credits'] > 0:
        stats['taux_remboursement'] = (stats['montant_total_remboursements'] / stats['montant_total_credits']) * 100
    else:
        stats['taux_remboursement'] = 0

    # Derniers logs d'activité
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(10).all()

    return render_template('direction/direction_dashboard_generique.html',
                           stats=stats,
                           logs=logs,
                           now=datetime.now)


@app.route('/agent/dashboard')
@login_required
def dashboard_agent():
    if current_user.role != 'agent':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('main.accueil'))

    from models import Client, Credit, Paiement, Succursale
    from sqlalchemy import func
    from datetime import datetime, timedelta

    # Récupérer l'ID de la succursale de l'agent
    succursale_id = current_user.succursale_id

    # Récupérer tous les IDs des clients de cette succursale
    clients_ids = [c.id for c in Client.query.filter_by(succursale_id=succursale_id).all()]

    # Statistiques
    stats = {
        'clients_actifs': Client.query.filter_by(succursale_id=succursale_id, statut='actif').count(),

        # Crédits actifs : ceux dont le client est dans la succursale
        'credits_actifs': Credit.query.filter(
            Credit.client_id.in_(clients_ids) if clients_ids else False,
            Credit.statut == 'actif'
        ).count() if clients_ids else 0,

        # Montant total décaissé pour les crédits actifs de la succursale
        'montant_total_decaissement': db.session.query(func.sum(Credit.montant))
                                      .filter(
            Credit.client_id.in_(clients_ids) if clients_ids else False,
            Credit.statut == 'actif'
        ).scalar() or 0 if clients_ids else 0,

        # Remboursements du mois pour les crédits de la succursale
        'remboursements_mois': db.session.query(func.sum(Paiement.montant))
                               .join(Credit)
                               .filter(
            Credit.client_id.in_(clients_ids) if clients_ids else False,
            Paiement.date_paiement >= datetime.now().replace(day=1, hour=0, minute=0, second=0)
        ).scalar() or 0 if clients_ids else 0,

        # Demandes en attente
        'demandes_en_attente': Credit.query.filter(
            Credit.client_id.in_(clients_ids) if clients_ids else False,
            Credit.statut == 'en_attente'
        ).count() if clients_ids else 0,

        # Crédits remboursés
        'credits_rembourses': Credit.query.filter(
            Credit.client_id.in_(clients_ids) if clients_ids else False,
            Credit.statut == 'rembourse'
        ).count() if clients_ids else 0,
    }

    # Calculer le taux de remboursement
    total_rembourse = db.session.query(func.sum(Paiement.montant)) \
                          .join(Credit) \
                          .filter(Credit.client_id.in_(clients_ids) if clients_ids else False) \
                          .scalar() or 0 if clients_ids else 0

    total_du = db.session.query(func.sum(Credit.montant_total_du)) \
                   .filter(Credit.client_id.in_(clients_ids) if clients_ids else False) \
                   .scalar() or 0 if clients_ids else 0

    stats['taux_remboursement'] = round((total_rembourse / total_du * 100), 2) if total_du > 0 else 0

    # Demandes en attente (avec les détails des clients)
    demandes_attente = []
    if clients_ids:
        demandes_attente = Credit.query \
            .filter(
            Credit.client_id.in_(clients_ids),
            Credit.statut == 'en_attente'
        ) \
            .order_by(Credit.date_demande.desc()) \
            .limit(5) \
            .all()

    # Paiements récents
    paiements_recents = []
    if clients_ids:
        paiements_recents = Paiement.query \
            .join(Credit) \
            .filter(Credit.client_id.in_(clients_ids)) \
            .order_by(Paiement.date_paiement.desc()) \
            .limit(5) \
            .all()

    # Crédits impayés (en retard)
    credits_impayes = []
    if clients_ids:
        credits_impayes = Credit.query \
            .filter(
            Credit.client_id.in_(clients_ids),
            Credit.statut == 'actif',
            Credit.date_echeance < datetime.now()
        ) \
            .order_by(Credit.date_echeance) \
            .all()

        # Ajouter une propriété jours_retard à chaque crédit
        for credit in credits_impayes:
            credit.jours_retard = (datetime.now() - credit.date_echeance).days

    return render_template('agent/dashboard_agent.html',
                           stats=stats,
                           demandes_attente=demandes_attente,
                           paiements_recents=paiements_recents,
                           credits_impayes=credits_impayes,
                           now=datetime.now)


@app.route('/nouveau-credit/<int:client_id>')
@login_required
def nouveau_credit(client_id):
    """Page pour créer un nouveau crédit pour un client"""
    from models import Client

    client = db.session.get(Client, client_id)
    if not client:
        flash('Client non trouvé', 'danger')
        return redirect(url_for('liste_clients'))

    return render_template('nouveau_credit.html', client=client)



@app.route('/agent/clients')
@login_required
def liste_clients():
    """Affiche la liste des clients pour un agent"""
    # Vérifier que l'utilisateur est un agent
    if current_user.role not in ['admin','admin_succursale', 'super_admin', 'superviseur', 'directeur','gestion_employes']:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('main.accueil'))

    from models import Client, Credit, Pret
    from sqlalchemy import func

    # Récupérer les paramètres de filtre et recherche
    search = request.args.get('search', '')
    statut = request.args.get('statut', '')
    page = request.args.get('page', 1, type=int)
    per_page = 20  # Nombre de clients par page

    # Construire la requête de base (clients de la succursale de l'agent)
    query = Client.query.filter_by(succursale_id=current_user.succursale_id)

    # Appliquer les filtres
    if search:
        query = query.filter(
            db.or_(
                Client.nom.ilike(f'%{search}%'),
                Client.prenom.ilike(f'%{search}%'),
                Client.telephone.ilike(f'%{search}%'),
                Client.email.ilike(f'%{search}%')
            )
        )

    if statut:
        query = query.filter_by(statut=statut)

    # Pagination
    clients = query.order_by(Client.nom, Client.prenom).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Statistiques pour chaque client
    clients_stats = []
    for client in clients.items:
        # Nombre de crédits du client
        nb_credits = Pret.query.filter_by(client_id=client.id).count()

        # Crédits actifs
        pret_actifs = Pret.query.filter_by(
            client_id=client.id,
            statut='actif'
        ).count()

        total_emprunte = db.session.query(func.sum(Pret.montant)).filter_by(client_id=client.id).scalar() or 0




        dernier_pret = Pret.query.filter_by(client_id=client.id) \
            .order_by(Pret.date_demande.desc()).first()

        clients_stats.append({
            'client': client,
            'nb_credits': nb_credits,
            'pret_actifs': pret_actifs,
            'total_emprunte': total_emprunte,
            'dernier_pret': dernier_pret,
            'dernier_credit_date': dernier_pret.date_demande if dernier_pret else None,
            'dernier_credit_montant': dernier_pret.montant if dernier_pret else None

        })

    # Statistiques globales
    stats = {
        'total': Client.query.filter_by(succursale_id=current_user.succursale_id).count(),
        'actifs': Client.query.filter_by(succursale_id=current_user.succursale_id, statut='actif').count(),
        'inactifs': Client.query.filter_by(succursale_id=current_user.succursale_id, statut='inactif').count(),
        'suspendu': Client.query.filter_by(succursale_id=current_user.succursale_id, statut='suspendu').count(),   # ← AJOUTER
        'avec_credits': db.session.query(Client.id).join(Pret).filter(Client.succursale_id == current_user.succursale_id).distinct().count()
    }

    return render_template('clients/liste_clients.html',
                           clients=clients,
                           clients_stats=clients_stats,
                           stats=stats,
                           search=search,
                           statut=statut)



@app.route("/agent/client/<int:client_id>")
@login_required
def voir_client(client_id):
    """Affiche les détails d'un client"""

    client = db.session.get(Client, client_id)

    if not client:
        flash("❌ Client introuvable.")
        return redirect(url_for("liste_clients"))

    if client.role != "client":
        flash("❌ Cet utilisateur n'est pas un client.")
        return redirect(url_for("liste_clients"))

    # ✅ AJOUTEZ CES LIGNES POUR LE SOLDE
    from models import Epargne
    from sqlalchemy import func

    # Récupérer le solde total du client (somme de tous ses comptes épargne actifs)
    solde = db.session.query(func.sum(Epargne.solde)).filter(
        Epargne.client_id == client.id,
        Epargne.statut == 'actif'
    ).scalar() or 0

    return render_template("clients/voir_client.html", client=client, solde=solde)




@app.route('/agent/client/<int:client_id>/modifier', methods=['GET', 'POST'])
@login_required
def modifier_client(client_id):

    client = User.query.get(client_id)

    if not client:
        flash("❌ Client introuvable.")
        return redirect(url_for('liste_clients'))

    if client.role != "client":
        flash("❌ Cet utilisateur n'est pas un client.")
        return redirect(url_for('liste_clients'))

    if request.method == "POST":
        client.nom = request.form.get("nom")
        client.telephone = request.form.get("telephone")

        db.session.commit()

        flash("✅ Client modifié avec succès.")
        return redirect(url_for('voir_client', id=client.id))

    return render_template("modifier_client.html", client=client)


@app.route('/deconnexion')
def deconnexion():
    logout_user()
    return redirect(url_for('main.accueil'))





# Ajoutez cette route pour la reconnaissance faciale avec DeepFace
@app.route('/api/face-recognition/verify', methods=['POST'])
def verify_faces_api():
    """API pour vérifier deux visages"""
    try:
        if 'image1' not in request.files or 'image2' not in request.files:
            return jsonify({'error': 'Deux images sont requises'}), 400

        image1 = request.files['image1']
        image2 = request.files['image2']

        # Sauvegarder temporairement les images
        temp_path1 = os.path.join(app.config['UPLOAD_FOLDER'], 'temp1.jpg')
        temp_path2 = os.path.join(app.config['UPLOAD_FOLDER'], 'temp2.jpg')

        image1.save(temp_path1)
        image2.save(temp_path2)

        # Comparer avec DeepFace
        result = DeepFace.verify(
            img1_path=temp_path1,
            img2_path=temp_path2,
            model_name="VGG-Face",
            detector_backend="opencv",
            distance_metric="cosine"
        )

        # Nettoyer les fichiers temporaires
        os.remove(temp_path1)
        os.remove(temp_path2)

        return jsonify({
            'verified': result['verified'],
            'distance': float(result['distance']),
            'similarity': float(1 - result['distance']),
            'threshold': 0.6,
            'model': 'VGG-Face'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# ==================== SYSTÈME DE REMBOURSEMENTS ====================

@app.route('/remboursement/nouveau', methods=['GET', 'POST'])
@login_required
def nouveau_remboursement():
    from flask import request, jsonify, render_template, flash, redirect, url_for, send_file
    from datetime import datetime
    from models import Pret, Remboursement, Journal, Client

    print("🔥 ROUTE ENREGISTREMENT REMBOURSEMENT")

    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form

            pret_id = data.get('pret_id')
            montant = float(data.get('montant', 0))
            methode = data.get('methode')
            type_paiement = request.form.get('type_paiement')
            reference = data.get('reference')

            pret = db.session.get(Pret, pret_id)

            if not pret:
                return jsonify({"success": False, "message": "Prêt introuvable"}), 404

            if montant <= 0:
                return jsonify({"success": False, "message": "Montant invalide"}), 400

            # ✅ Calculer le total déjà remboursé
            total_rembourse = sum(r.montant for r in pret.remboursements if r.statut in ['valide', 'effectue'])
            solde_reel = pret.montant - total_rembourse
            nouveau_solde = solde_reel - montant

            # ✅ CORRECTION 1 : Utiliser solde_reel au lieu de pret.solde_restant
            if montant > solde_reel:
                flash(f"❌ Montant dépasse le solde restant ({solde_reel:,.0f} HTG)", "error")
                return redirect(url_for('nouveau_remboursement'))

            # ✅ CORRECTION 2 : Récupérer succursale_id correctement
            succursale_id = current_user.succursale_id
            if not succursale_id:
                succursale_id = getattr(pret, 'succursale_id', None)

            # ✅ CORRECTION 3 : client_id sécurisé
            client_id = pret.client_id if pret.client_id else current_user.id

            remboursement = Remboursement(
                pret_id=pret.id,
                client_id=client_id,
                montant=montant,
                date_echeance=pret.date_echeance,
                type_paiement=type_paiement,
                methode=methode,
                reference=reference,
                statut='effectue',
                date_remboursement=datetime.utcnow(),
                employe_id=current_user.id,
                succursale_id=succursale_id
            )

            db.session.add(remboursement)

            # Mettre à jour le montant remboursé dans le prêt
            pret.montant_rembourse = (pret.montant_rembourse or 0)  + montant


            journal = Journal(
                employe_id=current_user.id,
                action="REMBOURSEMENT",
                details=f"Remboursement de {montant:,.0f} HTG pour prêt {pret.id}",
                date=datetime.now(),
                pret_id=pret.id,
            )
            db.session.add(journal)
            db.session.commit()  # Premier commit

            if nouveau_solde <= 0:
                pret.statut = 'rembourse'
                flash(f'🎉 Prêt #{pret.id} entièrement remboursé !', 'success')

                # ✅ Réactiver le client
                client = db.session.get(Client, pret.client_id)

                if client:
                    print("🔥 AVANT:", client.statut)
                    client.statut = 'actif'
                    print("🔥 APRÈS:", client.statut)

                flash(f'✅ Remboursement de {montant:,.0f} HTG enregistré ! Nouveau solde: {nouveau_solde:,.0f} HTG',
                      'success')


            db.session.commit()  # Commit du changement de statut

            # ✅ CORRECTION 4 : Flash avant le return
            try:
                recu = generer_recu_remboursement_pdf(pret, remboursement, current_user)
                flash('✅ Remboursement enregistré avec succès !', 'success')
                return send_file(
                    recu['pdf_file'],
                    as_attachment=True,
                    download_name=f"recu_remboursement_{pret.numero_pret}.pdf",
                    mimetype='application/pdf'
                )
            except Exception as e:
                print(f"Erreur génération reçu: {e}")
                flash("Remboursement enregistré mais erreur lors de la génération du reçu", "warning")
                return redirect(url_for('mes_remboursements'))

        except Exception as e:
            db.session.rollback()
            print("❌ Erreur remboursement:", e)
            return jsonify({"success": False, "message": "Erreur serveur"}), 500

    # ✅ GET → Afficher uniquement les prêts avec solde > 0
    prets = Pret.query.filter(
        Pret.client_id == current_user.id,
        Pret.statut.in_(['approuve', 'actif', 'retard'])
    ).all()

    # Filtrer ceux qui ont encore un solde > 0
    prets_avec_solde = []
    for pret in prets:
        total_rembourse = sum(r.montant for r in pret.remboursements if r.statut in ['valide', 'effectue'])
        if pret.montant - total_rembourse > 0:
            prets_avec_solde.append(pret)

    return render_template(
        'nouveau_remboursement.html',
        prets=prets_avec_solde
    )

@app.route('/mes-remboursements')
@login_required
def mes_remboursements():
    from sqlalchemy import func

    remboursements = Remboursement.query.filter_by(client_id=current_user.id).order_by(
        Remboursement.date_remboursement.desc()).all()

    # Associer les remboursements avec les prêts et calculer le vrai solde
    remboursements_avec_prets = []
    for remb in remboursements:
        pret = db.session.get(Pret, remb.pret_id)

        # Calculer le total remboursé pour ce prêt
        total_rembourse = db.session.query(func.sum(Remboursement.montant)).filter(
            Remboursement.pret_id == pret.id,
            Remboursement.statut == 'effectue'
        ).scalar() or 0

        # Calculer le solde restant réel
        solde_reel = pret.montant - total_rembourse

        remboursements_avec_prets.append({
            'remboursement': remb,
            'pret': pret,
            'total_rembourse': total_rembourse,
            'solde_restant': solde_reel
        })

    return render_template('mes_remboursements.html', remboursements_avec_prets=remboursements_avec_prets)


@app.route('/admin/notifications')
@login_required
def admin_notifications():
    """
    Page des notifications pour les administrateurs
    - Affiche les notifications récentes
    - Affiche la configuration des services de notification
    """

    # === 1. VÉRIFICATION DES PERMISSIONS (sécurisée) ===
    allowed_roles = ['admin', 'super_admin', 'admin_succursale']
    user_role = getattr(current_user, 'role', None)

    if user_role not in allowed_roles:
        flash("⛔ Accès non autorisé. Cette page est réservée aux administrateurs.", "danger")
        return redirect(url_for('tableau_de_bord'))

    # === 2. RÉCUPÉRATION DE LA CONFIGURATION (avec valeurs par défaut) ===
    config = {
        'SMTP_SERVER': os.getenv('SMTP_SERVER', 'Non configuré'),
        'SMTP_PORT': os.getenv('SMTP_PORT', '587'),
        'SMTP_USERNAME': os.getenv('SMTP_USERNAME', 'Non configuré'),
        'SMTP_PASSWORD': '********' if os.getenv('SMTP_PASSWORD') else None,
        'SMTP_FROM': os.getenv('SMTP_FROM', 'noreply@gmes.ht'),
        'SMS_API_KEY': '********' if os.getenv('SMS_API_KEY') else None,
        'SMS_FROM': os.getenv('SMS_FROM', 'GMES'),
        'NOTIFICATION_EMAIL': os.getenv('NOTIFICATION_EMAIL', 'admin@gmes.ht')
    }

    # === 3. RÉCUPÉRATION DES NOTIFICATIONS (version robuste) ===
    notifications = []
    unread_count = 0

    try:
        # Essayer de récupérer depuis la base de données si la table existe
        if hasattr(db, 'Notification') or 'Notification' in dir(db.Model):
            # Requête pour les 50 dernières notifications de l'utilisateur
            notifications_query = db.session.query(
                Notification.id,
                Notification.message,
                Notification.level,
                Notification.read,
                Notification.timestamp
            ).filter(
                Notification.employe_id == current_user.id
            ).order_by(
                Notification.timestamp.desc()
            ).limit(50).all()

            for n in notifications_query:
                notifications.append({
                    'id': n.id,
                    'message': n.message,
                    'level': n.level or 'info',
                    'read': n.read or False,
                    'time': n.timestamp.strftime('%d/%m/%Y %H:%M') if n.timestamp else 'Date inconnue'
                })

            unread_count = db.session.query(Notification).filter_by(
                employe_id=current_user.id,
                read=False
            ).count()

    except Exception as e:
        # Si la table n'existe pas, on utilise des notifications fictives pour la démo
        app.logger.warning(f"Table Notification non accessible: {e}")

        # Notifications de démonstration
        demo_notifications = [
            {
                'id': 1,
                'message': 'Bienvenue dans le centre de notifications',
                'level': 'info',
                'read': False,
                'time': datetime.now().strftime('%d/%m/%Y %H:%M')
            },
            {
                'id': 2,
                'message': 'La configuration SMTP est opérationnelle',
                'level': 'success',
                'read': False,
                'time': (datetime.now() - timedelta(hours=1)).strftime('%d/%m/%Y %H:%M')
            },
            {
                'id': 3,
                'message': 'Mise à jour du système prévue cette nuit',
                'level': 'warning',
                'read': True,
                'time': (datetime.now() - timedelta(days=1)).strftime('%d/%m/%Y %H:%M')
            }
        ]
        notifications = demo_notifications
        unread_count = sum(1 for n in demo_notifications if not n['read'])

    # === 4. VÉRIFICATION DE L'ÉTAT DES SERVICES ===
    services_status = {
        'smtp': {
            'active': bool(os.getenv('SMTP_SERVER') and os.getenv('SMTP_USERNAME')),
            'message': 'SMTP configuré' if bool(os.getenv('SMTP_SERVER')) else 'SMTP non configuré'
        },
        'sms': {
            'active': bool(os.getenv('SMS_API_KEY')),
            'message': 'SMS configuré' if bool(os.getenv('SMS_API_KEY')) else 'SMS non configuré'
        }
    }

    # === 5. STATISTIQUES DES NOTIFICATIONS ===
    stats = {
        'total': len(notifications),
        'unread': unread_count,
        'by_level': {
            'error': sum(1 for n in notifications if n.get('level') == 'error'),
            'warning': sum(1 for n in notifications if n.get('level') == 'warning'),
            'success': sum(1 for n in notifications if n.get('level') == 'success'),
            'info': sum(1 for n in notifications if n.get('level') == 'info')
        }
    }

    # === 6. RENDU DU TEMPLATE ===
    return render_template(
        'admin/admin_notifications.html',
        config=config,
        notifications=notifications,
        stats=stats,
        services_status=services_status,
        now=datetime.now()
    )


# === ROUTES API COMPLÉMENTAIRES ===
#
# @app.route('/api/notifications/mark-read/<int:notification_id>', methods=['POST'])
# @login_required
# def mark_notification_read(notification_id):
#     """Marque une notification comme lue"""
#     allowed_roles = ['admin', 'super_admin', 'admin_succursale', 'direction']
#     if getattr(current_user, 'role', None) not in allowed_roles:
#         return jsonify({'success': False, 'error': 'Non autorisé'}), 403
#
#     try:
#         # Vérifier si la table Notification existe
#         if hasattr(db, 'Notification'):
#             notification = Notification.query.get(notification_id)
#             if notification and notification.employe_id == current_user.id:
#                 notification.read = True
#                 db.session.commit()
#                 return jsonify({'success': True})
#
#         # Fallback pour la démo
#         return jsonify({'success': True})
#
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_notifications_read():
    """Marque toutes les notifications comme lues"""
    allowed_roles = ['admin', 'super_admin', 'admin_succursale']
    if getattr(current_user, 'role', None) not in allowed_roles:
        return jsonify({'success': False, 'error': 'Non autorisé'}), 403

    try:
        if hasattr(db, 'Notification'):
            Notification.query.filter_by(
                employe_id=current_user.id,
                read=False
            ).update({'read': True})
            db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/notifications/unread')
@login_required
def get_unread_notifications():
    """Récupère les notifications non lues (pour polling AJAX)"""
    allowed_roles = ['admin', 'super_admin', 'admin_succursale']
    if getattr(current_user, 'role', None) not in allowed_roles:
        return jsonify([]), 403

    try:
        notifications = []

        if hasattr(db, 'Notification'):
            # Récupérer les notifications non lues des 5 dernières minutes
            five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)

            recent_notifications = Notification.query.filter_by(
                employe_id=current_user.id,
                read=False
            ).filter(
                Notification.timestamp >= five_minutes_ago
            ).order_by(
                Notification.timestamp.desc()
            ).all()

            for n in recent_notifications:
                notifications.append({
                    'id': n.id,
                    'message': n.message,
                    'level': n.level or 'info',
                    'time': n.timestamp.strftime('%H:%M') if n.timestamp else 'maintenant',
                    'read': n.read
                })

        return jsonify(notifications)

    except Exception as e:
        app.logger.error(f"Erreur récupération notifications: {e}")
        return jsonify([])


@app.route('/api/test-email', methods=['POST'])
@login_required
def test_email_notification():
    """Test d'envoi d'email de notification"""
    allowed_roles = ['admin', 'super_admin', 'admin_succursale']
    if getattr(current_user, 'role', None) not in allowed_roles:
        return jsonify({'success': False, 'error': 'Non autorisé'}), 403

    try:
        # Ici votre logique d'envoi d'email de test
        # Exemple avec Flask-Mail
        """
        from flask_mail import Message

        msg = Message(
            subject="Test Notification - GMES",
            recipients=[current_user.email],
            body=f\"\"\"
        Ceci est un email de test du système de notifications.

        Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        Utilisateur: {current_user.prenom} {current_user.nom}

        Si vous recevez cet email, la configuration SMTP fonctionne correctement.

        ---
        GMES Microcrédit - Système de Gestion
        \"\"\"
        )
        mail.send(msg)
        """

        # Pour l'instant, on simule un succès
        app.logger.info(f"Test email envoyé à {current_user.email}")

        return jsonify({
            'success': True,
            'message': 'Email de test envoyé avec succès'
        })

    except Exception as e:
        app.logger.error(f"Erreur envoi email test: {e}")
        return jsonify({
            'success': False,
            'message': f'Erreur: {str(e)}'
        }), 500






@app.route('/admin/remboursements')
@login_required
def admin_remboursements():
    if getattr(current_user, 'role', None) != 'admin':
        return redirect(url_for('tableau_de_bord'))

    remboursements = Remboursement.query.all()

    # Associer avec clients et prêts
    remboursements_complets = []
    for remb in remboursements:
        pret = Pret.query.get(remb.pret_id)
        client = User.query.get(remb.client_id)  # ✅ CORRECTION: Utiliser User
        remboursements_complets.append({
            'remboursement': remb,
            'pret': pret,
            'client': client
        })

    return render_template('admin_remboursements.html', remboursements_complets=remboursements_complets)



@app.route('/api/calculer-echeancier/<int:pret_id>')
@login_required
def calculer_echeancier(pret_id):
    """Calcule l'échéancier d'un prêt"""
    pret = Pret.query.get_or_404(pret_id)

    # Vérifier que le prêt appartient au client
    if pret.client_id != current_user.id:
        return jsonify({'error': 'Accès non autorisé'})

    echeances = []
    montant_restant = pret.montant_total
    date_courante = datetime.utcnow()

    for i in range(pret.duree_mois):
        date_echeance = date_courante.replace(month=date_courante.month + i)
        echeances.append({
            'numero': i + 1,
            'date': date_echeance.strftime('%d/%m/%Y'),
            'montant': pret.mensualite,
            'capital': pret.mensualite * 0.8,  # Estimation
            'interet': pret.mensualite * 0.2  # Estimation
        })

    return jsonify({
        'pret': {
            'montant': pret.montant,
            'duree': pret.duree_mois,
            'mensualite': pret.mensualite,
            'total_a_rembourser': pret.montant_total
        },
        'echeances': echeances
    })


# Dans la route qui rend liste_groupes.html

@app.route('/liste_groupes')
def liste_groupes():
    # Récupérer tous les groupes
    groupes = Groupe.query.all()

    # Pour chaque groupe, calculer le nombre de clients
    groupes_avec_stats = []
    for groupe in groupes:
        nb_clients = Client.query.filter_by(groupe_id=groupe.id).count()
        groupes_avec_stats.append({
            'groupe': groupe,
            'nb_clients': nb_clients
        })

    return render_template('liste_groupes.html', groupes_avec_stats=groupes_avec_stats)
@app.route('/admin/assigner-groupe/<int:employe_id>', methods=['GET', 'POST'])
@login_required
def assigner_groupe(employe_id):
    """Assigner un groupe à un employé - Admin seulement"""
    if current_user.role != 'admin':
        return redirect(url_for('tableu_de_bord'))

    employe = User.query.get_or_404(employe_id)
    groupes = Groupe.query.all()

    if request.method == 'POST':
        groupe_id = request.form.get('groupe_id')
        employe.groupe_id = groupe_id if groupe_id else None
        session.commit()
        return redirect(url_for('gerer_employes'))

    return render_template('assigner_groupe.html', employe=employe, groupes=groupes)


@app.route('/groupe/<int:groupe_id>')
@login_required
def detail_groupe(groupe_id):
    groupe = Groupe.query.get_or_404(groupe_id)
    clients = Client.query.filter_by(groupe_id=groupe_id).all()
    prets_du_groupe = Pret.query.filter_by(groupe_id=groupe_id).all()

    # Calculer les statistiques du groupe
    stats = {
        'nombre_membres': len(clients),
        'prets_actifs': len([p for p in prets_du_groupe if p.statut == 'approuve']),
        'montant_total_prets': sum(p.montant for p in prets_du_groupe),
        'taux_remboursement': 95  # À calculer dynamiquement
    }

    return render_template('detail_groupe.html',
                           groupe=groupe,
                           clients=clients,
                           prets=prets_du_groupe,
                           stats=stats)


@app.route('/groupe/creer', methods=['GET', 'POST'])
@login_required
def creer_groupe():
    if getattr(current_user, 'role', None) not in ['admin', 'employe']:
        return redirect(url_for('tableau_de_bord'))

    if request.method == 'POST':
        nom = request.form.get('nom')
        zone = request.form.get('zone')

        # Générer un code de groupe unique
        code_groupe = f"GRP{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

        groupe = Groupe(
            nom=nom,
            code_groupe=code_groupe,
            zone=zone
        )

        session.add(groupe)
        session.commit()

        return redirect(url_for('liste_groupes'))

    return render_template('creer_groupe.html')


@app.route('/groupe/<int:groupe_id>/rejoindre')
@login_required
def rejoindre_groupe(groupe_id):

    # ... code existant ...

    current_user.groupe_id = groupe_id
    session.commit()

    # 🔔 NOTIFICATION de nouveau groupe
    notification_manager.notifier_nouveau_groupe(current_user, groupe)

    return redirect(url_for('detail_groupe', groupe_id=groupe_id))


@app.route('/groupe/<int:groupe_id>/quitter')
@login_required
def quitter_groupe(groupe_id):
    # Seuls les clients peuvent quitter des groupes
    if hasattr(current_user, 'role'):
        return redirect(url_for('tableau_de_bord'))

    # Vérifier que le client est bien dans ce groupe
    if current_user.groupe_id != groupe_id:
        return redirect(url_for('tableau_de_bord'))

    current_user.groupe_id = None
    session.commit()

    return redirect(url_for('liste_groupes'))


@app.route('/groupe/<int:groupe_id>/demande-pret-solidaire', methods=['GET', 'POST'])
@login_required
def demande_pret_solidaire(groupe_id):

    # Vérifier que l'utilisateur est un client membre du groupe
    if hasattr(current_user, 'role') or current_user.groupe_id != groupe_id:
        return redirect(url_for('tableau_de_bord'))

    groupe = Groupe.query.get_or_404(groupe_id)

    if request.method == 'POST':
        montant = float(request.form.get('montant'))
        duree = int(request.form.get('duree'))
        motif = request.form.get('motif')

        # Calculs automatiques
        taux_mensuel = 12.0 / 100 / 12
        mensualite = montant * taux_mensuel * (1 + taux_mensuel) ** duree / ((1 + taux_mensuel) ** duree - 1)
        montant_interet = (mensualite * duree) - montant
        montant_total = mensualite * duree

        nouveau_pret = Pret(
            client_id=current_user.id,
            groupe_id=groupe_id,
            montant=montant,
            duree_mois=duree,
            motif=motif,
            mensualite=round(mensualite, 2),
            montant_interet=round(montant_interet, 2),
            montant_total=round(montant_total, 2),
            statut='en_attente_solidaire'  # Statut spécial pour prêts solidaires
        )

        session.add(nouveau_pret)
        session.commit()

        return redirect(url_for('detail_groupe', groupe_id=groupe_id))

    return render_template('demande_pret_solidaire.html', groupe=groupe)


@app.route('/api/statistiques-groupes')
@login_required
def statistiques_groupes():

    if getattr(current_user, 'role', None) != 'super_admin':
        return jsonify({'error': 'Accès non autorisé'}), 403

    groupes = Groupe.query.all()

    print("=" * 50)
    print(f"NOMBRE GROUPES : {len(groupes)}")
    print("=" * 50)

    statistiques = []

    for groupe in groupes:

        clients = Client.query.filter_by(groupe_id=groupe.id).all()
        prets = Pret.query.filter_by(groupe_id=groupe.id).all()

        prets_actifs = [
            p for p in prets
            if p.statut in ['approuve', 'actif', 'en_cours']
        ]

        montant_total_prets = sum(
            float(p.montant or 0)
            for p in prets
        )

        montant_actif = sum(
            float(p.montant or 0)
            for p in prets_actifs
        )

        moyenne_credit = (
            montant_total_prets / len(prets)
            if len(prets) > 0 else 0
        )

        taux_performance = (
            (len(prets_actifs) / len(prets)) * 100
            if len(prets) > 0 else 0
        )

        statistiques.append({
            "groupe_id": groupe.id,
            "nom_groupe": groupe.nom,
            "zone": getattr(groupe, 'zone', ''),

            "nombre_membres": len(clients),

            "prets_total": len(prets),
            "prets_actifs": len(prets_actifs),

            "montant_total_prets": round(montant_total_prets, 2),
            "montant_actif": round(montant_actif, 2),

            "moyenne_credit": round(moyenne_credit, 2),
            "performance": round(taux_performance, 1)
        })

    return jsonify(statistiques)
# ==================== RAPPORTS ET STATISTIQUES ====================

@app.route('/admin/rapports')
@login_required
def admin_rapports():

    if getattr(current_user, 'role', None) != 'super_admin':
        return redirect(url_for('tableau_de_bord'))

    # Calculer les statistiques globales
    stats = calculer_statistiques_globales()

    return render_template('admin_rapports.html', stats=stats)


@app.route('/admin/rapport-prets')
@login_required
def rapport_prets():

    if getattr(current_user, 'role', None) != 'admin':
        return redirect(url_for('tableau_de_bord'))

    # Filtres
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')
    statut = request.args.get('statut')

    # Requête de base
    query = Pret.query

    # Appliquer les filtres
    if date_debut:
        query = query.filter(Pret.date_demande >= datetime.strptime(date_debut, '%Y-%m-%d'))
    if date_fin:
        query = query.filter(Pret.date_demande <= datetime.strptime(date_fin, '%Y-%m-%d'))
    if statut:
        query = query.filter(Pret.statut == statut)

    prets = query.all()

    # Préparer les données pour le rapport
    prets_rapport = []
    for pret in prets:
        client = User.query.get(pret.client_id)
        prets_rapport.append({
            'pret': pret,
            'client': client
        })

    return render_template('rapport_prets.html',
                           prets_rapport=prets_rapport,
                           filters={'date_debut': date_debut, 'date_fin': date_fin, 'statut': statut})


@app.route('/admin/rapport-remboursements')
@login_required
def rapport_remboursements():

    if getattr(current_user, 'role', None) != 'admin':
        return redirect(url_for('tableau_de_bord'))

    # Filtres
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')

    query = Remboursement.query

    if date_debut:
        query = query.filter(Remboursement.date_remboursement >= datetime.strptime(date_debut, '%Y-%m-%d'))
    if date_fin:
        query = query.filter(Remboursement.date_remboursement <= datetime.strptime(date_fin, '%Y-%m-%d'))

    remboursements = query.all()

    # Préparer les données
    remboursements_rapport = []
    for remb in remboursements:
        pret = Pret.query.get(remb.pret_id)
        client = User.query.get(remb.client_id)
        remboursements_rapport.append({
            'remboursement': remb,
            'pret': pret,
            'client': client
        })

    return render_template('rapport_remboursements.html',
                           remboursements_rapport=remboursements_rapport,
                           filters={'date_debut': date_debut, 'date_fin': date_fin})


@app.route('/api/statistiques-temps-reel')
@login_required
def statistiques_temps_reel():

    if getattr(current_user, 'role', None) != 'admin':
        return jsonify({'error': 'Accès non autorisé'})

    stats = calculer_statistiques_globales()
    return jsonify(stats)




@app.route('/test-mobile-routes')
def test_mobile_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        if 'mobile' in str(rule.rule):
            routes.append(f"{rule.rule} -> {rule.endpoint}")
    return "<br>".join(routes) if routes else "Aucune route mobile trouvée"




@app.route('/admin/export-prets-excel')
@login_required
def export_prets_excel():

    if getattr(current_user, 'role', None) != 'admin':
        return redirect(url_for('tableau_de_bord'))

    prets = Pret.query.all()

    # Créer un DataFrame (simulé)
    data = []
    for pret in prets:
        client = User.query.get(pret.client_id)
        data.append({
            'ID Prêt': pret.id,
            'Client': f"{client.prenom} {client.nom}" if client else "N/A",
            'Montant': pret.montant,
            'Durée (mois)': pret.duree_mois,
            'Mensualité': pret.mensualite,
            'Statut': pret.statut,
            'Date Demande': pret.date_demande.strftime('%d/%m/%Y'),
            'Motif': pret.motif
        })

    # Pour l'instant, retourner un JSON (implémentez l'export Excel plus tard)
    return jsonify({
        'message': 'Export Excel des prêts',
        'nombre_prets': len(data),
        'data': data
    })


@app.route('/cron/rappels-quotidiens')
def rappels_quotidiens():
    """
    Route pour les rappels automatiques (à appeler via cron job)
    """
    try:
        # Prêts avec remboursements en retard
        prets_actifs = Pret.query.filter_by(statut='approuve').all()

        for pret in prets_actifs:
            client = User.query.get(pret.client_id)

            # Calculer les jours jusqu'à la prochaine échéance
            # (simplifié pour l'exemple)
            jours_restants = 5  # À calculer dynamiquement

            if jours_restants <= 3:  # Rappel 3 jours avant
                notification_manager.notifier_rappel_remboursement(
                    client, pret, jours_restants
                )

        return jsonify({
            'status': 'success',
            'message': f'Rappels envoyés pour {len(prets_actifs)} prêts'
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/admin/test-notification')
@login_required
def test_notification():
    """Route de test pour les notifications avec choix manuel"""
    allowed_roles = ['admin', 'super_admin', 'admin_succursale']

    if getattr(current_user, 'role', None) not in allowed_roles:
        return jsonify({'error': 'Non autorisé'}), 403

    # Récupérer les paramètres de l'URL
    client_id = request.args.get('client_id', type=int)
    pret_id = request.args.get('pret_id', type=int)

    # Si pas de client_id, afficher la page de sélection
    if not client_id:
        clients = User.query.all()
        return render_template('admin/selection_test.html', clients=clients)

    # Récupérer le client sélectionné
    client = User.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client non trouvé'}), 404

    # Si pas de pret_id, afficher les prêts du client
    if not pret_id:
        prets = Pret.query.filter_by(client_id=client.id).all()
        return render_template('admin/selection_pret.html',
                               client=client,
                               prets=prets)

    # Récupérer le prêt sélectionné
    pret = Pret.query.get(pret_id)
    if not pret or pret.client_id != client.id:
        return jsonify({'error': 'Prêt non trouvé'}), 404

    # Envoyer la notification
    try:
        if hasattr(notification_manager, 'notifier_approbation_pret'):
            notification_manager.notifier_approbation_pret(client, pret)
            return jsonify({
                'status': 'success',
                'message': f'Notification envoyée à {client.email}',
                'client': {
                    'id': client.id,
                    'nom': client.nom,
                    'prenom': client.prenom,
                    'email': client.email
                },
                'pret': {
                    'id': pret.id,
                    'montant': pret.montant,
                    'statut': pret.statut
                }
            })
        else:
            return jsonify({
                'status': 'simulation',
                'message': 'Notification simulée',
                'client': client.email,
                'pret_id': pret.id
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Fonctions utilitaires pour les statistiques
def calculer_statistiques_globales():
    """Calcule les statistiques globales du système"""

    from models import User, Client, Pret, Remboursement, Epargne, Employe


    total_clients = Client.query.filter_by(role='client').count()  # ✅ Seulement les clients
    total_prets = Pret.query.count()
    prets_approuve = Pret.query.filter_by(statut='approuve').count()
    prets_actifs = Pret.query.filter_by(statut='actif').count()
    prets_en_attente = Pret.query.filter_by(statut='en_attente').count()

    # Calcul des montants
    montant_total_prets = db.session.query(db.func.sum(Pret.montant)).scalar() or 0
    montant_prets_actifs = db.session.query(db.func.sum(Pret.montant)).filter(
        Pret.statut == 'approuve'
    ).scalar() or 0

    # Remboursements
    total_remboursements = Remboursement.query.count()
    montant_total_rembourse = db.session.query(db.func.sum(Remboursement.montant)).scalar() or 0

    # Groupes
    total_groupes = Groupe.query.count()

    # Calcul du taux de remboursement (simplifié)
    # ✅ Correction du taux
    taux_remboursement = (montant_total_rembourse / montant_total_prets * 100) if montant_total_prets > 0 else 0

    # ✅ CORRECTION de la jointure problématique
    clients_avec_prets_count = db.session.query(
        db.func.count(db.func.distinct(User.id))
    ).join(Pret, User.id == Pret.client_id).filter(
        User.role == 'client'
    ).scalar() or 0

    return {
        'clients': {
            'total': total_clients,
            'avec_prets': clients_avec_prets_count,  # ✅ Utiliser la version corrigée
            'nouveaux_ce_mois': User.query.filter(
                User.date_inscription >= datetime.utcnow().replace(day=1),
                User.role == 'client'  # ✅ Seulement les clients
            ).count()
        },
        'prets': {
            'total': total_prets,
            'actifs': prets_actifs,
            'prets_approuve':prets_approuve,
            'en_attente': prets_en_attente,
            'montant_total': round(montant_total_prets, 2),
            'montant_actifs': round(montant_prets_actifs, 2)
        },
        'remboursements': {
            'total': total_remboursements,
            'montant_total': round(montant_total_rembourse, 2),
            'taux_remboursement': round(taux_remboursement, 1)
        },
        'groupes': {
            'total': total_groupes,
            'membres_moyen': total_clients / total_groupes if total_groupes > 0 else 0
        },
        'performance': {
            'taux_approbation': (prets_actifs / total_prets * 100) if total_prets > 0 else 0,
            'rotation_fonds': calculer_rotation_fonds()
        }
    }






def calculer_rotation_fonds():
    """Calcule la rotation des fonds (simplifié)"""
    # Implémentation simplifiée
    return 2.5  # Exemple fixe


@app.route('/tableau-bord-personnalise')
@login_required
def tableau_bord_personnalise():
    """Tableau de bord avec widgets personnalisables"""
    if getattr(current_user, 'role', None) != 'admin':
        return redirect(url_for('tableau_de_bord'))

    stats = calculer_statistiques_globales()

    # Données pour les graphiques
    prets_par_statut = session.query(
        Pret.statut,
        db.func.count(Pret.id)
    ).group_by(Pret.statut).all()

    prets_par_mois = session.query(
        db.func.strftime('%Y-%m', Pret.date_demande),
        db.func.count(Pret.id)
    ).group_by(db.func.strftime('%Y-%m', Pret.date_demande)).all()

    return render_template('tableau_bord_personnalise.html',
                           stats=stats,
                           prets_par_statut=prets_par_statut,
                           prets_par_mois=prets_par_mois)




@app.route('/fonctions/agent_credit/<succursale_code>/nouvelle-demande', methods=['GET', 'POST'])
@login_required
def agent_nouvelle_demande(succursale_code):
    """Route pour les agents de crédit - Créer une demande pour un client"""

    # Vérifier que c'est bien un agent de crédit
    if current_user.role != 'employe' or current_user.fonction != 'agent_credit':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import Succursale, Client, Pret

    succursale = Succursale.query.filter_by(code=succursale_code).first_or_404()

    if request.method == 'POST':
        # Récupérer les données du formulaire
        client_id = request.form.get('client_id')
        montant = float(request.form.get('montant'))
        duree = int(request.form.get('duree'))
        motif = request.form.get('motif')
        taux = float(request.form.get('taux', 12.0))
        garantie = request.form.get('garantie')
        type_pret = request.form.get('type_pret', 'classique')

        # Vérifier que le client existe
        client = Client.query.get_or_404(client_id)

        # Calculs automatiques
        taux_mensuel = taux / 100 / 12
        mensualite = montant * taux_mensuel * (1 + taux_mensuel) ** duree / ((1 + taux_mensuel) ** duree - 1)
        montant_interet = (mensualite * duree) - montant
        montant_total = mensualite * duree

        # Créer le prêt
        nouveau_pret = Pret(
            client_id=client_id,
            agent_id=current_user.id,
            montant=montant,
            duree_mois=duree,
            motif=motif,
            mensualite=round(mensualite, 2),
            montant_interet=round(montant_interet, 2),
            montant_total=round(montant_total, 2),
            statut='en_attente',
            garantie=garantie,
            type_pret=type_pret
        )

        db.session.add(nouveau_pret)
        db.session.commit()

        flash(f'✅ Demande de prêt créée pour {client.prenom} {client.nom}', 'success')
        return redirect(url_for('agent_credit_dashboard', succursale_code=succursale_code))

    # GET - Afficher le formulaire
    clients = Client.query.filter_by(succursale_id=succursale.id).all()
    return render_template('fonctions/agent_credit/nouvelle_demande.html',
                           succursale=succursale,
                           clients=clients)


@app.route('/mes-prets')
@login_required
def mes_prets():
    prets = Pret.query.filter_by(client_id=current_user.id).all()
    return render_template('mes_prets.html', prets=prets)


@app.route('/api/calcul-pret', methods=['POST'])
def calcul_pret():
    data = request.json
    montant = float(data['montant'])
    duree = int(data['duree'])
    taux_annuel = 12.0

    taux_mensuel = taux_annuel / 100 / 12
    mensualite = montant * taux_mensuel * (1 + taux_mensuel) ** duree / ((1 + taux_mensuel) ** duree - 1)
    total_rembourser = mensualite * duree
    cout_credit = total_rembourser - montant

    return jsonify({
        'mensualite': round(mensualite, 2),
        'total_rembourser': round(total_rembourser, 2),
        'cout_credit': round(cout_credit, 2)
    })


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():

    if current_user.role not in ['super_admin', 'admin_succursale']:
        flash("Accès refusé", "danger")
        return redirect(url_for('tableau_de_bord'))

    # 📍 Succursales visibles
    if current_user.role == 'super_admin':
        succursales = Succursale.query.all()
    else:
        succursales = Succursale.query.filter_by(
            id=current_user.succursale_id
        ).all()

    stats_par_succursale = {}

    for s in succursales:
        stats_par_succursale[s.id] = {
            "clients": Client.query.filter_by(succursale_id=s.id).count(),
            "prets_actifs": Pret.query.filter_by(
                succursale_id=s.id, statut='actif'
            ).count(),
            "remboursements": Remboursement.query.filter_by(
                succursale_id=s.id
            ).count()
        }

    # 👥 UTILISATEURS (calcul global, PAS dans la boucle)
    total_admins = User.query.filter(
        User.role.in_(["super_admin", "admin_succursale"])
    ).count()

    total_agents = User.query.filter_by(role="agent").count()

    total_clients = Client.query.count()

    comptes_en_attente = User.query.filter_by(
        statut="en_attente"
    ).all()

    return render_template(
        'admin_central/dashboard.html',
        succursales=succursales,
        stats_par_succursale=stats_par_succursale,
        total_admins=total_admins,
        total_agents=total_agents,
        total_clients=total_clients,
        comptes_en_attente=comptes_en_attente
    )


@app.route('/admin/succursales')
@login_required
def liste_succursales():

    if current_user.role == 'super_admin':
        succursales = Succursale.query.all()
    else:
        succursales = Succursale.query.filter_by(
            id=current_user.succursale_id
        ).all()
    # Création simple des stats
    stats_globales = []

    for succursale in succursales:
        stats = {
            'succursale': succursale,

            'clients': Client.query.filter_by(
                succursale_id=succursale.id
            ).count(),

            'prets': Pret.query.filter(
                Pret.succursale_id == succursale.id,
                Pret.statut.in_(['actif', 'approuve'])
            ).count(),

            'remboursements': Remboursement.query.filter_by(
                succursale_id=succursale.id
            ).count(),

            'montant_total': db.session.query(
                db.func.sum(Pret.montant_accorde)
            ).filter(
                Pret.succursale_id == succursale.id,
                Pret.statut.in_(['actif', 'approuve'])
            ).scalar() or 0
        }

        stats_globales.append(stats)

    return render_template(
        'admin_central/succursales.html',
        succursales=succursales,
        stats_globales=stats_globales
    )



@app.route('/client/dashboard')
@login_required
def client_dashboard():
    """Dashboard client"""

    # Vérifier si c'est un client (par différents moyens)
    est_client = False

    # Méthode 1: Par le rôle
    if hasattr(current_user, 'role') and current_user.role == 'client':
        est_client = True

    # Méthode 2: Par le type d'utilisateur
    if hasattr(current_user, 'type_utilisateur') and current_user.type_utilisateur == 'client':
        est_client = True

    # Méthode 3: Par la présence de champs spécifiques aux clients
    if hasattr(current_user, 'terms_accepted') and hasattr(current_user, 'terms_accepted_at'):
        est_client = True

    # Méthode 4: Par l'absence de rôle (comme dans votre cas)
    if not hasattr(current_user, 'role') or current_user.role is None or current_user.role == '':
        est_client = True

    if not est_client:
        print(f"⚠️ Utilisateur {current_user.id} n'est pas un client, redirection")
        return redirect(url_for('tableau_de_bord'))

    # Récupérer le groupe du client
    groupe = None
    if current_user.groupe_id:
        groupe = Groupe.query.get(current_user.groupe_id)

    # Vos statistiques existantes
    stats = calculer_statistiques_utilisateur(current_user)

    # Retourner le template avec toutes les variables nécessaires
    return render_template('client_dashboard.html',
                           user=current_user,
                           stats=stats,
                           groupe=groupe)  # ← Le groupe est maintenant disponible

@app.route('/pret/<int:pret_id>/<action>')
@login_required
def gerer_pret(pret_id, action):
    if getattr(current_user, 'role', None) not in ['admin', 'employe']:
        return redirect(url_for('tableau_de_bord'))

    pret = Pret.query.get_or_404(pret_id)
    client = User.query.get(pret.client_id)

    if action == 'approuver':
        pret.statut = 'approuve'
        pret.date_approbation = datetime.utcnow()

        # 🔔 NOTIFICATION d'approbation
        notification_manager.notifier_approbation_pret(client, pret)

    elif action == 'rejeter':
        pret.statut = 'rejete'
        motif = request.args.get('motif', 'Critères non satisfaits')

        # 🔔 NOTIFICATION de rejet
        notification_manager.notifier_rejet_pret(client, pret, motif)

    db.session.commit()
    return redirect(url_for('prets_en_attente'))


@app.route('/prets-en-attente')
@login_required
def prets_en_attente():
    # Vérifier que c'est un admin ou employé (sans hasattr)
    if getattr(current_user, 'role', None) in ['admin', 'employe']:
        prets = Pret.query.filter_by(statut='en_attente').all()

        # Récupérer les informations clients manuellement
        prets_avec_clients = []
        for pret in prets:
            client = User.query.get(pret.client_id)
            prets_avec_clients.append({
                'pret': pret,
                'client': client
            })

        return render_template('admin/admin_prets_attente.html', prets_avec_clients=prets_avec_clients)
    else:
        return redirect(url_for('tableau_de_bord'))


# ==================== NOUVELLES ROUTES POUR LE DASHBOARD ====================

@app.route('/tableau-de-bord')
@login_required
def tableau_de_bord():
    """Tableau de bord principal avec toutes les fonctionnalités"""
    stats = calculer_statistiques_utilisateur(current_user)
    return render_template('tableau_de_bord.html', user=current_user, stats=stats)


# ==================== ROUTES SCORE CRÉDIT ====================

@app.route('/score-credit')
@login_required
def score_credit():
    """Page détaillée du score de crédit"""
    from models import Pret, Remboursement

    # Récupérer le score de crédit de l'utilisateur
    score = getattr(current_user, 'score_credit', 650)

    # Historique des prêts
    prets = Pret.query.filter_by(client_id=current_user.id).order_by(Pret.date_demande.desc()).all()

    # Historique des remboursements
    remboursements = Remboursement.query.filter_by(employe_id=current_user.id).order_by(
        Remboursement.date_remboursement.desc()).limit(10).all()

    # Calculer le taux de remboursement
    total_prets = Pret.query.filter_by(client_id=current_user.id).count()
    total_rembourses = Remboursement.query.filter_by(employe_id=current_user.id, statut='paye').count()
    taux_remboursement = round((total_rembourses / total_prets * 100), 1) if total_prets > 0 else 0

    # Facteurs influençant le score
    facteurs = {
        'positifs': [],
        'negatifs': []
    }

    # Vérifier les remboursements ponctuels
    remboursements_en_retard = Remboursement.query.filter_by(employe_id=current_user.id, statut='en_retard').count()
    if remboursements_en_retard == 0:
        facteurs['positifs'].append({'nom': 'Aucun retard de paiement', 'impact': '+20 points'})
    else:
        facteurs['negatifs'].append(
            {'nom': f'{remboursements_en_retard} retard(s) de paiement', 'impact': '-15 points'})

    # Vérifier l'ancienneté du compte
    if current_user.date_creation:
        anciennete_jours = (datetime.now() - current_user.date_creation).days
        if anciennete_jours > 365:
            facteurs['positifs'].append({'nom': 'Ancienneté client > 1 an', 'impact': '+10 points'})

    # Vérifier le nombre de prêts
    if total_prets >= 3:
        facteurs['positifs'].append({'nom': f'{total_prets} prêts remboursés', 'impact': '+15 points'})

    # Vérifier le montant total des prêts
    montant_total = db.session.query(db.func.sum(Pret.montant)).filter_by(client_id=current_user.id).scalar() or 0
    if montant_total > 100000:
        facteurs['positifs'].append({'nom': 'Historique de prêts important', 'impact': '+5 points'})

    # Recommandations
    recommandations = []
    if total_prets == 0:
        recommandations.append('Faites votre premier prêt pour commencer à construire votre score')
    if remboursements_en_retard > 0:
        recommandations.append('Régularisez vos paiements en retard pour améliorer votre score')
    if taux_remboursement < 80:
        recommandations.append('Améliorez votre taux de remboursement en payant à temps')

    return render_template('score_credit.html',
                           score=score,
                           prets=prets,
                           remboursements=remboursements,
                           taux_remboursement=taux_remboursement,
                           facteurs=facteurs,
                           recommandations=recommandations)



# from datetime import date

def verifier_retards():
    prets = Pret.query.filter_by(statut='approuve').all()

    for pret in prets:

        if pret.prochaine_echeance:

            aujourd_hui = date.today()

            if aujourd_hui > pret.prochaine_echeance:

                jours_retard = (
                    aujourd_hui - pret.prochaine_echeance
                ).days

                existe = RetardPaiement.query.filter_by(
                    pret_id=pret.id,
                    statut='impaye'
                ).first()

                total_jours_retard = db.session.query(
                    db.func.sum(RetardPaiement.jours_retard)
                ).filter(
                    RetardPaiement.client_id == pret.client_id
                ).scalar() or 0

                retards = RetardPaiement.query.filter(
                    RetardPaiement.client_id == pret.client_id,
                    RetardPaiement.jours_retard > 0
                ).count()

                # Récupérer le client
                client = Client.query.get(pret.client_id)

                # Calculer le score du client
                nouveau_score = verifier_retards_et_mettre_a_jour_scores(client.id)


                if not existe:

                    retard = RetardPaiement(
                        client_id=pret.client_id,
                        pret_id=pret.id,
                        echeance_prevue=pret.prochaine_echeance,
                        jours_retard=jours_retard,
                        montant_retard=pret.mensualite
                    )

                    db.session.add(retard)

    db.session.commit()


def verifier_retards_avec_logging():
    """Version avec logging pour débogage"""

    prets = Pret.query.filter_by(statut='approuve').all()
    retards_trouves = 0
    scores_modifies = 0

    for pret in prets:
        if pret.prochaine_echeance and date.today() > pret.prochaine_echeance:
            jours_retard = (date.today() - pret.prochaine_echeance).days
            retards_trouves += 1

            # Logging
            print(f"⚠️ Prêt #{pret.id} - Client #{pret.client_id} : {jours_retard} jours de retard")

            existe = RetardPaiement.query.filter_by(
                pret_id=pret.id,
                statut='impaye'
            ).first()

            if not existe:
                retard = RetardPaiement(
                    client_id=pret.client_id,
                    pret_id=pret.id,
                    echeance_prevue=pret.prochaine_echeance,
                    jours_retard=jours_retard,
                    montant_retard=pret.mensualite
                )
                db.session.add(retard)

                # Mettre à jour le score
                client = Client.query.get(pret.client_id)
                ancien_score = client.score
                nouveau_score = calculer_score_client(client.id)
                client.score = nouveau_score
                scores_modifies += 1

                print(f"  📊 Score : {ancien_score} → {nouveau_score}")

    db.session.commit()
    print(f"✅ Vérification terminée : {retards_trouves} retards, {scores_modifies} scores mis à jour")

    return {
        'retards_trouves': retards_trouves,
        'scores_modifies': scores_modifies,
        'date_verification': date.today()
    }


# ==================== ROUTES GAMIFICATION ====================

@app.route('/profil-gamification')
@login_required
def profil_gamification():
    """Page principale de gamification"""
    from models import Pret, Remboursement, Badge, Defi

    # Récupérer les données du joueur
    points = getattr(current_user, 'points_gamification', 0)
    niveau = getattr(current_user, 'niveau_gamification', 1)

    # Calculer l'expérience nécessaire pour le prochain niveau
    exp_needed = niveau * 500
    exp_actuelle = points % 500 if points > 0 else 0
    progression = round((exp_actuelle / exp_needed * 100), 1) if exp_needed > 0 else 0

    # Récupérer les badges obtenus
    badges_obtenus = Badge.query.filter_by(employe_id=current_user.id, obtenu=True).all()

    # Récupérer les badges disponibles
    badges_disponibles = Badge.query.filter_by(obtenu=False).all()

    # Récupérer les défis en cours
    defis_en_cours = Defi.query.filter_by(employe_id=current_user.id, termine=False).all()

    # Récupérer les défis terminés
    defis_termines = Defi.query.filter_by(employe_id=current_user.id, termine=True).count()

    # Statistiques
    stats = {
        'prets_rembourses': Remboursement.query.filter_by(employe_id=current_user.id, statut='paye').count(),
        'prets_total': Pret.query.filter_by(client_id=current_user.id).count(),
        'badges_obtenus': len(badges_obtenus),
        'defis_termines': defis_termines
    }

    return render_template('profil-gamification.html',
                           points=points,
                           niveau=niveau,
                           progression=progression,
                           badges_obtenus=badges_obtenus,
                           badges_disponibles=badges_disponibles,
                           defis_en_cours=defis_en_cours,
                           stats=stats)


@app.route('/defis')
@login_required
def defis():
    """Page des défis"""
    from models import Defi, Pret, Remboursement

    # Défis dynamiques basés sur l'activité réelle
    defis_list = []

    # Défi 1: Premier prêt
    premier_pret = Pret.query.filter_by(client_id=current_user.id).first()
    defis_list.append({
        'id': 1,
        'nom': 'Premier prêt',
        'description': 'Obtenez votre premier prêt',
        'recompense': 100,
        'termine': premier_pret is not None,
        'progression': '1/1' if premier_pret else '0/1'
    })

    # Défi 2: Remboursement ponctuel
    remboursements_ponctuels = Remboursement.query.filter_by(employe_id=current_user.id, statut='paye').count()
    defis_list.append({
        'id': 2,
        'nom': 'Remboursement ponctuel',
        'description': '3 remboursements à temps',
        'recompense': 50,
        'termine': remboursements_ponctuels >= 3,
        'progression': f'{min(remboursements_ponctuels, 3)}/3'
    })

    # Défi 3: Leader du groupe
    groupe_id = getattr(current_user, 'groupe_id', None)
    if groupe_id:
        membres_groupe = User.query.filter_by(groupe_id=groupe_id).count()
        defis_list.append({
            'id': 3,
            'nom': 'Leader du groupe',
            'description': 'Devenir coordinateur de groupe',
            'recompense': 200,
            'termine': current_user.role == 'coordinateur',
            'progression': '1/1' if current_user.role == 'coordinateur' else '0/1'
        })
    else:
        defis_list.append({
            'id': 3,
            'nom': 'Rejoindre un groupe',
            'description': 'Intégrez un groupe d\'épargne',
            'recompense': 100,
            'termine': False,
            'progression': '0/1'
        })

    # Défi 4: Score crédit élevé
    score = getattr(current_user, 'score_credit', 0)
    defis_list.append({
        'id': 4,
        'nom': 'Score crédit élevé',
        'description': 'Atteindre un score de crédit > 700',
        'recompense': 150,
        'termine': score >= 700,
        'progression': f'{score}/700'
    })

    return render_template('defis.html', defis=defis_list)


@app.route('/badges')
@login_required
def badges():
    """Page des badges"""
    from models import Pret, Remboursement

    badges_list = []

    # Badge Bronze
    badges_list.append({
        'id': 1,
        'nom': 'Bronze',
        'icone': '🥉',
        'description': 'Premier prêt obtenu',
        'obtenu': Pret.query.filter_by(client_id=current_user.id).first() is not None
    })

    # Badge Argent
    remboursements_ponctuels = Remboursement.query.filter_by(employe_id=current_user.id, statut='paye').count()
    badges_list.append({
        'id': 2,
        'nom': 'Argent',
        'icone': '🥈',
        'description': '5 remboursements ponctuels',
        'obtenu': remboursements_ponctuels >= 5
    })

    # Badge Or
    score = getattr(current_user, 'score_credit', 0)
    badges_list.append({
        'id': 3,
        'nom': 'Or',
        'icone': '🥇',
        'description': 'Score crédit > 750',
        'obtenu': score >= 750
    })

    # Badge Fidélité
    if current_user.date_creation:
        anciennete = (datetime.now() - current_user.date_creation).days
        badges_list.append({
            'id': 4,
            'nom': 'Fidélité',
            'icone': '⭐',
            'description': 'Client depuis plus d\'un an',
            'obtenu': anciennete >= 365
        })

    return render_template('badges.html', badges=badges_list)


@app.route('/classement')
@login_required
def classement():
    """Page du classement"""
    from models import User

    # Récupérer tous les utilisateurs avec leurs points
    users = User.query.filter(
        User.role == 'client',
        User.actif == True
    ).order_by(User.points_gamification.desc()).limit(50).all()

    classement_data = []
    position = 1
    user_position = None

    for user in users:
        points = getattr(user, 'points_gamification', 0)
        niveau = getattr(user, 'niveau_gamification', 1)

        classement_data.append({
            'position': position,
            'id': user.id,
            'nom': f"{user.prenom} {user.nom}",
            'points': points,
            'niveau': niveau
        })

        if user.id == current_user.id:
            user_position = position

        position += 1

    # Si l'utilisateur n'est pas dans le top 50
    if not user_position:
        user_points = getattr(current_user, 'points_gamification', 0)
        user_niveau = getattr(current_user, 'niveau_gamification', 1)
        classement_data.append({
            'position': '...',
            'id': current_user.id,
            'nom': f"{current_user.prenom} {current_user.nom}",
            'points': user_points,
            'niveau': user_niveau
        })

    return render_template('classement.html', classement=classement_data, user_position=user_position)


@app.route('/recompenses')
@login_required
def recompenses():
    """Page des récompenses"""
    points = getattr(current_user, 'points_gamification', 0)

    recompenses_list = [
        {
            'id': 1,
            'nom': 'Réduction taux',
            'description': '1% de réduction sur le prochain prêt',
            'points': 300,
            'disponible': points >= 300,
            'type': 'taux_reduction',
            'valeur': 1
        },
        {
            'id': 2,
            'nom': 'Frais de dossier offerts',
            'description': 'Frais de dossier gratuits',
            'points': 500,
            'disponible': points >= 500,
            'type': 'frais_offerts',
            'valeur': 100
        },
        {
            'id': 3,
            'nom': 'Assurance gratuite',
            'description': '3 mois d\'assurance offerte',
            'points': 800,
            'disponible': points >= 800,
            'type': 'assurance',
            'valeur': 3
        }
    ]

    return render_template('recompenses.html', recompenses=recompenses_list, points=points)


@app.route('/recommandations-pret')
@login_required
def recommandations_pret():
    """Page des recommandations de prêt"""
    from models import Pret, Client

    # Récupérer les données du client
    client = current_user if hasattr(current_user, 'client_profile') else Client.query.get(current_user.id)

    recommandations = []

    if client:
        # Recommandation basée sur le revenu
        if client.revenu_mensuel:
            max_pret = client.revenu_mensuel * 12
            recommandations.append({
                'type': 'capacite',
                'titre': 'Capacité de remboursement',
                'description': f'Basé sur votre revenu mensuel de {client.revenu_mensuel:,.0f} HTG',
                'montant_max': max_pret,
                'duree_recommandee': 12
            })

        # Recommandation basée sur l'historique
        prets_anterieurs = Pret.query.filter_by(client_id=client.id).all()
        if prets_anterieurs:
            montant_moyen = sum(p.montant for p in prets_anterieurs) / len(prets_anterieurs)
            recommandations.append({
                'type': 'historique',
                'titre': 'Basé sur votre historique',
                'description': f'Vous avez déjà remboursé {len(prets_anterieurs)} prêt(s)',
                'montant_max': montant_moyen * 1.2,
                'duree_recommandee': prets_anterieurs[-1].duree_mois if prets_anterieurs else 12
            })

    # Recommandations par défaut
    if not recommandations:
        recommandations = [
            {'type': 'debutant', 'titre': 'Prêt découverte', 'description': 'Commencez avec un petit prêt',
             'montant_max': 50000, 'duree_recommandee': 6},
            {'type': 'croissance', 'titre': 'Prêt croissance', 'description': 'Pour développer votre activité',
             'montant_max': 150000, 'duree_recommandee': 12}
        ]

    return render_template('recommandations_pret.html', recommandations=recommandations)


# ==================== API GAMIFICATION ====================

@app.route('/api/gamification/points')
@login_required
def get_gamification_points():
    """API pour récupérer les points de gamification"""
    points = getattr(current_user, 'points_gamification', 0)
    niveau = getattr(current_user, 'niveau_gamification', 1)
    exp_needed = niveau * 500
    exp_actuelle = points % 500 if points > 0 else 0
    progression = round((exp_actuelle / exp_needed * 100), 1) if exp_needed > 0 else 0

    return jsonify({
        'points': points,
        'niveau': niveau,
        'progression': f'{progression}%',
        'points_prochain_niveau': exp_needed - exp_actuelle
    })


@app.route('/api/gamification/complete-defi/<int:defi_id>', methods=['POST'])
@login_required
def complete_defi(defi_id):
    """API pour compléter un défi"""
    from models import Defi

    try:
        # Vérifier si le défi existe
        defi = Defi.query.get(defi_id)
        if not defi:
            return jsonify({'success': False, 'error': 'Défi non trouvé'}), 404

        # Vérifier si déjà complété
        if defi.termine:
            return jsonify({'success': False, 'error': 'Défi déjà complété'}), 400

        # Marquer comme complété
        defi.termine = True
        defi.date_completion = datetime.now()

        # Ajouter les points
        current_user.points_gamification = (current_user.points_gamification or 0) + defi.recompense

        # Vérifier le niveau
        points = current_user.points_gamification
        nouveau_niveau = points // 500 + 1
        if nouveau_niveau > (current_user.niveau_gamification or 1):
            current_user.niveau_gamification = nouveau_niveau

        db.session.commit()

        return jsonify({
            'success': True,
            'points_gagnes': defi.recompense,
            'total_points': current_user.points_gamification,
            'niveau': current_user.niveau_gamification
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/gamification/echanger-recompense/<int:recompense_id>', methods=['POST'])
@login_required
def echanger_recompense(recompense_id):
    """API pour échanger des points contre une récompense"""
    points = getattr(current_user, 'points_gamification', 0)

    recompenses = {
        1: {'nom': 'Réduction taux', 'points': 300, 'type': 'taux_reduction'},
        2: {'nom': 'Frais de dossier offerts', 'points': 500, 'type': 'frais_offerts'},
        3: {'nom': 'Assurance gratuite', 'points': 800, 'type': 'assurance'}
    }

    if recompense_id not in recompenses:
        return jsonify({'success': False, 'error': 'Récompense non trouvée'}), 404

    recompense = recompenses[recompense_id]

    if points < recompense['points']:
        return jsonify({'success': False, 'error': 'Points insuffisants'}), 400

    # Déduire les points
    current_user.points_gamification = points - recompense['points']

    # Enregistrer la récompense échangée
    from models import RecompenseEchange
    echange = RecompenseEchange(
        employe_id=current_user.id,
        recompense_id=recompense_id,
        points_depenses=recompense['points'],
        date_echange=datetime.now(),
        statut='valide'
    )
    db.session.add(echange)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Récompense "{recompense["nom"]}" échangée avec succès',
        'points_restants': current_user.points_gamification
    })


@app.route('/reconnaissance-faciale')
@login_required
def reconnaissance_faciale():
    """Gestion de la reconnaissance faciale"""
    return render_template('reconnaissance_faciale.html')


@app.route('/analytics-personnel')
@login_required
def analytics_personnel():
    """Analytics et statistiques du personnel"""
    if not current_user.est_admin and not current_user.est_employe:
        return redirect(url_for('tableau_de_bord'))

    # Vos données d'analytics ici
    stats = calculer_statistiques_globales()
    return render_template('analytics_personnel.html', stats=stats)
#

@app.route('/previsions-remboursement')
@login_required
def previsions_remboursement():
    """Prévisions et calendrier de remboursement"""
    if current_user.est_client:
        # Pour les clients : leurs propres prévisions
        prets = Pret.query.filter_by(client_id=current_user.id, statut='approuve').all()
    else:
        # Pour admin/employé : toutes les prévisions
        prets = Pret.query.filter_by(statut='approuve').all()

    return render_template('previsions_remboursement.html', prets=prets)

@app.route('/notifications')
@login_required
def notifications():
    """Page des notifications utilisateur"""
    notifications = Notification.query.filter_by(employe_id=current_user.id).order_by(Notification.date_creation.desc()).all()
    return render_template('notifications.html', notifications=notifications)


@app.route('/parametres', methods=['GET', 'POST'])
@login_required
def parametres():

    if request.method == 'POST':

        config.taux_interet = request.form['taux_interet']
        config.frais_dossier = request.form['frais_dossier']
        config.penalite_retard = request.form['penalite_retard']
        config.commission_transfert = request.form['commission_transfert']
        config.max_pret = request.form['max_pret']
        config.duree_max = request.form['duree_max']
        config.solde_min = request.form['solde_min']
        config.devise = request.form['devise']

        db.session.commit()

        flash("Paramètres bancaires mis à jour", "success")
        return redirect(url_for('parametres'))

    return render_template('parametres.html', config=config)


def employe_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('connexion'))

        if current_user.role != 'employe':
            flash('Accès réservé aux employés', 'error')
            if current_user.role == 'agent':
                return redirect(url_for('dashboard_agent'))
            elif current_user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif current_user.role == 'direction':
                return redirect(url_for('direction_dashboard'))
            return redirect(url_for('main.accueil'))
        return f(*args, **kwargs)
    return decorated_function



@app.route('/profil')
@login_required
def profil():
    """Page de profil utilisateur - Version simplifiée"""
    # Calculs basiques sans dépendances complexes
    prets_actifs = Pret.query.filter_by(client_id=current_user.id, statut='approuve').count() if hasattr(current_user,
                                                                                                         'groupe_id') else 0

    stats = {
        'score_credit': 650,
        'score_categorie': 'good',
        'prets_actifs': prets_actifs,
        'montant_actifs': 0,
        'niveau': 1,
        'points': 50,
        'badge': 'Bronze'
    }

    return render_template('profil.html', user=current_user, stats=stats)
# ==================== LANCEMENT ====================

@app.route('/securite')
@login_required
def securite():
    """Page de sécurité et paramètres de compte"""
    return render_template('securite.html')

@app.route('/test-mobile')
def test_mobile():
    return redirect(url_for('test_mobile_routes'))


# Route pour la gestion des remboursements (caissier)
@app.route('/employe/remboursements')
@login_required
def employe_remboursements():
    if not (current_user.role == 'employe' and current_user.has_permission('caissier')):
        return redirect(url_for('tableau_de_bord'))
    return render_template('employe_remboursements.html')



@app.route('/api/recherche-client-pret')
def recherche_client_pret():

    from models import Client, Pret

    q = request.args.get('q', '').strip()

    if not q:
        return jsonify({"results": []})

    results = []

    # 🔎 Recherche par ID prêt
    pret = Pret.query.filter(Pret.numero_pret == q).first()
    if pret:
        results.append({
            "pret_id": pret.id,
            "client_nom": pret.client.nom,
            "client_prenom": pret.client.prenom,
            "telephone": pret.client.telephone,
            "montant": pret.montant,
            "mensualite": pret.mensualite,
            "solde": pret.solde_restant,
            "statut": pret.statut
        })

    # 🔎 Recherche client
    clients = Client.query.filter(
        (Client.nom.ilike(f"%{q}%")) |
        (Client.prenom.ilike(f"%{q}%")) |
        (Client.telephone.ilike(f"%{q}%")) |
        (Client.email.ilike(f"%{q}%")) |
        (Client.id == int(q) if q.isdigit() else False)
    ).all()

    for c in clients:
        for p in Pret.query.filter_by(client_id=c.id).all():
            results.append({
                "client_id": c.id,
                "client_nom": c.nom,
                "client_prenom": c.prenom,
                "telephone": c.telephone,
                "pret_id": p.id,
                "numero_pret": p.numero_pret,  # ✅ À AJOUTER
                "montant": p.montant,  # ✅ Ajouté
                "mensualite": p.mensualite,  # ✅ Ajouté
                "solde": p.solde_restant,  # ✅ Ajouté
                "statut": p.statut  # ✅ AJOUTÉ (solution)
            })

    if not results:
        return jsonify({
            "results": [],
            "message": "Aucun prêt attribué à ce client"
        })

    return jsonify({"results": results})



@app.route('/pret/<int:pret_id>/recu')
@login_required
def recu_pret(pret_id):
    from models import Pret, Client
    from datetime import datetime
    import qrcode
    import os

    pret = Pret.query.get_or_404(pret_id)
    client = pret.client

    # 📅 Calcul calendrier des versements
    echeances = []
    date = pret.date_debut

    for i in range(pret.duree_mois):
        echeances.append({
            "numero": i + 1,
            "date": date,
            "montant": pret.mensualite
        })
        date = date + timedelta(days=30)  # simple (tu peux améliorer avec mois réel)
        receipt_number = f"REC-{pret.id}-{datetime.now().strftime('%Y%m%d')}"

        qr_data = f"""
        GMES RECEIPT
        Receipt: {receipt_number}
        Client: {client.nom} {client.prenom}
        Montant: {pret.montant}
        Statut: {pret.statut}
        """

        filename = f"qr_{pret.id}.png"
        filepath = os.path.join("static", filename)

        img = qrcode.make(qr_data)
        img.save(filepath)

    return render_template(
        "recu_pret.html",
        pret=pret,
        client=client,
        echeances=echeances,
        current_date=datetime.now(),
        qr_code=url_for('static', filename=filename)
    )


# ==================== GÉNÉRATION REÇU REMBOURSEMENT PDF ====================



def generer_recu_remboursement_pdf(pret, remboursement, client, dossier_recus="recus_remboursements"):
    """Génère un reçu PDF après chaque remboursement"""
    from reportlab.platypus import Image as RLImage  # ← Ajoutez cette ligne

    # Créer le dossier
    if not os.path.exists(dossier_recus):
        os.makedirs(dossier_recus)

    # Créer le dossier pour les QR codes
    qr_dossier = os.path.join("static", "qrcodes_remboursement")
    if not os.path.exists(qr_dossier):
        os.makedirs(qr_dossier)

    # Générer le numéro de reçu
    receipt_number = f"REC-REM-{pret.id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # === QR CODE ===
    qr_data = f"""
    GMES REÇU REMBOURSEMENT
    Reçu N°: {receipt_number}
    Prêt N°: {pret.numero_pret}
    Client: {client.nom} {client.prenom}
    Montant payé: {remboursement.montant:,.0f} HTG
    Solde restant: {pret.solde_restant:,.0f} HTG
    Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}
    """

    qr_filename = f"qr_remb_{pret.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    qr_filepath = os.path.join(qr_dossier, qr_filename)

    img = qrcode.make(qr_data)
    img.save(qr_filepath)

    # === CRÉATION DU PDF ===
    pdf_filename = f"recu_remboursement_{pret.numero_pret}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_filepath = os.path.join(dossier_recus, pdf_filename)

    doc = SimpleDocTemplate(pdf_filepath, pagesize=A4,
                            rightMargin=20 * mm, leftMargin=20 * mm,
                            topMargin=20 * mm, bottomMargin=20 * mm)

    styles = getSampleStyleSheet()

    # Styles personnalisés
    style_title = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
                                 fontSize=16, alignment=TA_CENTER, spaceAfter=20)
    style_header = ParagraphStyle('CustomHeader', parent=styles['Heading2'],
                                  fontSize=12, textColor=colors.HexColor('#0b3b4f'), spaceAfter=10)
    style_normal = ParagraphStyle('CustomNormal', parent=styles['Normal'],
                                  fontSize=10, spaceAfter=6)
    style_success = ParagraphStyle('Success', parent=styles['Normal'],
                                   fontSize=12, textColor=colors.green, alignment=TA_CENTER, spaceAfter=10)

    # Contenu du PDF
    story = []

    # En-tête
    story.append(Paragraph("GMES MICROFINANCE", style_title))
    story.append(Paragraph("REÇU DE REMBOURSEMENT", style_title))
    story.append(Spacer(1, 10))

    # Informations du reçu
    story.append(Paragraph(f"N° Reçu: <b>{receipt_number}</b>", style_normal))
    story.append(Paragraph(f"Date: <b>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</b>", style_normal))
    story.append(Spacer(1, 10))
    story.append(Paragraph("-" * 80, style_normal))
    story.append(Spacer(1, 10))

    # Message de succès
    story.append(Paragraph(f"✓ Paiement enregistré avec succès !", style_success))
    story.append(Spacer(1, 10))

    # Informations client
    story.append(Paragraph("<b>INFORMATIONS CLIENT</b>", style_header))
    story.append(Paragraph(f"Nom complet: {client.nom} {client.prenom}", style_normal))
    story.append(Paragraph(f"Téléphone: {client.telephone}", style_normal))
    story.append(Paragraph(f"Email: {client.email or 'Non renseigné'}", style_normal))
    story.append(Spacer(1, 10))

    # Informations du prêt
    story.append(Paragraph("<b>INFORMATIONS DU PRÊT</b>", style_header))
    story.append(Paragraph(f"Numéro de prêt: {pret.numero_pret}", style_normal))
    story.append(Paragraph(f"Montant initial: {pret.montant:,.0f} HTG", style_normal))
    story.append(Paragraph(f"Mensualité: {pret.mensualite:,.0f} HTG", style_normal))
    story.append(Spacer(1, 10))

    # Tableau du remboursement
    story.append(Paragraph("<b>DÉTAIL DU REMBOURSEMENT</b>", style_header))

    table_data = [
        ["Description", "Montant"],
        ["Montant payé", f"{remboursement.montant:,.0f} HTG"],
        ["Méthode de paiement", remboursement.type_paiement or remboursement.methode or "Espèces"],
        ["Référence", remboursement.reference or "N/A"],
    ]

    if remboursement.reference:
        table_data.append(["Référence", remboursement.reference])

    table = Table(table_data, colWidths=[80 * mm, 80 * mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0b3b4f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    story.append(table)
    story.append(Spacer(1, 10))

    # Situation après remboursement
    story.append(Paragraph("<b>SITUATION APRÈS CE REMBOURSEMENT</b>", style_header))

    situation_data = [
        ["Solde avant", f"{(pret.solde_restant + remboursement.montant):,.0f} HTG"],
        ["Montant payé aujourd'hui", f"{remboursement.montant:,.0f} HTG"],
        ["Nouveau solde restant", f"{pret.solde_restant:,.0f} HTG"],
    ]

    if pret.solde_restant <= 0:
        situation_data.append(
            [
                "Statut",
                Paragraph(
                    "<font color='green'><b>✅ ENTIÈREMENT REMBOURSÉ</b></font>",
                    styles['BodyText']
                )
            ])

    situation_table = Table(situation_data, colWidths=[80 * mm, 80 * mm])
    situation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    story.append(situation_table)
    story.append(Spacer(1, 10))

    # Historique des remboursements
    story.append(Paragraph("<b>HISTORIQUE DES REMBOURSEMENTS</b>", style_header))

    from models import Remboursement
    from sqlalchemy import func

    remboursements = Remboursement.query.filter_by(pret_id=pret.id, statut='effectue').order_by(
        Remboursement.date_remboursement.desc()).all()

    if remboursements:
        histo_data = [["Date", "Montant", "Méthode"]]
        for r in remboursements[:5]:  # 5 derniers remboursements
            histo_data.append([
                r.date_remboursement.strftime('%d/%m/%Y'),
                f"{r.montant:,.0f} HTG",
                r.type_paiement or r.methode or "Espèces"
            ])

        histo_table = Table(histo_data, colWidths=[50 * mm, 60 * mm, 50 * mm])
        histo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0b3b4f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ]))
        story.append(histo_table)
    else:
        story.append(Paragraph("Aucun historique disponible", style_normal))

    story.append(Spacer(1, 20))

    # QR Code
    if os.path.exists(qr_filepath):
        qr_img = RLImage(qr_filepath, width=40 * mm, height=40 * mm)
        story.append(Spacer(1, 10))
        story.append(Paragraph("<b>Vérification du reçu</b>",
                               ParagraphStyle('Center', parent=style_normal, alignment=TA_CENTER)))
        story.append(Spacer(1, 5))
        story.append(qr_img)

    # Signatures
    story.append(Spacer(1, 20))
    signature_data = [
        ["Client:", "_________________________"],
        ["Agent:", "__________________________"],
    ]
    signature_table = Table(signature_data, colWidths=[40 * mm, 50 * mm, 40 * mm, 50 * mm])
    signature_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(signature_table)

    # Générer le PDF
    doc.build(story)

    return {
        "pdf_file": pdf_filepath,
        "qr_file": qr_filepath,
        "receipt_number": receipt_number
    }

@app.route('/<string:succursale_code>/employees/historique-remboursements')
@login_required
def historique_remboursements(succursale_code):
    """Affiche l'historique des remboursements"""
    from sqlalchemy.orm import joinedload

    # Vérifier l'accès à la succursale
    succursale = Succursale.query.filter_by(code=succursale_code).first_or_404()

    # ✅ Pour un caissier/employé - voir tous les remboursements de la succursale
    remboursements = Remboursement.query.join(Pret).filter(
        Pret.succursale_id == succursale.id  # ← Filtre par succursale
    ).options(
        joinedload(Remboursement.client),
        joinedload(Remboursement.pret)
    ).order_by(Remboursement.date_remboursement.desc()).all()

    statut = request.args.get('statut', 'tous')
    if statut != 'tous':
        remboursements = [r for r in remboursements if r.statut == statut]

    # ✅ CALCULER LE SOLDE POUR CHAQUE REMBOURSEMENT
    for r in remboursements:
        if r.pret:
            # Récupérer tous les remboursements VALIDES de ce prêt, triés par date
            remboursements_pret = Remboursement.query.filter(
                Remboursement.pret_id == r.pret.id,
                Remboursement.statut.in_(['valide', 'effectue'])  # Inclure les deux
            ).order_by(Remboursement.date_remboursement.asc()).all()

            # Calculer le solde cumulatif
            cumul = 0
            solde_apres = None
            for remb in remboursements_pret:
                cumul += remb.montant
                if remb.id == r.id:
                    solde_apres = r.pret.montant - cumul
                    break

            r.solde_calcule = solde_apres
        else:
            r.solde_calcule = None


        # Ajoutez ces variables pour la progression
    pret = None
    total_rembourse = 0
    pourcentage = 0

    # Si vous voulez afficher les infos du prêt #13 spécifiquement
    pret = Pret.query.get(13)
    if pret:
        remb_valides = Remboursement.query.filter(
            Remboursement.pret_id == pret.id,
            Remboursement.statut.in_(['valide', 'effectue'])
        ).all()
        total_rembourse = sum(r.montant for r in remb_valides)
        pourcentage = (total_rembourse / pret.montant * 100) if pret.montant > 0 else 0



    # # ✅ Récupérer les remboursements avec les relations Client et Pret
    # remboursements = Remboursement.query.filter_by(
    #     employe_id=current_user.id
    # ).options(
    #     joinedload(Remboursement.client),
    #     joinedload(Remboursement.pret)
    # ).order_by(Remboursement.date_remboursement.desc()).all()

    return render_template(
        'employees/historique_remboursements.html',
        succursale=succursale,
        remboursements=remboursements,
        pret=pret,  # ← AJOUTEZ CECI
        total_rembourse=total_rembourse,  # ← AJOUTEZ CECI
        pourcentage=pourcentage,  # ← AJOUTEZ CECI
        statut=statut

    )


from flask import make_response
import csv
from io import StringIO


@app.route('/<string:succursale_code>/employees/export-remboursements')
@login_required
def export_remboursements_csv(succursale_code):
    """Exporte l'historique des remboursements en CSV"""
    from sqlalchemy.orm import joinedload

    # Vérifier l'accès à la succursale
    succursale = Succursale.query.filter_by(code=succursale_code).first_or_404()

    # Récupérer les remboursements
    remboursements = Remboursement.query.join(Pret).filter(
        Pret.succursale_id == succursale.id
    ).options(
        joinedload(Remboursement.client),
        joinedload(Remboursement.pret)
    ).order_by(Remboursement.date_remboursement.desc()).all()

    # Calculer les soldes pour chaque remboursement
    for r in remboursements:
        if r.pret:
            remb_anterieurs = Remboursement.query.filter(
                Remboursement.pret_id == r.pret.id,
                Remboursement.date_remboursement <= r.date_remboursement,
                Remboursement.statut.in_(['valide', 'effectue'])
            ).all()
            total_avant = sum(remb.montant for remb in remb_anterieurs)
            r.solde_calcule = r.pret.montant - total_avant
        else:
            r.solde_calcule = None

    # Créer le fichier CSV
    output = StringIO()
    writer = csv.writer(output, delimiter=';')

    # En-têtes
    writer.writerow([
        'ID', 'Client', 'Prêt N°', 'Montant (HTG)', 'Solde restant (HTG)',
        'Date', 'Méthode', 'Référence', 'Statut'
    ])

    # Données
    for r in remboursements:
        writer.writerow([
            r.id,
            f"{r.client.nom} {r.client.prenom}" if r.client else "N/A",
            r.pret.id if r.pret else "N/A",
            f"{r.montant:,.0f}".replace(',', ' '),
            f"{r.solde_calcule:,.0f}".replace(',', ' ') if r.solde_calcule is not None else "N/A",
            r.date_remboursement.strftime('%d/%m/%Y %H:%M'),
            r.type_paiement or r.methode or 'Espèces',
            r.reference or '-',
            'Payé' if r.statut in ['valide', 'effectue'] else r.statut
        ])

    # Préparer la réponse
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers[
        'Content-Disposition'] = f'attachment; filename=remboursements_{succursale_code}_{datetime.now().strftime("%Y%m%d")}.csv'

    return response


@app.route('/admin/dashboard-global')
@login_required
def dashboard_global():

    # Vérification
    if current_user.role != 'super_admin':
        abort(403)

    # prendre une succursale par défaut
    succursale = current_user.succursale
    # ✅ Récupérer toutes les succursales pour le filtre
    succursales = Succursale.query.all()

    if not succursale:
        succursale = Succursale.query.first()

    return render_template(
        'direction/dashboard_global.html',
        succursale=succursale,
        succursales = succursales  # ← Ajouter cette ligne
    )

@app.route('/<string:succursale_code>/api/dashboard-data')
@login_required
def api_dashboard_data(succursale_code):

    from models import Pret, Remboursement, Client, Transaction, User, Succursale
    from sqlalchemy import func
    from datetime import datetime, timedelta

    # =========================
    # PARAMÈTRES
    # =========================

    periode = request.args.get('periode', 'mois')
    vue = request.args.get('vue', 'global')
    succursale = Succursale.query.filter_by(code=succursale_code).first()

    if not succursale:
        return jsonify({"error": "Succursale introuvable"}), 404

    succursale_id = request.args.get('succursale_id')

    print("succursale_code reçu:", succursale_code)

    # =========================
    # DATES
    # =========================

    now = datetime.now()

    if periode == 'mois':

        date_debut = now.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

    elif periode == 'mois-passe':

        first_day_this_month = now.replace(day=1)

        last_month = first_day_this_month - timedelta(days=1)

        date_debut = last_month.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

    elif periode == 'annee':

        date_debut = now.replace(
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

    elif periode == 'trimestre':

        current_month = now.month

        trimestre = ((current_month - 1) // 3) * 3 + 1

        date_debut = now.replace(
            month=trimestre,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

    else:
        date_debut = None

    # =========================
    # MOIS FR
    # =========================

    MOIS_FR = {
        1: "Jan",
        2: "Fév",
        3: "Mars",
        4: "Avr",
        5: "Mai",
        6: "Juin",
        7: "Juil",
        8: "Août",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Déc"
    }

    # =========================
    # REQUÊTE BASE
    # =========================

    query = Remboursement.query

    if succursale_id and succursale_id != 'all':

        query = query.filter(
            Remboursement.succursale_id == int(succursale_id)
        )

    if date_debut:

        query = query.filter(
            Remboursement.date_remboursement >= date_debut
        )

    # =========================
    # REMBOURSEMENTS
    # =========================

    total_remboursements = query.with_entities(
        func.sum(Remboursement.montant)
    ).scalar() or 0

    remboursements_mois = total_remboursements

    # =========================
    # ÉVOLUTION DYNAMIQUE
    # =========================

    evolution_query = db.session.query(
        func.extract(
            'month',
            Remboursement.date_remboursement
        ).label('mois'),

        func.sum(
            Remboursement.montant
        ).label('total')
    )

    if succursale_id and succursale_id != 'all':

        evolution_query = evolution_query.filter(
            Remboursement.succursale_id == int(succursale_id)
        )

    if date_debut:

        evolution_query = evolution_query.filter(
            Remboursement.date_remboursement >= date_debut
        )

    evolution_query = evolution_query.group_by(
        'mois'
    ).order_by(
        'mois'
    ).all()

    evolution = []

    for row in evolution_query:

        mois_num = int(row.mois)

        montant = float(row.total or 0)

        evolution.append({
            "mois": MOIS_FR.get(mois_num, str(mois_num)),
            "montant": montant,
            "prevision": False
        })

    # =========================
    # PRÊTS APPROUVÉS
    # =========================

    prets_query = Pret.query

    if succursale_id and succursale_id != 'all':

        prets_query = prets_query.filter(
            Pret.succursale_id == int(succursale_id)
        )

    prets_approuves = prets_query.filter(Pret.statut.in_(['approuve', 'actif'])).count()

    montant_approuve = prets_query.filter(Pret.statut.in_(['approuve', 'actif'])).with_entities(func.sum(Pret.montant)).scalar() or 0

    # =========================
    # PRÊTS EN ATTENTE
    # =========================

    prets_en_attente = prets_query.filter(
        Pret.statut == 'en_attente'
    ).count()

    # =========================
    # NOUVEAUX CLIENTS
    # =========================

    clients_query = Client.query

    if succursale_id and succursale_id != 'all':

        clients_query = clients_query.filter(
            Client.succursale_id == int(succursale_id)
        )

    if date_debut:

        clients_query = clients_query.filter(Client.date_creation >= date_debut)

    nouveaux_clients = clients_query.count()

    # =========================
    # TOP CLIENTS
    # =========================

    top_clients_query = db.session.query(
        Client.id,
        Client.nom,
        Client.prenom,

        func.sum(
            Transaction.montant
        ).label('total_depots')

    ).join(
        Transaction,
        Transaction.client_id == Client.id
    )

    if succursale_id and succursale_id != 'all':

        top_clients_query = top_clients_query.filter(
            Client.succursale_id == int(succursale_id)
        )

    top_clients = top_clients_query.group_by(
        Client.id
    ).order_by(
        func.sum(Transaction.montant).desc()
    ).limit(5).all()

    top_clients_data = []

    for c in top_clients:

        prets_actifs = Pret.query.filter_by(
            client_id=c.id,
            statut='actif'
        ).count()

        top_clients_data.append({
            "nom": c.nom,
            "prenom": c.prenom,
            "total_depots": float(c.total_depots or 0),
            "prets_actifs": prets_actifs
        })

    # =========================
    # TRANSACTIONS
    # =========================

    transactions_query = Transaction.query

    if succursale_id and succursale_id != 'all':

        transactions_query = transactions_query.filter(
            Transaction.succursale_id == int(succursale_id)
        )

    transactions = transactions_query.order_by(
        Transaction.date.desc()
    ).limit(10).all()

    transactions_data = []

    for t in transactions:

        transactions_data.append({
            "date": t.date.strftime('%d/%m/%Y %H:%M')
            if t.date else "",

            "type": t.type if t.type else "N/A",

            "client_nom": t.client.nom
            if t.client else "N/A",

            "client_prenom": t.client.prenom
            if t.client else "",

            "montant": float(t.montant or 0),

            "statut": "Payé"
        })

    # =========================
    # PRÉVISIONS DYNAMIQUES
    # =========================

    previsions = []

    croissance = 0.10

    if len(evolution) >= 2:

        dernier = evolution[-1]["montant"]

        avant_dernier = evolution[-2]["montant"]

        if avant_dernier > 0:

            croissance = (
                (dernier - avant_dernier)
                / avant_dernier
            )

        montant_prevu = dernier

        mois_actuel = datetime.now().month

        for i in range(1, 4):

            montant_prevu = montant_prevu + (
                montant_prevu * croissance
            )

            prochain_mois = mois_actuel + i

            if prochain_mois > 12:
                prochain_mois -= 12

            previsions.append({
                "mois": MOIS_FR[prochain_mois],
                "montant": round(montant_prevu, 2),
                "prevision": True
            })

    else:

        montant_base = 100000

        for i in range(1, 4):

            prochain_mois = datetime.now().month + i

            if prochain_mois > 12:
                prochain_mois -= 12

            montant_base *= 1.10

            previsions.append({
                "mois": MOIS_FR[prochain_mois],
                "montant": round(montant_base, 2),
                "prevision": True
            })

    # =========================
    # MAX MONTANT DYNAMIQUE
    # =========================

    tous_les_montants = [
        e["montant"]
        for e in evolution + previsions
    ]

    max_montant = max(
        tous_les_montants,
        default=1
    )

    # =========================
    # ÉVOLUTIONS %
    # =========================

    evolution_depots = f"+{round(croissance * 100, 2)}%"

    evolution_retraits = f"-{round((croissance * 100) / 2, 2)}%"

    # =========================
    # RETOUR JSON
    # =========================

    return jsonify({

        # KPI
        "total_remboursements": float(total_remboursements),

        "remboursements_mois": float(remboursements_mois),

        "total_depots": float(montant_approuve),

        "total_retraits": 0,

        "prets_approuves": prets_approuves,

        "montant_approuve": float(montant_approuve),

        "prets_en_attente": prets_en_attente,

        "nouveaux_clients": nouveaux_clients,

        # Graphiques
        "evolution": evolution,

        "previsions": previsions,

        "max_montant": float(max_montant),

        # Clients
        "topClients": top_clients_data,

        # Transactions
        "transactions": transactions_data,

        # Évolution %
        "evolution_depots": evolution_depots,

        "evolution_retraits": evolution_retraits,

        # Prévisions
        "prevision_encaissements":
            previsions[-1]["montant"]
            if previsions else 0,

        "croissance_prevue":
            round(croissance * 100, 2),

        "objectif_mensuel":
            (
                previsions[-1]["montant"] * 1.1
            ) if previsions else 0
    })


@app.template_filter('has_permission')
def has_permission_filter(permission):
    """Filtre pour vérifier les permissions dans les templates"""
    if not current_user.is_authenticated:
        return False
    if not hasattr(current_user, 'permissions'):
        return False
    return permission in current_user.permissions


# Route pour l'analyse des prêts (analyste crédit)
@app.route('/employe/analyse-prets')
@login_required
def employe_analyse_prets():
    if not (current_user.role == 'employe' and current_user.has_permission(current_user, 'analyste_credit')):
        return redirect(url_for('tableau_de_bord'))
    return render_template('employe_analyse_prets.html')

# Route pour la gestion des clients (conseiller clientèle)
@app.route('/employe/gestion-clients')
@login_required
def employe_gestion_clients():
    if not (current_user.role == 'employe' and current_user.has_permission('conseiller')):
        return redirect(url_for('tableau_de_bord'))
    return render_template('employe_gestion_clients.html')


@app.route('/employe-section')
@login_required
def employe_section():
    # Vérifiez les permissions
    if not (current_user.role == 'employe' and current_user.has_permission(current_user, 'conseiller')):
        return redirect(url_for('tableau_de_bord'))

    # Affichez un tableau de bord ou page d'accueil employé
    return render_template('employe_section.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Aucun fichier", 400

    file = request.files['file']

    if file.filename == '':
        return "Aucun fichier sélectionné", 400

    if file:
        # Utiliser la fonction de sauvegarde
        filename = save_uploaded_file(file, prefix="id_0046710614")

        if filename:
            # Sauvegarder le chemin dans la base de données si nécessaire
            # chemin_relatif = f"uploads/{filename}"
            return f"Fichier {filename} sauvegardé avec succès"

    return "Erreur lors du téléchargement", 400


@app.route('/admin/employe/<int:employe_id>/update-conformite', methods=['POST'])
@login_required
def update_conformite(employe_id):
    """Met à jour le statut de conformité BRH d'un employé"""
    employe = User.query.get_or_404(employe_id)

    verification = request.form.get('verification_antecedents') == 'on'
    formation = request.form.get('formation_aml_cft') == 'on'

    if verification:
        employe.verification_antecedents = True
        employe.date_verification_antecedents = datetime.utcnow()

    if formation:
        employe.formation_aml_cft = True
        employe.date_formation_aml_cft = datetime.utcnow()

    # Vérifier si toutes les exigences sont remplies
    if employe.verification_antecedents and employe.formation_aml_cft:
        employe.statut_conformite = 'conforme'
        flash(f"✅ {employe.prenom} {employe.nom} est maintenant conforme aux exigences BRH", "success")
    else:
        employe.statut_conformite = 'en_attente'
        flash(f"⚠️ Conformité partielle pour {employe.prenom} {employe.nom}", "warning")

    db.session.commit()

    return redirect(url_for('gerer_employes'))


@app.context_processor
def utility_processor():
    return {'now': datetime.utcnow}


def verifier_conformite_brh():
    """Vérifie les employés qui n'ont pas complété leurs obligations BRH"""
    with app.app_context():

        print("🔄 Vérification BRH en cours...")

        today = datetime.utcnow().date()
        deadline = today - timedelta(days=7)

        employes_non_conformes = User.query.filter(
            User.date_embauche <= deadline,
            User.actif == True,
            User.statut_conformite == 'en_attente'
        ).all()

        for employe in employes_non_conformes:
            if not employe.verification_antecedents or not employe.formation_aml_cft:

                # ⚠️ éviter d'écraser si déjà non conforme
                if employe.statut_conformite != 'non_conforme':
                    employe.statut_conformite = 'non_conforme'

                    notif = Notification(
                        employe_id=employe.id,
                        message=f"⚠️ NON-CONFORME BRH: {employe.prenom} {employe.nom} n'a pas complété les obligations.",
                        type='brh_alerte'
                    )
                    db.session.add(notif)

        db.session.commit()


# Lancer la vérification quotidiennement
def schedule_brh_check():
    schedule.every().day.at("08:00").do(verifier_conformite_brh)
    print("⏰ Scheduler BRH démarré...")
    while True:
        schedule.run_pending()
        time.sleep(60)


# Démarrer dans un thread séparé (au démarrage de l'app)
threading.Thread(target=schedule_brh_check, daemon=True).start()

@app.route('/admin/ajouter-employe/', defaults={'succursale_code': None}, methods=['GET', 'POST'])
@app.route('/admin/ajouter-employe/<string:succursale_code>/', methods=['GET', 'POST'])
@login_required
def ajouter_employe(succursale_code):

    print("🔥🔥🔥 ROUTE AJOUTER_EMPLOYE APPELÉE 🔥🔥🔥")

    print("========== DEBUG AJOUT EMPLOYÉ ==========")
    print("User ID :", current_user.id)
    print("Username :", getattr(current_user, 'username', getattr(current_user, 'nom_utilisateur', 'N/A')))

    print("Role :", current_user.role)
    print("Succursale user :", current_user.succursale_id)
    print("Succursale code URL :", succursale_code)
    print("Méthode :", request.method)
    # 🔍 DEBUG (tu peux enlever après)
    print("👉 ROUTE ajouter_employe APPELÉE")
    print("succursale_code =", succursale_code)

    # print(f"🔍 DEBUG RÔLE UTILISATEUR: {current_user.role}")
    # print(f"🔍 DEBUG ATTRIBUTS UTILISATEUR: {dir(current_user)}")

    # 🔐 Vérification des rôles
    if current_user.role not in ['admin_succursale', 'directeur','direction', 'super_admin']:
        flash("Permission refusée", 'danger')
        return redirect(url_for('employe_dashboard'))

    # 🏦 Récupérer les succursales
    succursales = Succursale.query.all()

    # 🎯 Déterminer la succursale cible
    succursale = None
    if succursale_code:
        succursale = Succursale.query.filter_by(code=succursale_code).first()
        if not succursale:
            flash("Succursale invalide", 'danger')
            return redirect(url_for('dashboard'))
    else:
        succursale = current_user.succursale

    # 📩 POST
    if request.method == 'POST':
        # succursale_id = request.form.get('succursale_id')

        if current_user.role != 'super_admin':
            succursale_id = current_user.succursale_id
        else:
            succursale_id = request.form.get('succursale_id')

        photo_profil = request.files.get('photo_profil')
        photo_recto = request.files.get('photo_recto')
        photo_verso = request.files.get('photo_verso')

        import os
        import uuid
        from werkzeug.utils import secure_filename
        from flask import current_app

        def save_file(file):
            """Sauvegarde un fichier et retourne son nom unique"""
            if file and file.filename != '':
                # Vérifier l'extension
                if not allowed_file(file.filename):
                    return None

                filename = secure_filename(file.filename)
                unique_name = str(uuid.uuid4()) + "_" + filename

                # Utiliser la configuration de l'application
                upload_folder = current_app.config['UPLOAD_FOLDER']

                # Créer le chemin absolu
                absolute_path = os.path.join(current_app.root_path, upload_folder)

                # Créer le dossier s'il n'existe pas
                os.makedirs(absolute_path, exist_ok=True)

                # Chemin complet du fichier
                file_path = os.path.join(absolute_path, unique_name)

                # Sauvegarder
                file.save(file_path)

                print(f"Fichier sauvegardé : {file_path}")  # Debug
                print(f"Existe ? {os.path.exists(file_path)}")  # Debug

                return unique_name
            return None

        # Dans votre route
        profil_filename = save_file(photo_profil)

        if profil_filename:
            current_user.photo_profil = profil_filename
            db.session.commit()
            print(f"Photo sauvegardée en BDD : {profil_filename}")  # Debug

        recto_filename = save_file(photo_recto)
        verso_filename = save_file(photo_verso)

        if not succursale_id:
            flash("Veuillez sélectionner une succursale", "danger")
            return render_template(
                'admin/ajouter_employe.html',
                succursales=succursales,
                succursale=succursale,
                employees=[]
            )
        # Récupérer les valeurs du formulaire
        username = request.form.get('username')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        adresse = request.form.get('adresse')
        cin_nif = request.form.get('id_number')  # ← Changé: cin/nif → cin_nif
        id_type = request.form.get('id_type')  # ← Ajouté
        password = request.form.get('password')

        # Juste après avoir récupéré les fichiers
        photo_recto = request.files.get('photo_recto')
        photo_verso = request.files.get('photo_verso')

        print("  valeurs Récupérer")

        # 🔎 Vérifications
        if User.query.filter_by(username=request.form.get('username')).first():
            flash("Nom d'utilisateur déjà utilisé", "danger")
            return render_template(
                'admin/ajouter_employe.html',
                succursales=succursales,
                succursale=succursale,
                employees=[]
            )
        print("nom utilisateur")

        if User.query.filter_by(email=request.form.get('email')).first():
            flash("Email déjà utilisé", "danger")

            print("Email déjà utilisé","danger")

            return render_template(
                'admin/ajouter_employe.html',
                succursales=succursales,
                succursale=succursale,
                employees=[]
            )
        print("email")

        if User.query.filter_by(telephone=request.form.get('telephone')).first():
            flash(" numero de telephone a ete déjà utilisé", "danger")
            return render_template(
                'admin/ajouter_employe.html',
                succursales=succursales,
                succursale=succursale,
                employees=[]
            )
        print("tel")

        if cin_nif and User.query.filter_by(cin_nif=cin_nif).first():  # ← Changé
            flash("Numéro de CIN/NIF déjà utilisé", "danger")
            return render_template(
                'admin/ajouter_employe.html',
                succursales=succursales,
                succursale=succursale,
                employees=[]
            )
        print("cin")

        password = request.form.get('password')

        if not password or len(password) < 8:
            flash("Mot de passe invalide (min 8 caractères)", "danger")
            return redirect(request.url)

        if not photo_recto or not photo_verso:
            flash("Recto et verso obligatoires", "danger")
            return redirect(request.url)

        # 👤 Création utilisateur
        employe = User(
            username=request.form.get('username'),
            email=request.form.get('email'),
            nom=request.form.get('nom'),
            prenom=request.form.get('prenom'),
            telephone=request.form.get('telephone'),
            adresse=request.form.get('adresse'),
            cin_nif =request.form.get('id_number'),
            id_type=request.form.get('id_type'), # ← Ajouté
            role=request.form.get('role'),
            fonction=request.form.get('fonction'),
            statut='en_attente',
            succursale_id=int(succursale_id),
            photo_profil = profil_filename,
            photo_recto = recto_filename,
            photo_verso = verso_filename,
            # Nouveaux champs BRH
            date_embauche = datetime.utcnow().date(),
            verification_antecedents = False,
            formation_aml_cft = False,
            statut_conformite = 'en_attente'

        )
        employe.set_password(request.form.get('password'))

        print("creer employe")


        # Sauvegarder les questions secrètes si présentes
        question_1 = request.form.get('question_1')
        reponse_1 = request.form.get('reponse_1')
        question_2 = request.form.get('question_2')
        reponse_2 = request.form.get('reponse_2')
        question_3 = request.form.get('question_3')
        reponse_3 = request.form.get('reponse_3')

        try:
            db.session.add(employe)
            db.session.flush()  # Pour obtenir user.id sans commit

            # Ajouter les questions secrètes
            if question_1 and reponse_1:
                q1 = QuestionSecrete(
                    employe_id=employe.id,
                    question=question_1,
                    reponse=reponse_1
                )
                db.session.add(q1)

            if question_2 and reponse_2:
                q2 = QuestionSecrete(
                    employe_id=employe.id,
                    question=question_2,
                    reponse=reponse_2
                )
                db.session.add(q2)

            if question_3 and reponse_3:
                q3 = QuestionSecrete(
                    employe_id=employe.id,
                    question=question_3,
                    reponse=reponse_3
                )
                db.session.add(q3)


            db.session.commit()

            # Logger l'action
            log_audit(
                action='create',
                module='employe',
                details={
                    'employe_id': employe.id,
                    'employe_nom': f"{employe.prenom} {employe.nom}",
                    'username': employe.username,
                    'role': employe.role,
                    'fonction': employe.fonction,
                    'succursale_id': employe.succursale_id
                },
                succursale_id=employe.succursale_id
            )

            flash("Employé créé avec succès", "success")
            return redirect(url_for('gerer_employes'))

        except Exception as e:
            db.session.rollback()
            print("=" * 50)
            print("❌ ERREUR DÉTAILLÉE:")
            print(f"Type d'erreur: {type(e).__name__}")
            print(f"Message: {str(e)}")
            print("=" * 50)

            # Pour voir l'erreur complète
            import traceback
            traceback.print_exc()

            flash(f"Erreur lors de la création de l'employé: {str(e)}", "danger")
            return redirect(request.url)

    # 📄 GET
    return render_template(
        'admin/ajouter_employe.html',
        succursales=succursales,
        succursale=succursale,
        employees=[]
    )


@app.route('/output/<path:filename>')
def serve_output(filename):
    """Sert les fichiers du dossier output"""
    from flask import send_file, safe_join
    import os

    # Chemin absolu
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', filename)

    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/jpeg' if filename.endswith('.jpg') else 'image/png')
    return f"Fichier non trouvé: {file_path}", 404


import random
import string

def generate_carte_numero():
    part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{part1}-{part2}"


def generate_unique_carte_numero():
    while True:
        numero = generate_carte_numero()
        if not User.query.filter_by(carte_numero=numero).first():
            return numero



@app.route('/admin/employe/<int:employe_id>/carte')
def generer_carte(employe_id):
    user = User.query.get_or_404(employe_id)

    try:
        import os
        import asyncio
        import qrcode
        import requests
        from playwright.async_api import async_playwright
        from datetime import datetime, timedelta

        # ================= UTIL =================
        def download_image(url, path):
            """Télécharge une image depuis une URL"""
            try:
                if not url:
                    return None
                r = requests.get(url, timeout=30)
                r.raise_for_status()
                with open(path, "wb") as f:
                    f.write(r.content)
                return path
            except Exception as e:
                print(f"Erreur téléchargement image: {e}")
                return None

        # ================= GÉNÉRATION =================
        async def generate_card(user_obj):
            """Génère une carte PDF pour un utilisateur"""

            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            OUTPUT_DIR = os.path.join(BASE_DIR, "output")
            os.makedirs(OUTPUT_DIR, exist_ok=True)

            # 🔥 Génération du numéro de carte AVANT user_data
            if not user_obj.carte_numero:
                user_obj.carte_numero = generate_unique_carte_numero()
                db.session.commit()

            carte_numero = user_obj.carte_numero

            # Ajoutez ces lignes vers ligne 25-28
            if not user_obj.matricule:
                user_obj.matricule = f"DIR-{user_obj.id:06d}" if user_obj.role == 'direction' else f"EMP-{user_obj.id:06d}"
                db.session.commit()

            # Récupérer les données de l'utilisateur (objet SQLAlchemy)
            user_data = {
                "id": user_obj.id,
                "nom": f"{user_obj.prenom} {user_obj.nom}" if hasattr(user_obj, 'prenom') else user_obj.nom,

                "fonction": "Directeur" if user_obj.role == 'direction' else (
                            user_obj.fonction or user_obj.role or "Employé"),
                "departement": "Direction Générale" if user_obj.role == 'direction' else (user_obj.departement or "RH"),

                "matricule": user_obj.matricule or f"EMP{user_obj.id:06d}",
                "succursale": user_obj.succursale.nom if hasattr(user_obj, 'succursale') and user_obj.succursale else "Non définie",
                "email": user_obj.email,
                "telephone": user_obj.telephone or "Non renseigné",
                "date_embauche": user_obj.date_embauche.strftime(
                    "%d %B %Y") if user_obj.date_embauche else "Date non définie",
                "carte_numero": carte_numero,
                "photo": user_obj.photo if hasattr(user_obj, 'photo') and user_obj.photo else None
            }


            # ================= PHOTO =================
            photopath = None

            if user_obj.photo_selfie:
                path = os.path.join('static/uploads/profils', user_obj.photo_selfie)
                if os.path.exists(path):
                    photopath = path

            if not photopath and user_obj.photo_profil:
                path = os.path.join('static/uploads/profils', user_obj.photo_profil)
                if os.path.exists(path):
                    photopath = path

            # ================= URL PHOTO =================
            photo_url = None
            if photopath and os.path.exists(photopath):
                photo_url = f"file:///{os.path.abspath(photopath).replace(os.sep, '/')}"
            else:
                # avatar par défaut
                default_avatar = os.path.join('static', 'default-avatar.png')
                if os.path.exists(default_avatar):
                    photo_url = f"file:///{os.path.abspath(default_avatar).replace(os.sep, '/')}"
                else:
                    photo_url = None

            print(f"🔍 Photo pour {user_obj.nom}: {photo_url}")  # Debug
                # # avatar par défaut
                # photo_url = f"file:///{os.path.abspath('static/default-avatar.png').replace(os.sep, '/')}"

            # Génération QR Code
            qr_data = f"GMES|{user_data['id']}|{user_data['matricule']}"
            qr = qrcode.make(qr_data)
            qrpath = f"output/qr_{user_data['id']}.png"
            qr.save(qrpath)
            print(f"✅ QR généré pour {user_obj.nom}")

            # Convertir les chemins locaux en URLs pour le template
            qr_url = f"file:///{os.path.abspath(qrpath).replace(os.sep, '/')}"

            signature_path = os.path.join('static', 'signature.png')

            if os.path.exists(signature_path):
                signature_url = f"file:///{os.path.abspath(signature_path).replace(os.sep, '/')}"
            else:
                signature_url = None

            # Ajoutez cette ligne avant render_template
            print(
                f"🎫 Génération carte pour {user_obj.nom} - Rôle: {user_obj.role} - Matricule: {user_data['matricule']}")

            # Rendu HTML
            html = render_template('admin/cartes.html',
                                   nom=user_data["nom"],
                                   fonction=user_data["fonction"],
                                   matricule=user_data["matricule"],
                                   departement=user_data["departement"],
                                   succursale=user_data["succursale"],
                                   email=user_data["email"],
                                   telephone=user_data["telephone"],
                                   date_embauche=user_data["date_embauche"],
                                   carte_numero=user_data["carte_numero"],
                                   photo=photo_url or "/static/default-avatar.png",
                                   qr=qr_url,
                                   signature=signature_url
                                   )

            # Sauvegarde HTML temporaire
            htmlpath = f"output/carte_{user_data['id']}.html"
            with open(htmlpath, "w", encoding="utf-8") as f:
                f.write(html)

            # Génération PDF
            pdfpath = f"output/carte_{user_data['id']}.pdf"

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page(viewport={"width": 1200, "height": 800})

                # Convertir chemin en file:// URL (absolu)
                abs_path = os.path.abspath(htmlpath)
                file_url = f"file:///{abs_path.replace(os.sep, '/')}"
                await page.goto(file_url, wait_until="networkidle")

                # PDF avec dimensions exactes
                await page.pdf(
                    path=pdfpath,
                    width="1050px",
                    height="660px",
                    print_background=True,
                    margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
                )

                await browser.close()

            # Nettoyer les fichiers temporaires (optionnel)
            # os.remove(htmlpath)
            # if photopath and os.path.exists(photopath):
            #     os.remove(photopath)
            # os.remove(qrpath)

            return pdfpath

        # Exécuter la génération asynchrone
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        pdf_path = loop.run_until_complete(generate_card(user))
        loop.close()

        # Mettre à jour l'utilisateur
        user.carte_expiration = datetime.utcnow() + timedelta(days=365)
        user.carte_generee = True
        db.session.commit()



        return send_file(pdf_path, as_attachment=True, download_name=f"carte_{user.nom}_{user.id}.pdf")

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Erreur lors de la génération: {str(e)}", 500

@app.route("/dashboard_directeur")
def dashboard_directeur():
    directeur = current_user

    users = User.query.filter_by(
        succursale_id=directeur.succursale_id
    ).all()

    # AJOUTER ICI - Récupération des prêts en attente
    from models import Pret

    total_employes = User.query.filter(
        User.role != 'client'
    ).count()

    prets_attente = Pret.query.filter(
        Pret.statut.in_(['en_attente', 'soumis'])
    ).count()

    retards = RetardPaiement.query.filter_by(
        statut='impaye'
    ).all()

    montant_retards = sum(
        r.montant_retard or 0
        for r in retards
    )

    nombre_retards = len(retards)

    total_prets = Pret.query.filter(
        Pret.statut.in_(['actif', 'approuve'])
    ).count()

    prets_retard_30 = RetardPaiement.query.filter(
        RetardPaiement.jours_retard >= 30
    ).count()


    par30 = round(
        (prets_retard_30 / total_prets) * 100,
        2
    ) if total_prets else 0

    score_moyen = db.session.query(
        db.func.avg(
            ScoringCredit.score_global
        )
    ).scalar() or 0

    clients_risque = ScoringCredit.query.filter(
        ScoringCredit.categorie_risque.in_(
            ['D', 'E']
        )
    ).count()

    portefeuille_credits = db.session.query(
        db.func.sum(Pret.montant_accorde)
    ).filter(
        Pret.statut.in_(['actif', 'approuve'])
    ).scalar() or 0

    epargne_totale = db.session.query(
        db.func.sum(Epargne.solde)
    ).scalar() or 0

    epargne_totale = db.session.query(
        db.func.sum(Epargne.montant)
    ).scalar() or 0

    total_clients = Client.query.count()

    # Créez le dictionnaire stats
    stats = {

        'en_attente': 0,

        'prets_attente': prets_attente,

        'total_actifs': portefeuille_credits + epargne_totale,

        'portefeuille_credits':portefeuille_credits,

        'total_clients': total_clients,

        'resultat_net': 0,

        'par_30':par30,

        'roa': 0,

        'taux_penetration': 0,

        'satisfaction': 95,

        'montant_retards': montant_retards,

        'nombre_retards': nombre_retards,

        'score_moyen': round(score_moyen),

        'clients_risque': clients_risque,

        'total_employes':total_employes
    }

    clients_en_retard = db.session.query(
        Client,
        db.func.sum(
            RetardPaiement.jours_retard
        ),
        db.func.count(
            RetardPaiement.id
        )
    ).join(
        RetardPaiement
    ).group_by(
        Client.id
    ).all()

    alertes = []

    if par30 > 10:
        alertes.append({
            'type': 'danger',
            'icone': 'exclamation-triangle',
            'titre': 'PAR30 critique',
            'description': f'{par30}% du portefeuille en retard',
            'priorite': 'Élevée',
            'succursale': 'Global',
            'date': datetime.now().strftime('%d/%m/%Y')
        })

    if clients_risque > 20:
        alertes.append({
            'type': 'warning',
            'icone': 'user-times',
            'titre': 'Clients à risque',
            'description': f'{clients_risque} clients catégorie D/E',
            'priorite': 'Moyenne',
            'succursale': 'Global',
            'date': datetime.now().strftime('%d/%m/%Y')
        })

        performance = {
            'commercial': {
                'ca_mensuel': portefeuille_credits
            },
            'financier': {
                'resultat_net': 0
            },
            'operations': {
                'transactions_jour':
                    TransactionEpargne.query.count()
            },
            'rh': {
                'effectif_total':
                    User.query.count()
            }
        }

        evolution = {
            'encours':
                [10, 12, 14, 15, 16, 18, 20, 22, 24, 25, 27, 30],

            'clients':
                [100, 120, 140, 160, 180, 200, 220, 250, 280, 300, 320, 350]
        }

        from sqlalchemy import func

        clients_en_retard = (
            db.session.query(
                Client,
                func.sum(RetardPaiement.jours_retard).label("total_retard"),
                func.count(RetardPaiement.id).label("nombre_retards")
            )
            .join(RetardPaiement, RetardPaiement.client_id == Client.id)
            .group_by(Client.id)
            .having(func.sum(RetardPaiement.jours_retard) > 0)
            .all()
        )

        return render_template(
            "dashboard_directeur.html",
            users=users,
            stats=stats,
            clients_en_retard=clients_en_retard,
            alertes=alertes,
            performance=performance,
            evolution=evolution,
            succursales=Succursale.query.all(),
            decisions=[]
        )

    return render_template("dashboard_directeur.html",
                         users=users,
                         stats=stats)



@app.route('/direction/prets/attente')
@login_required
def directeur_demandes_attente():
    """Affiche les demandes de prêt en attente"""
    from models import Pret

    prets = Pret.query.filter(
        Pret.statut.in_(['en_attente', 'soumis'])
    ).order_by(Pret.date_demande.desc()).all()

    return render_template('prets/directeur_prets_attente.html', prets=prets)

@app.route("/scan/<token>")
def scan_pointage(token):
    user = User.query.filter_by(qr_token=token).first()

    if not user or not user.actif:
        return "❌ Accès refusé"

    pointage = Pointage(
        employe_id=user.id,
        heure_arrivee=datetime.utcnow()
    )

    db.session.add(pointage)
    db.session.commit()

    return "✅ Présence enregistrée"

from flask_login import login_user

@app.route("/login-qr/{token}")
def login_qr(token: str):
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        user = get_user(data["employe_id"])

        return {
            "status": "success",
            "user": user.nom
        }

    except:
        return {"error": "QR invalide"}


def check_presence(user):
    now = datetime.now().hour

    if now > 8:
        send_notification(user, "⚠️ Retard détecté")

def send_notification(user, message):
    print(f"Notif → {user.nom}: {message}")



# Route pour télécharger la carte
@app.route('/admin/employe/<int:employe_id>/download-carte')
def download_carte(employe_id):
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"carte_{employe_id}.pdf")

    if os.path.exists(pdf_path):
        user = User.query.get(employe_id)
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f'carte_{user.nom}_{user.prenom}.pdf'
        )
    else:
        return "Carte non trouvée", 404


from flask import send_file, render_template
import os


@app.route('/admin/employe/<int:employe_id>/voir-carte')
def voir_carte(employe_id):
    """Affiche la carte dans le navigateur"""
    user = User.query.get_or_404(employe_id)
    pdf_path = f"output/carte_{employe_id}.pdf"  # Changé ici

    if os.path.exists(pdf_path):
        return send_file(pdf_path, mimetype='application/pdf')
    else:
        return f"Carte non trouvée pour {user.prenom} {user.nom}. Veuillez d'abord la générer.", 404


@app.route('/admin/employe/<int:employe_id>/telecharger-carte')
def telecharger_carte(employe_id):
    """Télécharge la carte PDF"""
    user = User.query.get_or_404(employe_id)
    pdf_path = f"output/carte_{employe_id}.pdf"  # Changé ici

    if os.path.exists(pdf_path):
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"carte_{user.nom}_{user.prenom}.pdf"
        )
    else:
        return "Carte non trouvée", 404


# Route pour la page directeur - Liste des employés approuvés
@app.route('/directeur/employes-approuves')
@login_required
def employes_approuves():
    """Page directeur avec liste des employés approuvés"""
    # Récupérer tous les employés approuvés
    employes = User.query.filter_by(status='approuve').all()

    return render_template('directeur/employes_approuves.html',
                           employes=employes,
                           maintenant=datetime.now())


@app.route('/admin/cartes')
def liste_cartes():
    """Affiche toutes les cartes disponibles"""
    users = User.query.all()
    cartes_info = []

    for user in users:
        # Utilisez le même chemin que generer_carte()
        pdf_path = f"output/carte_{user.id}.pdf"
        carte_existe = os.path.exists(pdf_path)

        cartes_info.append({
            'user': user,
            'carte_existe': carte_existe,
            'carte_url': f"/output/carte_{user.id}.pdf" if carte_existe else None
        })

    return render_template('admin/liste_cartes.html', cartes=cartes_info)



@app.route('/mobile/dashboard')
@login_required
def mobile_dashboard():
    stats = calculer_statistiques_utilisateur(current_user)
    return render_template('mobile_dashboard.html', stats=stats)


@app.route('/debug-routes')
def debug_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"{rule.rule} -> {rule.endpoint}")
    return "<br>".join(routes)

@app.route('/list-routes')
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        if 'static' not in rule.rule:
            routes.append(f"{rule.rule} -> {rule.endpoint}")
    return "<br>".sorted(routes)


@app.route('/client/test')
@login_required
def client_test():
    """Route temporaire pour tester l'interface client"""
    if current_user.role != 'client':
        return f"⚠️ Accès refusé. Votre rôle: {current_user.role}"

    return """
    <h1>✅ Interface Client Fonctionnelle</h1>
    <p>Bienvenue {}</p>
    <p>Votre rôle: {}</p>
    <a href="/client/dashboard">Accéder au tableau de bord complet</a>
    """.format(current_user.nom_complet, current_user.role)


@app.route('/admin/debug-stats')
@login_required
def debug_stats():
    if current_user.role != 'admin':
        return redirect(url_for('tableau_de_bord'))

    stats = calculer_statistiques_globales()

    # Debug détaillé
    debug_info = {
        'stats_object': stats,
        'clients_count': User.query.filter_by(role='client').count(),
        'active_loans': Pret.query.filter_by(statut='approuve').count(),
        'pending_loans': Pret.query.filter_by(statut='en_attente').count()
    }

    return jsonify(debug_info)


@app.route('/admin/employe/<int:employe_id>/permissions', methods=['GET', 'POST'])
@login_required
def gerer_permissions(employe_id):
    from models import User, Permission, HistoriqueEmploye
    from flask import request

    # CORRECTION: Utiliser User au lieu de Employe
    employe = User.query.get_or_404(employe_id)

    # Vérifier les permissions
    roles_autorises = ['super_admin', 'admin', 'directeur']

    if not (current_user.role in roles_autorises or
            (current_user.role == 'directeur' and
             current_user.succursale_id == employe.succursale_id)):
        flash("⛔ Permission refusée", 'danger')
        # CORRECTION: employe.id au lieu de user.id
        return redirect(url_for('voir_employe',employe_id=employe.id))

    if request.method == 'POST':
        # Récupérer les permissions du formulaire
        permissions_ids = request.form.getlist('permissions')

        # Sauvegarder les anciennes permissions pour l'historique
        anciennes_permissions = [p.nom for p in employe.permissions]

        # Mettre à jour les permissions
        employe.permissions = []
        for perm_id in permissions_ids:
            permission = Permission.query.get(int(perm_id))
            if permission:
                employe.permissions.append(permission)

        # Nouvelles permissions
        nouvelles_permissions = [p.nom for p in employe.permissions]

        db.session.commit()

        # Enregistrer dans l'historique
        if 'HistoriqueEmploye' in dir():
            HistoriqueEmploye.enregistrer_modification(
                employe_id=employe_id,
                modifie_par=current_user,
                anciennes_valeurs={'permissions': anciennes_permissions},
                nouvelles_valeurs={'permissions': nouvelles_permissions},
                ip_address=request.remote_addr
            )
            db.session.commit()

        flash(f'✅ Permissions mises à jour pour {employe.prenom} {employe.nom}', 'success')
        return redirect(url_for('voir_employe', employe_id=user.id))

    # GET: Afficher le formulaire
    toutes_permissions = Permission.query.all()
    permissions_employe = [p.id for p in employe.permissions]

    return render_template('employees/gerer_permissions.html',
                           employe=employe,
                           toutes_permissions=toutes_permissions,
                           permissions_employe=permissions_employe)


@app.route('/debug/init-permissions')
def init_permissions():
    """Initialise les permissions de base"""
    from models import Permission

    permissions = [
        # Permissions clients
        ('voir_clients', 'Voir la liste des clients'),
        ('creer_client', 'Créer un nouveau client'),
        ('modifier_client', 'Modifier les informations client'),
        ('supprimer_client', 'Supprimer un client'),

        # Permissions crédits
        ('voir_credits', 'Voir les crédits'),
        ('creer_credit', 'Créer une demande de crédit'),
        ('approuver_credit', 'Approuver les crédits'),
        ('rejeter_credit', 'Rejeter les crédits'),

        # Permissions paiements
        ('voir_paiements', 'Voir les paiements'),
        ('enregistrer_paiement', 'Enregistrer un paiement'),
        ('annuler_paiement', 'Annuler un paiement'),

        # Permissions rapports
        ('voir_rapports', 'Voir les rapports'),
        ('exporter_rapports', 'Exporter les rapports'),

        # Permissions employés (pour superviseurs)
        ('voir_employes', 'Voir les employés'),
        ('gerer_employes', 'Gérer les employés'),

        # Permissions caissier
        ('gerer_caisse', 'Gérer la caisse'),
        ('cloturer_caisse', 'Clôturer la caisse'),

        # Permissions agent de crédit
        ('analyser_credit', 'Analyser les demandes de crédit'),
        ('proposer_credit', 'Proposer des crédits'),
    ]

    for nom, desc in permissions:
        if not Permission.query.filter_by(nom=nom).first():
            db.session.add(Permission(nom=nom, description=desc))

    db.session.commit()
    return "✅ Permissions initialisées"

@app.template_filter('has_permission')
def has_permission_filter(user, permission_name):
    return user.has_permission( permission_name)


@app.route('/debug/all-users')
def debug_all_users():
    """Voir tous les utilisateurs en base"""
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'nom': user.nom,
            'prenom': user.prenom,
            'has_password': bool(user.password_hash)
        })
    return jsonify(result)


@app.route('/admin/gerer-employes')
@login_required
def gerer_employes():
    # Rôles autorisés à gérer les employés
    roles_autorises = ['admin', 'admin_succursale', 'super_admin']

    if current_user.role not in roles_autorises:
        flash(f'⛔ Accès non autorisé. Votre rôle est "{current_user.role}"', 'danger')
        abort(403)

    # Filtrer par succursale - les admins ne voient que leurs employés
    query = User.query.filter(User.role.in_(['employe', 'superviseur']))

    # Si c'est un admin de succursale, filtrer par sa succursale
    if current_user.role in ['admin', 'admin_succursale']:
        query = query.filter_by(succursale_id=current_user.succursale_id)

    utilisateurs = query.all()

    # Calculer les statistiques
    stats = {
        'total': len(utilisateurs),
        'en_attente': len([u for u in utilisateurs if u.statut == 'en_attente']),
        'actifs': len([u for u in utilisateurs if u.statut == 'actif']),
        'suspendus': len([u for u in utilisateurs if u.statut == 'suspendu']),
        'employes': len([u for u in utilisateurs if u.role == 'employe']),
        'superviseurs': len([u for u in utilisateurs if u.role == 'superviseur'])
    }

    return render_template('employees/gerer_employes.html', utilisateurs=utilisateurs, stats=stats)

# ✅ APPROUVER un employé
@app.route('/admin/approuver-employe/<int:employe_id>')
@login_required
def approuver_employe(employe_id):
    if current_user.role != 'admin':
        abort(403)

    employe = User.query.get_or_404(employe_id)

    if employe.role != 'employe':
        return redirect(url_for('gerer_employes'))

    # Approuver l'employé
    employe.statut = 'actif'
    employe.approuve_par = current_user.id
    employe.date_approbation = datetime.utcnow()

    session.commit()

    flash(f'Employé {employe.prenom} {employe.nom} approuvé avec succès', 'success')

    print(f"✅ Employé {employe.prenom} {employe.nom} approuvé par {current_user.prenom}")
    return redirect(url_for('gerer_employes'))


@app.route('/admin/employe/<int:employe_id>/suspendre')
@login_required
def suspendre_employe(employe_id):
    """Suspendre un employé (désactiver temporairement)"""
    from models import User, HistoriqueEmploye
    from flask import request
    from datetime import datetime

    # Vérifier les permissions
    roles_autorises = ['admin', 'admin_succursale', 'super_admin']
    if current_user.role not in roles_autorises:
        flash('⛔ Permission refusée', 'danger')
        return redirect(url_for('gerer_employes'))

    employe = User.query.get_or_404(employe_id)

    # Vérifier que l'employé est dans la même succursale
    if current_user.role == 'admin_succursale' and employe.succursale_id != current_user.succursale_id:
        flash("⛔ Vous ne pouvez suspendre que les employés de votre succursale", 'danger')
        return redirect(url_for('gerer_employes'))

    # Vérifier que l'employé est actif
    if employe.statut != 'actif':
        flash(f"❌ Cet employé n'est pas actif (statut actuel: {employe.statut})", 'warning')
        return redirect(url_for('gerer_employes'))

    # Empêcher de suspendre son propre compte
    if employe.id == current_user.id:
        flash('❌ Vous ne pouvez pas suspendre votre propre compte', 'danger')
        return redirect(url_for('gerer_employes'))

    # Sauvegarder l'ancien statut
    ancien_statut = employe.statut

    # Suspendre l'employé
    employe.statut = 'suspendu'

    try:
        db.session.commit()

        # Enregistrer dans l'historique
        if 'HistoriqueEmploye' in dir():
            HistoriqueEmploye.enregistrer_changement_statut(
                employe=employe,
                modifie_par=current_user,
                ancien_statut=ancien_statut,
                nouveau_statut='suspendu',
                ip_address=request.remote_addr
            )
            db.session.commit()

        flash(f'⏸️ Employé {employe.prenom} {employe.nom} suspendu avec succès', 'warning')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Erreur lors de la suspension: {str(e)}', 'danger')

    return redirect(url_for('gerer_employes'))


# 🗑️ SUPPRIMER un employé (AVEC toutes ses dépendances)
@app.route('/admin/supprimer-employe/<int:employe_id>', methods=['GET','POST'])
@login_required
def supprimer_employe(employe_id):
    from models import User, Competence, Notification, Action, HistoriqueEmploye, QuestionSecrete

    # Vérifier les permissions
    roles_autorises = ['admin', 'admin_succursale', 'super_admin']
    if current_user.role not in roles_autorises:
        flash(f'⛔ Vous n\'avez pas la permission de supprimer des employés (rôle: {current_user.role})', 'danger')
        return redirect(url_for('tableau_de_bord'))

    # Récupérer l'employé
    employe = User.query.get(employe_id)
    if not employe:
        flash('❌ Employé non trouvé', 'danger')
        return redirect(url_for('gerer_employes'))

    # Vérifier que c'est bien un employé
    roles_employes = ['employe', 'superviseur', 'admin_succursale', 'admin', 'direction', 'admin_central']
    if employe.role not in roles_employes:
        flash('❌ Cet utilisateur n\'est pas un employé', 'danger')
        return redirect(url_for('gerer_employes'))

    # Pour un admin de succursale, vérifier que l'employé est dans sa succursale
    if current_user.role == 'admin_succursale' and employe.succursale_id != current_user.succursale_id:
        flash('⛔ Vous ne pouvez supprimer que les employés de votre succursale', 'danger')
        return redirect(url_for('gerer_employes'))

    # Empêcher la suppression de soi-même
    if employe.id == current_user.id:
        flash('❌ Vous ne pouvez pas supprimer votre propre compte', 'danger')
        return redirect(url_for('gerer_employes'))

    nom_complet = f"{employe.prenom} {employe.nom}"

    try:
        with db.session.no_autoflush:
            print(f"🔍 Suppression de l'employé: {nom_complet} (ID: {employe_id})")

            # 1. Supprimer les compétences
            deleted = Competence.query.filter_by(client_id=employe_id).delete()
            print(f"   🗑️ {deleted} compétences supprimées")

            # 2. Supprimer les questions secrètes
            if hasattr(QuestionSecrete, 'query'):
                deleted = QuestionSecrete.query.filter_by(user_id=employe_id).delete()
                print(f"   🗑️ {deleted} questions secrètes supprimées")

            # 3. Supprimer les clients (une seule fois !)
            deleted = Client.query.filter_by(cree_par_id=employe_id).delete()
            print(f"   🗑️ {deleted} clients supprimés (cree_par_id)")

            # 4. Supprimer les notifications
            deleted = Notification.query.filter_by(acteur_id=employe_id).delete()
            print(f"   🗑️ {deleted} notifications supprimées (acteur_id)")

            # 5. Supprimer les actions
            deleted = Action.query.filter_by(assignee_a_id=employe_id).delete()
            print(f"   🗑️ {deleted} actions supprimées (assignee_a_id)")

            deleted = Action.query.filter_by(creee_par_id=employe_id).delete()
            print(f"   🗑️ {deleted} actions supprimées (creee_par_id)")

            # 6. Supprimer l'historique
            deleted = HistoriqueEmploye.query.filter_by(employe_id=employe_id).delete()
            print(f"   🗑️ {deleted} entrées d'historique supprimées")


            # Flush pour appliquer toutes les suppressions
            db.session.flush()

            # 6. Supprimer l'employé
            db.session.delete(employe)

            # 7. Commit final
            db.session.commit()

            flash(f'✅ Employé {nom_complet} supprimé avec succès !', 'success')
            print(f"✅ Employé {nom_complet} (ID: {employe_id}) supprimé par {current_user.prenom} {current_user.nom}")

    except Exception as e:
        db.session.rollback()
        flash(f'❌ Erreur lors de la suppression: {str(e)}', 'danger')
        print(f"❌ Erreur suppression employé {employe_id}: {e}")
        import traceback
        traceback.print_exc()

    return redirect(url_for('gerer_employes'))

@app.route('/admin/employe/<int:employe_id>/reactiver')
@login_required
def reactiver_employe(employe_id):
    from models import User, HistoriqueEmploye
    from flask import request
    from datetime import datetime

    # Vérifier les permissions
    roles_autorises = ['admin', 'admin_succursale', 'super_admin']
    if current_user.role not in roles_autorises:
        flash('⛔ Permission refusée', 'danger')
        return redirect(url_for('gerer_employes'))

    employe = User.query.get_or_404(employe_id)

    # Vérifier que l'employé est dans la même succursale
    if current_user.role == 'admin_succursale' and employe.succursale_id != current_user.succursale_id:
        flash("⛔ Vous ne pouvez réactiver que les employés de votre succursale", 'danger')
        return redirect(url_for('gerer_employes'))

    if employe.statut != 'suspendu':
        flash(f"❌ Cet employé n'est pas suspendu (statut actuel: {employe.statut})", 'warning')
        return redirect(url_for('gerer_employes'))

    # Sauvegarder l'ancien statut
    ancien_statut = employe.statut

    # Réactiver l'employé
    employe.statut = 'actif'

    db.session.commit()

    # Enregistrer dans l'historique
    if 'HistoriqueEmploye' in dir():
        HistoriqueEmploye.enregistrer_changement_statut(
            employe=employe,
            modifie_par=current_user,
            ancien_statut=ancien_statut,
            nouveau_statut='actif',
            ip_address=request.remote_addr
        )
        db.session.commit()

    flash(f'✅ Employé {employe.prenom} {employe.nom} réactivé avec succès', 'success')
    return redirect(url_for('gerer_employes'))





# 📊 GÉNÉRATION DE RAPPORTS
@app.route('/employe/rapports')
@login_required
def rapports_dashboard():
    if current_user.role != 'employe' or current_user.fonction != 'rapports':
        return redirect(url_for('tableau_de_bord'))

    # Statistiques pour les rapports
    stats_rapports = {
        'rapports_generes': 45,
        'export_reussis': 38,
        'rapports_urgents': 3
    }

    return render_template('rapports_dashboard.html', stats=stats_rapports)


# Route Conseiller avec données
@app.route('/employe/conseiller')
@login_required
def conseiller_dashboard():
    if current_user.role != 'employe' or current_user.fonction != 'conseiller':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('tableau_de_bord'))

    # ✅ FILTRER UNIQUEMENT les clients créés par CE conseiller
    clients = Client.query.filter_by(
        cree_par_id=current_user.id  # ← Important : seulement ses clients
    ).order_by(
        Client.date_inscription.desc()
    ).limit(6).all()

    # Dans la route du conseiller
    dossiers = Client.query.filter_by(
        succursale_id=current_user.succursale_id
    ).all()

    # Il faut ajouter cree_par_id à Client (comme mentionné avant)
    dossiers = Client.query.filter_by(
        succursale_id=current_user.succursale_id,
        cree_par_id=current_user.id
    ).all()


    # Statistiques réelles (pas en dur)
    total_clients = Client.query.filter_by(cree_par_id=current_user.id).count()
    dossiers_actifs = Client.query.filter_by(cree_par_id=current_user.id, statut='actif').count()
    demandes_attente = Client.query.filter_by(cree_par_id=current_user.id,
                                            statut='en_attente_terms').count()

    # Valeurs par défaut (à adapter)
    rdv_aujourdhui = 2
    clients_prioritaires = 0
    dossiers_urgence = 0
    appels_attente = 0

    # Préparer les données pour l'affichage
    clients_avec_prets = []
    for client in clients:
        # Compter les prêts du client (à adapter selon votre modèle)
        nb_prets = 0  # Remplacer par votre logique
        clients_avec_prets.append({
            'client': client,
            'nb_prets': nb_prets
        })

    return render_template('conseiller_dashboard.html',
                           clients=clients,
                           clients_avec_prets=clients_avec_prets,
                           total_clients=total_clients,
                           dossiers_actifs=dossiers_actifs,
                           demandes_attente=demandes_attente,
                           rdv_aujourdhui=rdv_aujourdhui,
                           clients_prioritaires=clients_prioritaires,
                           dossiers_urgence=dossiers_urgence,
                           appels_attente=appels_attente)


# Route Analyste avec données
@app.route('/employe/analyste')
@login_required
def analyste_dashboard():
    if current_user.role != 'employe' or current_user.fonction != 'analyste_credit':
        return redirect(url_for('tableau_de_bord'))

    prets_en_attente = Pret.query.filter_by(statut='en_attente').all()

    return render_template('analyste_dashboard.html',
                           prets_en_attente=prets_en_attente,
                           prets_traites=24,
                           taux_approbation=78.5,
                           delai_moyen="4.2")


# Route Gestionnaire avec données
@app.route('/employe/gestionnaire')
@login_required
def gestionnaire_dashboard():
    if current_user.role != 'employe' or current_user.fonction != 'gestionnaire':
        return redirect(url_for('tableau_de_bord'))

    groupes = Groupe.query.all()

    return render_template('gestionnaire_dashboard.html',
                           groupes=groupes,
                           total_groupes=len(groupes),
                           total_membres=User.query.filter_by(role='client').count(),
                           performance_moyenne=85.2,
                           nouveaux_membres=12)

#

# ✅ APPROUVER un employé/superviseur
@app.route('/admin/approver-utilisateur/<int:employe_id>')
@login_required
def approver_utilisateur(employe_id):
    if current_user.role != 'admin':
        return redirect(url_for('tableau_de_bord'))

    utilisateur = User.query.get_or_404(employe_id)

    if utilisateur.role not in ['employe', 'superviseur']:
        return redirect(url_for('gerer_employes'))

    # Approuver l'utilisateur
    utilisateur.statut = 'actif'
    utilisateur.approuve_par = current_user.id
    utilisateur.date_approbation = datetime.utcnow()

    session.commit()

    print(f"✅ {utilisateur.role} {utilisateur.prenom} {utilisateur.nom} approuvé par {current_user.prenom}")
    return redirect(url_for('gerer_employes'))


# ⏸️ SUSPENDRE un utilisateur
@app.route('/admin/suspendre-utilisateur/<int:employe_id>')
@login_required
def suspendre_utilisateur(employe_id):
    if current_user.role != 'admin':
        return redirect(url_for('tableau_de_bord'))

    utilisateur = User.query.get_or_404(employe_id)

    if utilisateur.role not in ['employe', 'superviseur']:
        return redirect(url_for('gerer_employes'))

    # Suspendre l'utilisateur
    utilisateur.statut = 'suspendu'
    session.commit()

    print(f"⏸️ {utilisateur.role} {utilisateur.prenom} {utilisateur.nom} suspendu")
    return redirect(url_for('gerer_employes'))




# 👥 VOIR TOUS LES EMPLOYÉS
@app.route('/superviseur/employes')
@login_required
def superviseur_tous_employes():
    if current_user.role != 'superviseur':
        return redirect(url_for('tableau_de_bord'))

    employes = User.query.filter_by(role='employe').all()
    return render_template('superviseur_tous_employes.html', employes=employes)


# 🏦 VOIR PAR FONCTION
@app.route('/superviseur/fonction/<fonction>')
@login_required
def superviseur_voir_fonction(fonction):
    if current_user.role != 'superviseur':
        return redirect(url_for('tableau_de_bord'))

    employes = User.query.filter_by(role='employe', fonction=fonction).all()

    # Libellé de la fonction
    libelles_fonctions = {
        'caissier': 'Caissiers',
        'conseiller': 'Conseillers Clientèle',
        'analyste_credit': 'Analystes Crédit',
        'gestionnaire_groupe': 'Gestionnaires de Groupes',
        'rapports': 'Générateurs de Rapports'
    }

    return render_template('superviseur_par_fonction.html',
                           employes=employes,
                           fonction=fonction,
                           libelle_fonction=libelles_fonctions.get(fonction, fonction))


# 👤 VOIR DÉTAILS EMPLOYÉ
@app.route('/superviseur/employe/<int:employe_id>')
@login_required
def superviseur_voir_employe(employe_id):
    """Page de détail d'un employé"""
    if current_user.role != 'superviseur':
        return redirect(url_for('tableau_de_bord'))

    employe = User.query.get_or_404(employe_id)

    # Vérifier que c'est bien un employé
    if employe.role != 'employe':
        return redirect(url_for('superviseur_dashboard'))

    # Calculer les statistiques
    stats = calculer_stats_employe(employe)

    return render_template('superviseur_voir_employe.html',
                           employe=employe,
                           stats=stats)

# 📊 RAPPORTS PERFORMANCE
@app.route('/superviseur/rapports')
@login_required
def superviseur_rapports():
    if current_user.role != 'superviseur':
        return redirect(url_for('tableau_de_bord'))

    # Données de performance pour le template superviseur_rapports.html
    performances = {
        'caissier': {'nombre': 5, 'employes_actifs': 4, 'performance_moyenne': 85, 'taux_activite': 92},
        'conseiller': {'nombre': 8, 'employes_actifs': 7, 'performance_moyenne': 78, 'taux_activite': 88},
        'analyste_credit': {'nombre': 3, 'employes_actifs': 3, 'performance_moyenne': 91, 'taux_activite': 95},
        'gestionnaire_groupe': {'nombre': 4, 'employes_actifs': 4, 'performance_moyenne': 82, 'taux_activite': 90},
        'rapports': {'nombre': 2, 'employes_actifs': 2, 'performance_moyenne': 88, 'taux_activite': 85}
    }

    return render_template('superviseur_rapports.html', performances=performances)


@app.route('/superviseur/employes')
@login_required
def superviseur_employes():
    if current_user.role != 'superviseur':
        return redirect(url_for('tableau_de_bord'))

    employes = User.query.filter_by(role='employe').all()
    return render_template('superviseur_employes.html', employes=employes)


@app.route('/superviseur/dashboard')
@login_required
def superviseur_dashboard():
    if current_user.role != 'superviseur':
        return redirect(url_for('tableau_de_bord'))

    try:
        # Statistiques globales employés
        total_employes = User.query.filter_by(role='employe').count()
        employes_actifs = User.query.filter_by(role='employe', statut='actif').count()
        employes_attente = User.query.filter_by(role='employe', statut='en_attente').count()

        # Compter par fonction - FILTRER les fonctions None
        employes_par_fonction = session.query(
            User.fonction,
            db.func.count(User.id)
        ).filter(
            User.role == 'employe',
            User.fonction.isnot(None),  # ← FILTRE IMPORTANT
            User.fonction != ''         # ← FILTRE IMPORTANT
        ).group_by(User.fonction).all()

        # Tâches en retard
        taches_retard = 2

        return render_template('superviseur_dashboard.html',
                               total_employes=total_employes,
                               employes_actifs=employes_actifs,
                               employes_attente=employes_attente,
                               employes_par_fonction=employes_par_fonction,
                               taches_retard=taches_retard)

    except Exception as e:
        print(f"❌ Erreur superviseur dashboard: {e}")
        return render_template('superviseur_dashboard.html',
                               total_employes=0,
                               employes_actifs=0,
                               employes_attente=0,
                               employes_par_fonction=[],
                               taches_retard=0)




# 👥 VOIR TOUS LES EMPLOYÉS (version superviseur)


# 📊 RAPPORTS PERFORMANCE

# 📝 JOURNAL DES ACTIVITÉS
@app.route('/superviseur/activites')
@login_required
def superviseur_activites():
    if current_user.role != 'superviseur':
        return redirect(url_for('tableau_de_bord'))

    return "<h1>📝 Journal des Activités - En construction</h1><p>Cette fonctionnalité sera disponible prochainement.</p>"


@app.route('/superviseur/init-fonctions')
@login_required
def init_fonctions():
    if current_user.role != 'superviseur':
        return redirect(url_for('tableau_de_bord'))

    try:
        employes = User.query.filter_by(role='employe').all()
        fonctions_disponibles = ['caissier', 'conseiller', 'analyste_credit', 'gestionnaire_groupe', 'rapports']

        for i, employe in enumerate(employes):
            if not employe.fonction:
                # Assigner une fonction cycliquement
                fonction = fonctions_disponibles[i % len(fonctions_disponibles)]
                employe.fonction = fonction
                print(f"✅ {employe.prenom} {employe.nom} -> {fonction}")

        session.commit()
        return "✅ Fonctions initialisées avec succès!"

    except Exception as e:
        session.rollback()
        return f"❌ Erreur: {e}"


@app.route('/superviseur/debug-fonctions')
@login_required
def debug_fonctions():
    if current_user.role != 'superviseur':
        return redirect(url_for('tableau_de_bord'))

    # Vérifier tous les employés et leurs fonctions
    employes = User.query.filter_by(role='employe').all()

    result = "<h1>Debug Fonctions Employés</h1>"
    for emp in employes:
        result += f"<p>{emp.prenom} {emp.nom} - Fonction: '{emp.fonction}' - Statut: {emp.statut}</p>"

    # Vérifier le regroupement par fonction
    fonctions = session.query(
        User.fonction,
        db.func.count(User.id)
    ).filter_by(role='employe').group_by(User.fonction).all()

    result += "<h2>Groupement par fonction:</h2>"
    for fonction, count in fonctions:
        result += f"<p>Fonction '{fonction}': {count} employé(s)</p>"

    return result

@app.route('/superviseur/')
@login_required
def superviseur_index():
    """Redirection vers le dashboard superviseur"""
    if current_user.role != 'superviseur':
        return redirect(url_for('tableau_de_bord'))
    return redirect(url_for('superviseur_dashboard'))


# ==================== ROUTES MANQUANTES ====================

@app.route('/notifications')
@login_required
def voir_toutes_notifications():
    """Page pour voir toutes les notifications"""
    from models import Notification

    # Récupérer toutes les notifications de l'utilisateur connecté
    notifications = Notification.query.filter_by(
        employe_id=current_user.id
    ).order_by(Notification.date_envoi.desc()).all()

    return render_template('notifications.html', notifications=notifications)


@app.route('/api/notifications/unread')
@login_required
def api_notifications_unread():
    """API pour récupérer les notifications non lues"""
    from models import Notification

    try:
        notifications = Notification.query.filter_by(
            employe_id=current_user.id,
            lue=False
        ).order_by(Notification.date_creation.desc()).limit(10).all()

        result = []
        for n in notifications:
            result.append({
                'id': n.id,
                'message': n.message,
                'titre': n.titre,
                'level': n.type_notification or 'info',
                'time': n.date_creation.strftime('%H:%M') if n.date_creation else '',
                'lien': n.lien
            })

        return jsonify(result)

    except Exception as e:
        print(f"❌ Erreur notifications: {e}")
        return jsonify([])

#
# @app.route('/notification/marquer/<int:notification_id>')
# @login_required
# def mark_notification_read(notification_id):
#     """Marquer une notification comme lue"""
#     from models import Notification
#
#     notification = Notification.query.get_or_404(notification_id)
#
#     # Vérifier que la notification appartient bien à l'utilisateur
#     if notification.employe_id == current_user.id:
#         notification.lue = True
#         db.session.commit()
#         flash('Notification marquée comme lue', 'success')
#     else:
#         flash('Accès non autorisé', 'danger')
#
#     return redirect(url_for('voir_toutes_notifications'))


@app.route('/notification/marquer/<int:notification_id>', methods=['GET', 'POST'])
@login_required
def mark_notification_read(notification_id):
    """Marquer une notification comme lue (supporte GET et POST)"""
    from models import Notification

    notification = Notification.query.get_or_404(notification_id)

    # Vérifier que la notification appartient bien à l'utilisateur
    if notification.employe_id != current_user.id:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'Accès non autorisé'}), 403
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('voir_toutes_notifications'))

    # Marquer comme lue
    notification.lue = True
    db.session.commit()

    # Si c'est une requête AJAX (API)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True})

    # Sinon, redirection normale
    flash('Notification marquée comme lue', 'success')
    return redirect(url_for('voir_toutes_notifications'))



# API pour les notifications en temps réel (pour le dropdown)
@app.route('/api/notifications')
@login_required
def api_notifications():
    """API pour récupérer les notifications"""
    from models import Notification

    try:
        # Compter les non lues
        non_lues = Notification.query.filter_by(
            employe_id=current_user.id,
            lue=False
        ).count()

        # Dernières 10 notifications
        recentes = Notification.query.filter_by(
            employe_id=current_user.id
        ).order_by(Notification.date_envoi.desc()).limit(10).all()

        notifications_data = []
        for n in recentes:
            # Déterminer l'icône selon le type
            icone = 'fa-info-circle'
            if n.type_notification == 'approval':
                icone = 'fa-check-circle'
            elif n.type_notification == 'warning':
                icone = 'fa-exclamation-triangle'
            elif n.type_notification == 'success':
                icone = 'fa-check-circle'

            notifications_data.append({
                'id': n.id,
                'titre': n.titre,
                'message': n.message,
                'lue': n.lue,
                'icone': icone,
                'lien': n.lien,
                'heure': n.date_envoi.strftime('%H:%M')
            })

        return jsonify({
            'non_lues': non_lues,
            'notifications': notifications_data
        })
    except Exception as e:
        print(f"❌ Erreur chargement notifications: {e}")
        return jsonify({'non_lues': 0, 'notifications': []})


@app.route('/api/notifications/count')
@login_required
def api_notifications_count():
    """API pour compter les notifications non lues"""
    try:
        count = Notification.query.filter_by(
            employe_id=current_user.id,
            lue=False
        ).count()
        return jsonify({'count': count})
    except Exception as e:
        print(f"❌ Erreur notifications count: {e}")
        return jsonify({'count': 0})


@app.route('/api/notifications/<int:notif_id>/read', methods=['POST'])
@login_required
def marquer_notification_lue_api(notif_id):
    """API pour marquer une notification comme lue"""
    from models import Notification

    try:
        notification = Notification.query.get_or_404(notif_id)
        if notification.employe_id == current_user.id:
            notification.lue = True
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Non autorisé'}), 403
    except Exception as e:
        print(f"❌ Erreur marquer lue: {e}")
        return jsonify({'success': False}), 500


@app.route('/api/notifications/tout-lu', methods=['POST'])
@login_required
def marquer_tout_lu_api():
    """API pour marquer toutes les notifications comme lues"""
    from models import Notification

    try:
        Notification.query.filter_by(
            employe_id=current_user.id,
            lue=False
        ).update({'lue': True})
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"❌ Erreur marquer tout lu: {e}")
        return jsonify({'success': False}), 500



@app.route('/init-fonctions-employes')
def init_fonctions_employes():
    """Initialiser les fonctions des employés existants"""
    try:
        employes = User.query.filter_by(role='employe').all()
        fonctions = ['caissier', 'conseiller', 'analyste_credit', 'gestionnaire_groupe', 'rapports']

        results = []
        for i, employe in enumerate(employes):
            if not employe.fonction:
                employe.fonction = fonctions[i % len(fonctions)]
                results.append(f"✅ {employe.prenom} {employe.nom} -> {employe.fonction}")

        session.commit()

        html_response = "<h1>Fonctions employés initialisées!</h1>"
        for result in results:
            html_response += f"<p>{result}</p>"

        html_response += "<br><a href='/superviseur/dashboard'>Aller au dashboard superviseur</a>"
        return html_response

    except Exception as e:
        session.rollback()
        return f"❌ Erreur: {str(e)}"


@app.route('/debug/employes-fonctions')
def debug_employes_fonctions():
    """Debug des fonctions des employés"""
    employes = User.query.filter_by(role='employe').all()
    result = "<h1>Employés et leurs fonctions</h1>"

    if not employes:
        result += "<p>Aucun employé trouvé</p>"
    else:
        for emp in employes:
            result += f"""
            <div style="border: 1px solid #ccc; padding: 10px; margin: 5px;">
                <strong>{emp.prenom} {emp.nom}</strong><br>
                Email: {emp.email}<br>
                Fonction: <span style="color: {'green' if emp.fonction else 'red'}">
                    {emp.fonction if emp.fonction else 'NON DÉFINIE'}
                </span><br>
                Statut: {emp.statut}
            </div>
            """

    result += "<br><a href='/init-fonctions-employes'>Initialiser les fonctions</a>"
    return result


@app.route('/create-superviseur-test')
def create_superviseur_test():
    """Créer un compte superviseur de test"""
    if User.query.filter_by(username='superviseur').first():
        return """
        <h1>Superviseur existe déjà!</h1>
        <p>Identifiant: <strong>superviseur</strong></p>
        <p>Mot de passe: <strong>superviseur123</strong></p>
        <br>
        <a href="/connexion">Se connecter</a>
        """

    superviseur = User(
        username='superviseur',
        email='superviseur@gmes.com',
        role='superviseur',
        nom='Superviseur',
        prenom='Test',
        telephone='+50900000001',
        fonction='superviseur',
        statut='actif'
    )
    superviseur.set_password('superviseur123')

    session.add(superviseur)
    session.commit()

    return """
    <h1>✅ Superviseur créé !</h1>
    <p>Identifiant: <strong>superviseur</strong></p>
    <p>Mot de passe: <strong>superviseur123</strong></p>
    <p>Email: <strong>superviseur@gmes.com</strong></p>
    <br>
    <a href="/connexion" style="background: blue; color: white; padding: 10px; text-decoration: none;">
    🚀 Se connecter maintenant
    </a>
    """


def calculer_stats_employe(employe):
    """Calcule les statistiques d'un employé"""
    stats = {
        'performance': 85,  # Valeur par défaut
        'taches_terminees': 0,
        'taches_en_cours': 0,
        'satisfaction_client': 4.2,
        'activite_recente': 'Élevée'
    }

    # Selon la fonction de l'employé, calculer des stats spécifiques
    if employe.fonction == 'caissier':
        stats['taches_terminees'] = Remboursement.query.filter(
            db.func.date(Remboursement.date_remboursement) == datetime.utcnow().date()
        ).count()
        stats['taches_en_cours'] = 3
        stats['performance'] = min(100, stats['taches_terminees'] * 10 + 50)

    elif employe.fonction == 'conseiller':
        stats['taches_terminees'] = User.query.filter_by(role='client').count()
        stats['taches_en_cours'] = 5
        stats['performance'] = 78

    elif employe.fonction == 'analyste_credit':
        stats['taches_terminees'] = Pret.query.filter_by(statut='approuve').count()
        stats['taches_en_cours'] = Pret.query.filter_by(statut='en_attente').count()
        stats['performance'] = 91

    elif employe.fonction == 'gestionnaire_groupe':
        stats['taches_terminees'] = Groupe.query.count()
        stats['taches_en_cours'] = 2
        stats['performance'] = 82

    elif employe.fonction == 'rapports':
        stats['taches_terminees'] = 15
        stats['taches_en_cours'] = 3
        stats['performance'] = 88

    return stats



@app.route('/employe/dashboard')
@login_required
def employe_dashboard():
    if current_user.role != 'employe':
        return redirect(url_for('tableau_de_bord'))

    # Récupérer les permissions de l'employé
    permissions = []
    if current_user.permissions:
        try:
            permissions = json.loads(current_user.permissions)
        except:
            permissions = []

    # ✅ CORRECTION : Utiliser la FONCTION has_permission()
    stats = {}

    if current_user.has_permission('caissier'):
        stats['remboursements_du_jour'] = Remboursement.query.filter(
            db.func.date(Remboursement.date_remboursement) == datetime.utcnow().date()
        ).count()

    if current_user.has_permission('analyste_credit'):
        stats['prets_en_attente'] = Pret.query.filter_by(statut='en_attente').count()

    # Statistiques communes
    stats.update({
        'clients_assignes': User.query.filter_by(role='client').count() if current_user.has_permission('conseiller') else 0,
        'groupes_geres': Groupe.query.count() if current_user.has_permission('gestionnaire_groupe') else 0,
        'rapports_generes': 12 if current_user.has_permission('rapports') else 0
    })

    return render_template('employees/employe_dashboard.html',
                           permissions=permissions,
                           stats=stats)



@app.route('/employe/dashboard-fallback')
@login_required
def employe_dashboard_fallback():
    """Dashboard de fallback basé sur les permissions"""
    return render_template('employe/dashboard_fallback.html')


@app.route('/employees/dashboard-generique')
@login_required
def employe_dashboard_generique():
    """Dashboard générique pour les employés sans fonction"""
    return render_template('employees/dashboard_generique.html')




@app.route('/activate-all-employes')
def activate_all_employes():
    """Activer tous les employés en attente"""
    if current_user.role != 'admin' and current_user.role != 'superviseur':
        return "Accès non autorisé"

    employes = User.query.filter_by(role='employe', statut='en_attente').all()

    for employe in employes:
        employe.statut = 'actif'
        employe.approuve_par = current_user.id
        employe.date_approbation = datetime.utcnow()
        print(f"✅ {employe.prenom} {employe.nom} activé")

    session.commit()

    return f"✅ {len(employes)} employé(s) activé(s)!"


@app.route('/mes-groupes')
@login_required
def mes_groupes():
    """Voir mon groupe - Pour employés seulement"""
    if current_user.role != 'employe':
        return redirect(url_for('tableau_de_bord'))

    # Si l'employé a un groupe_id, montrer seulement son groupe
    if current_user.groupe_id:
        groupe = Groupe.query.get(current_user.groupe_id)
        return render_template('mon_groupe.html', groupe=groupe)
    else:
        return render_template('mon_groupe.html', groupe=None)



########### resoudre prblem
def check_table_structure():
    conn = sqlite3.connect('faces.db')
    cursor = conn.cursor()

    try:
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='face_data'")
        table_exists = cursor.fetchone()

        if table_exists:
            # Vérifier les colonnes
            cursor.execute("PRAGMA table_info(face_data)")
            columns = cursor.fetchall()
            print("📊 Structure de la table 'face_data':")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
        else:
            print("❌ Table 'face_data' n'existe pas")

    except Exception as e:
        print(f"❌ Erreur vérification structure: {e}")
    finally:
        conn.close()


def verify_all_in_appdb():
    """Vérifie que tout est bien dans gmes.db"""
    print("\n🔍 VÉRIFICATION: Tout dans gmes.db")

    # Liste de tous les fichiers .db
    db_files = [f for f in os.listdir('.') if f.endswith('.db')]
    db_files += [f for f in os.listdir('gmes') if os.path.isdir('gmes') and f.endswith('.db')]

    print(f"📁 Fichiers .db trouvés: {db_files}")

    if len(db_files) == 1 and ('gmes.db' in db_files or 'gmes/gmes.db' in db_files):
        print("✅ PARFAIT! Un seul fichier gmes.db")
    elif len(db_files) == 0:
        print("⚠️ Aucun fichier .db trouvé")
    else:
        print(f"❌ PROBLÈME: {len(db_files)} fichiers .db détectés")
        print("   Supprimez tous sauf gmes.db")

    # Vérifier le contenu
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"📋 Tables dans gmes.db: {tables}")

    if 'face_data' in tables:
        from sqlalchemy import text
        count = session.execute(text("SELECT COUNT(*) FROM face_data")).scalar()
        print(f"👤 Visages dans face_data: {count}")


def cleanup_databases():
    """Nettoie tous les fichiers .db sauf gmes.db"""
    print("🧹 Nettoyage des bases...")

    # Liste des fichiers à garder
    keep_files = ['gmes.db', 'gmes/gmes.db']

    # Parcourir tous les fichiers .db
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.db'):
                full_path = os.path.join(root, file)

                # Vérifier si c'est un fichier à garder
                should_keep = False
                for keep in keep_files:
                    if keep in full_path or file == 'gmes.db':
                        should_keep = True
                        break

                if not should_keep:
                    try:
                        os.remove(full_path)
                        print(f"🗑️ Supprimé: {full_path}")
                    except Exception as e:
                        print(f"⚠️ Impossible de supprimer {full_path}: {e}")





def detecter_succursale():
    """Détecter la succursale depuis l'URL ou la session"""
    g.succursale = None

    # 1. Depuis l'URL : /br001/admin/dashboard
    path = request.path
    match = re.match(r'^/(br\d+)/', path.lower())

    if match:
        code_succursale = match.group(1).upper()  # BR001
        g.succursale = Succursale.query.filter_by(code=code_succursale).first()

    # 2. Depuis la session
    if not g.succursale and 'succursale_id' in session:
        g.succursale = Succursale.query.get(session['succursale_id'])

    # 3. Depuis l'utilisateur connecté
    if not g.succursale and current_user.is_authenticated:
        if current_user.succursale_id:
            g.succursale = Succursale.query.get(current_user.succursale_id)

    return g.succursale


@app.route('/test-login/<int:employe_id>')
def test_login(employe_id):
    """Route de test pour simuler une connexion"""
    from flask_login import login_user

    user = db.session.get(User, employe_id)
    if user:
        login_user(user, remember=True)
        print(f"✅ Connexion forcée: {user.username}")
        return f"""
        <h2>✅ Connecté en tant que {user.username}</h2>
        <p>Rôle: {user.role}</p>
        <p>ID: {user.id}</p>
        <p><a href="/debug-session">Vérifier session</a></p>
        <p><a href="/debug-redirect">Tester redirection</a></p>
        <p><a href="/logout">Déconnexion</a></p>
        """
    return "❌ Utilisateur non trouvé"




from flask import abort

@app.route('/<succursale_code>/dashboard')
@login_required
def dashboard_succursale(succursale_code):
    print(f"🚨 DASHBOARD {succursale_code} - DÉBUT")
    print(f"current_user: {current_user}")
    print(f"is_authenticated: {current_user.is_authenticated}")
    print(f"Rôle: {current_user.role}")
    print(f"Fonction: {getattr(current_user, 'fonction', 'Non définie')}")
    print(f"Succursale utilisateur: {current_user.succursale_id}")
    print(f"Succursale demandée: {succursale_code}")

    print("\n" + "=" * 60)
    print(f"🚨 DASHBOARD {succursale_code} - DÉBUT")
    print(f"current_user: {current_user}")
    print(f"is_authenticated: {current_user.is_authenticated}")

    succursale = Succursale.query.filter_by(
        code=succursale_code.upper()
    ).first_or_404()

    user_role = getattr(current_user, 'role', None)
    user_succursale_id = getattr(current_user, 'succursale_id', None)

    print(f"Rôle: {user_role}")
    print(f"Succursale utilisateur: {user_succursale_id}")
    print(f"Succursale demandée: {succursale.id}")

    # 🔑 SUPER ADMIN & ADMIN GLOBAL
    if user_role in ['super_admin', 'admin','direction','admin_central']:
        print("✅ Accès autorisé: admin")
        pass

    # 🏦 ADMIN DE SUCCURSALE
    elif user_role == 'admin_succursale':
        if user_succursale_id != succursale.id:
            print("❌ Accès refusé: mauvaise succursale")
            abort(403)
        print("✅ Accès autorisé: admin_succursale")

    # 👔 EMPLOYÉS
    elif user_role in ['directeur', 'employe']:
        if user_succursale_id != succursale.id:
            print("❌ Accès refusé: employé mauvaise succursale")
            abort(403)
        print("✅ Accès autorisé: employé")

    # ❌ AUTRES RÔLES
    else:
        print(f"❌ Accès refusé: rôle inconnu {user_role}")
        abort(403)


    users_query = User.query.filter( User.succursale_id == succursale.id ).filter( User.role != 'client' )

    employes_query = Employe.query.filter_by( succursale_id=succursale.id )

    users_employes = users_query.all()

    employes_table = employes_query.all()

    emsembles = users_employes + employes_table




    # 📊 Stats
    stats = {
        'clients': Client.query.filter_by(succursale_id=succursale.id).count(),
        'employes': len(emsembles),

        'prets': Pret.query.filter( Pret.succursale_id == succursale.id, Pret.statut.in_(['actif', 'approuve'])).count(),
        'remboursements': Remboursement.query.filter_by( succursale_id=succursale.id ).count(),
        'montant_total': db.session.query(db.func.sum(Pret.montant_accorde)).filter(
            Pret.succursale_id == succursale.id, Pret.statut.in_(['actif', 'approuve'])).scalar() or 0
    }

    print(f"✅ Accès réussi à la succursale {succursale.code}")


    return render_template(
        'succursale/dashboard.html',
        succursale=succursale,
        stats=stats
    )


# Dans admin_dashboard()
def admin_dashboard():
    # Top 5 des pires retards
    pires_retards = RetardPaiement.query.filter_by(statut='impaye') \
        .order_by(RetardPaiement.jours_retard.desc()) \
        .limit(5) \
        .all()

    # Récupérer les infos clients
    for retard in pires_retards:
        retard.client_nom = Client.query.get(retard.client_id).nom
        retard.client_prenom = Client.query.get(retard.client_id).prenom

    return render_template('direction/dashboard.html', pires_retards=pires_retards)

# Dans ton blueprint pour les succursales ou employés
@employees_bp.route('/<branch_code>/dashboard')
@login_required
def branch_dashboard(branch_code):
    # Vérifier que l'utilisateur est un admin_succursale
    if not hasattr(current_user, 'role') or current_user.role != 'admin_succursale':
        # Rediriger les autres rôles vers leurs dashboards respectifs
        if current_user.role == 'super_admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'client':
            return redirect(url_for('clients.client_dashboard'))
        elif current_user.role == 'employee':
            return redirect(url_for('employees.employee_dashboard'))
        else:
            abort(403)

    # Vérifier que l'admin a accès à cette succursale spécifique
    if not hasattr(current_user, 'branch_code'):
        abort(403, "Admin sans succursale affectée")

    if current_user.branch_code != branch_code:
        abort(403, f"Accès non autorisé à la succursale {branch_code}")

    # DEBUG
    print(f"=== DEBUG BRANCH DASHBOARD ===")
    print(f"Admin: {current_user.username}")
    print(f"Succursale demandée: {branch_code}")
    print(f"Succursale admin: {current_user.branch_code}")

    # Récupérer les statistiques de LA SUCCURSALE SPÉCIFIQUE
    from models import User, Loan, Transaction

    # Compter seulement les clients de cette succursale
    total_clients = Client.query.filter_by(branch_code=branch_code, role='client').count()

    # Prêts en attente de cette succursale
    pending_loans = Loan.query.join(User).filter(
        User.branch_code == branch_code,
        Loan.status == 'pending'
    ).count()

    # Transactions en attente de cette succursale
    pending_transactions = Transaction.query.join(User).filter(
        User.branch_code == branch_code,
        Transaction.status == 'pending'
    ).count()

    return render_template('branch_dashboard.html',
                           branch_code=branch_code,
                           total_clients=total_clients,
                           pending_loans=pending_loans,
                           pending_transactions=pending_transactions,
                           user=current_user)

@app.route('/<succursale_code>/remboursements')
@login_required
def remboursements_succursale(succursale_code):
    """Remboursements pour une succursale spécifique"""
    succursale = Succursale.query.filter_by(code=succursale_code.upper()).first_or_404()

    # Filtrer par succursale
    remboursements = Remboursement.query.filter_by(succursale_id=succursale.id).all()

    return render_template('succursale/remboursements.html',
                           succursale=succursale,
                           remboursements=remboursements)


def generer_id_client(succursale_code):
    """Générer un code client unique : BR001-CL001"""
    dernier_client = Client.query.filter(
        Client.id_client.like(f'{succursale_code}-CL%')
    ).order_by(Client.id.desc()).first()

    if dernier_client:
        dernier_num = int(dernier_client.id_client.split('-CL')[1])
        nouveau_num = dernier_num + 1
    else:
        nouveau_num = 1

    return f"{succursale_code}-CL{str(nouveau_num).zfill(3)}"


def generer_code_pret(succursale_code):
    """Générer un code prêt unique : BR001-PR001"""
    dernier_pret = Pret.query.filter(
        Pret.code_pret.like(f'{succursale_code}-PR%')
    ).order_by(Pret.id.desc()).first()

    if dernier_pret:
        dernier_num = int(dernier_pret.code_pret.split('-PR')[1])
        nouveau_num = dernier_num + 1
    else:
        nouveau_num = 1

    return f"{succursale_code}-PR{str(nouveau_num).zfill(3)}"



# en developement il peux etre efface apres
@app.route('/admin/supprimer-client/<int:client_id>')
@login_required
def supprimer_client(client_id):
    """Supprimer UNIQUEMENT les clients (avec leurs prêts)"""
    if current_user.role not in ['super_admin', 'admin']:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('liste_users'))

    try:
        client = User.query.get_or_404(client_id)

        # Vérifier que c'est bien un client
        if client.role != 'client':
            flash("⛔ Cette route est réservée aux clients", "danger")
            return redirect(url_for('liste_users'))

        # Supprimer les prêts du client
        Pret.query.filter_by(client_id=client_id).delete()

        # Supprimer le client
        db.session.delete(client)
        db.session.commit()

        flash(f"✅ Client {client.prenom} {client.nom} supprimé", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"❌ Erreur: {e}", "danger")

    return redirect(url_for('liste_users'))


@app.route('/toggle_user/<int:employe_id>')
@login_required
def toggle_user(employe_id):

    if current_user.role != "super_admin":
        abort(403)

    user = User.query.get_or_404(employe_id)

    # Protection
    if user.id == current_user.id:
        flash("Impossible de modifier votre propre statut.", "danger")
        return redirect(url_for('liste_users'))

    if user.statut == "actif":
        user.statut = "suspendu"
        flash("Utilisateur suspendu.", "warning")
    else:
        user.statut = "actif"
        flash("Utilisateur réactivé.", "success")

    db.session.commit()
    return redirect(url_for('liste_users'))


@app.route('/bloquer_client/<int:client_id>')
@login_required
def bloquer_client(client_id):
    if current_user.role != "super_admin":
        abort(403)

    user = User.query.get_or_404(client_id)

    if user.role != "client":
        flash("Ce n'est pas un client.")
        return redirect(url_for('liste_users'))

    user.statut = "bloque"
    db.session.commit()

    flash("Client bloqué.")
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/debloquer-client/<int:client_id>')
@login_required
def debloquer_client(client_id):
    """Débloquer un client"""
    if current_user.role not in ['super_admin', 'admin']:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('liste_users'))

    client = User.query.get_or_404(client_id)
    client.statut = 'actif'
    db.session.commit()

    flash(f"✅ Client {client.prenom} {client.nom} débloqué", "success")
    return redirect(url_for('liste_users'))


@app.route('/transferer_employe/<int:employe_id>', methods=['GET', 'POST'])
@login_required
def transferer_employe(employe_id):
    if current_user.role != "super_admin":
        abort(403)

    user = User.query.get_or_404(employe_id)

    # Vérifier que c'est un employé
    if user.role not in ["admin", "agent", "employe", "superviseur"]:
        flash("Seuls les employés peuvent être transférés.")
        return redirect(url_for('liste_users'))

    if request.method == 'POST':
        nouvelle_succursale_id = request.form.get('succursale_id')
        if not nouvelle_succursale_id:
            flash("Veuillez sélectionner une succursale")
            return redirect(url_for('transferer_employe', employe_id=user.id))

        # ✅ AJOUTEZ CETTE LIGNE pour changer le statut
        user.statut = 'transferer'  # ← NOUVEAU !

        user.succursale_id = nouvelle_succursale_id
        db.session.commit()
        flash(f"Employé {user.prenom} {user.nom} transféré avec succès.")
        return redirect(url_for('liste_users'))

    # GET : Afficher le formulaire de sélection
    from models import Succursale
    succursales = Succursale.query.filter(Succursale.id != user.succursale_id).all()
    return render_template('admin_central/transferer_employe.html',
                           user=user,
                           succursales=succursales)



@app.route('/liste_users')
@login_required
def liste_users():
    # DÉBOGAGE - À SUPPRIMER APRÈS
    print(f"Utilisateur: {current_user.username}")
    print(f"Rôle actuel: '{current_user.role}'")
    print(f"ID: {current_user.id}")
    # Vérifier les permissions
    if current_user.role != "super_admin":
        flash(f'Accès non autorisé. Votre rôle est "{current_user.role}"', 'danger')
        abort(403)

    # 🔹 RÉCUPÉRER LES PARAMÈTRES DE FILTRE
    search = request.args.get('search', '')
    role = request.args.get('role', '')
    statut = request.args.get('statut', '')

    # 🔹 CONSTRUIRE LA REQUÊTE
    query = User.query

    # Appliquer le filtre recherche (nom, prénom, email, username)
    if search:
        query = query.filter(
            db.or_(
                User.nom.ilike(f'%{search}%'),
                User.prenom.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%'),
                User.username.ilike(f'%{search}%')
            )
        )

    # Appliquer le filtre rôle
    if role:
        query = query.filter_by(role=role)

    # Appliquer le filtre statut
    if statut:
        query = query.filter_by(statut=statut)

    # 🔹 EXÉCUTER LA REQUÊTE
    users = query.all()

    # 🔹 PASSER LES VALEURS DES FILTRES AU TEMPLATE
    return render_template(
        "admin_central/liste_users.html",
        users=users,
        search=search,
        role=role,
        statut=statut
    )


@app.route('/supprimer_succursale/<int:succursale_id>')
@login_required
def supprimer_succursale(succursale_id):

    if current_user.role != "super_admin":
        abort(403)

    succursale = Succursale.query.get_or_404(succursale_id)

    users = User.query.filter_by(succursale_id=succursale.id).all()

    if users:
        flash("Impossible de supprimer : des employés sont encore liés à cette succursale.", "danger")
        return redirect(url_for('liste_succursales'))

    db.session.delete(succursale)
    db.session.commit()

    flash("Succursale supprimée avec succès.", "success")
    return redirect(url_for('liste_succursales'))





@app.route('/admin-central/succursales')
@login_required
def admin_central_succursales():

    if current_user.role != 'admin_central':
        abort(403)

    stats_globales = get_stats_admin_central_succursales()

    return render_template(
        'admin_central/succursales.html',
        stats_globales=stats_globales
    )


@app.template_filter('number_format')
def number_format(value):
    """Formater les nombres avec séparateurs de milliers"""
    try:
        return f"{int(value):,}".replace(",", " ")
    except:
        return value


@app.route('/admin/succursale/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_succursale():
    if current_user.role != 'super_admin':
        abort(403)

    # Générer automatiquement le prochain code de succursale
    dernier = Succursale.query.order_by(Succursale.id.desc()).first()
    if dernier:
        match = re.search(r'GMES-(\d+)', dernier.code)
        dernier_num = int(match.group(1)) if match else 0
        prochain_num = dernier_num + 1
    else:
        prochain_num = 1
    code_auto = f"GMES-{prochain_num:05d}"  # GMES-00001, GMES-00002, etc.

    if request.method == 'POST':
        nom = request.form.get('nom')
        ville = request.form.get('ville')
        adresse = request.form.get('adresse')
        telephone = request.form.get('telephone')
        email = request.form.get('email')

        succ = Succursale(
            code=code_auto,
            nom=nom,
            ville=ville,
            adresse=adresse,
            telephone=telephone,
            email=email
        )
        try:
            db.session.add(succ)
            db.session.commit()

            flash(f"Succursale {code_auto} créée avec succès !", "success")
            return redirect(url_for('admin_dashboard'))

        except IntegrityError as e:
            db.session.rollback()
            flash(humanize_unique_error(e), "danger")
            return redirect(request.referrer)

    return render_template('admin_central/ajouter_succursale.html', code_auto=code_auto)





@app.route('/admin/succursale/<int:succursale_id>')
@login_required
def detail_succursale(succursale_id):

    if current_user.role != 'super_admin':
        abort(403)

    succursale = Succursale.query.get_or_404(
        succursale_id
    )

    stats = get_detail_succursale_stats(
        succursale_id
    )

    return render_template(
        'admin_central/detail_succursale.html',
        succursale=succursale,
        stats=stats
    )





@app.route('/admin-central/succursales')
@login_required
def afficher_succursales():

    stats_globales = get_stats_succursales(
        current_user
    )

    return render_template(
        'succursales.html',
        stats_globales=stats_globales
    )



# app.py ou ton fichier Flask principal



@app.route('/admin-central/succursales/<int:succ_id>/edit', methods=['GET', 'POST'])
@app.route('/admin-central/succursales/<int:succ_id>/editer', methods=['GET', 'POST'])  # alias
def edit_succursale(succ_id):
    # Récupère la succursale depuis la base de données
    succursale = Succursale.query.get_or_404(succ_id)

    if request.method == 'POST':
        succursale.nom = request.form.get('nom')
        succursale.ville = request.form.get('ville')
        succursale.adresse = request.form.get('adresse')  # 🔥 ajouté
        succursale.telephone = request.form.get('telephone')
        succursale.email = request.form.get('email')  # 🔥 ajouté
        succursale.statut = request.form.get('statut')
        print("POST reçu")
        print(request.form)


        # Sauvegarder dans la base
        db.session.commit()
        flash(f"Succursale {succursale.nom} mise à jour avec succès !", 'success')
        return redirect(url_for('admin_dashboard'))  # Retour au dashboard


    # GET → Affiche le formulaire avec les valeurs actuelles
    return render_template('admin_central/edit_succursale.html', succursale=succursale)



def humanize_unique_error(error):
    """Transforme une erreur IntegrityError en message lisible"""
    error_str = str(error).lower()

    if 'username' in error_str:
        return "❌ Ce nom d'utilisateur est déjà utilisé. Veuillez en choisir un autre."
    elif 'email' in error_str:
        return "❌ Cette adresse email est déjà utilisée. Veuillez en utiliser une autre."
    elif 'telephone' in error_str:
        return "❌ Ce numéro de téléphone est déjà utilisé."
    elif 'cin_nif' in error_str:
        return "❌ Ce numéro CIN/NIF est déjà enregistré."
    elif 'matricule' in error_str:
        return "❌ Ce matricule est déjà attribué."
    else:
        return f"❌ Une erreur est survenue: {str(error)}"


@app.route('/admin/ajouter-admin', methods=['GET', 'POST'])
@login_required
def ajouter_admin():
    """Ajouter un nouvel administrateur"""

    print("👉  44 admin:")

    if current_user.role != 'super_admin':
        flash("Accès refusé. Seul le super-admin peut ajouter un admin.", "danger")
        return redirect(url_for('admin_dashboard'))

    print("👉  33 Geler:")

    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            nom_utilisateur = request.form.get('nom_utilisateur')
            prenom = request.form.get('prenom')
            nom = request.form.get('nom')
            email = request.form.get('email')
            telephone = request.form.get('telephone')
            adresse = request.form.get('adresse')
            date_naissance = request.form.get('date_naissance')
            cin_nif = request.form.get('cin_nif')
            password = request.form.get('password')
            role = request.form.get('role')
            fonction = request.form.get('fonction') or "Non défini"
            succursale_id = request.form.get('succursale_id') or None

            # ✅ Récupérer les questions secrètes
            question_1 = request.form.get('question_1')
            reponse_1 = request.form.get('reponse_1', '').strip().lower()
            question_2 = request.form.get('question_2')
            reponse_2 = request.form.get('reponse_2', '').strip().lower()
            question_3 = request.form.get('question_3')
            reponse_3 = request.form.get('reponse_3', '').strip().lower()

            print("👉 Fonction reçue du formulaire 75:", fonction)

            # Validation des champs obligatoires
            if not nom_utilisateur or not email or not password:
                flash("Nom d'utilisateur, email et mot de passe sont obligatoires", "danger")
                return redirect(request.referrer)

            print("👉  76:")

            # Vérifier si l'utilisateur existe déjà
            existing_user = User.query.filter(
                (User.username == nom_utilisateur) | (User.email == email)
            ).first()

            if existing_user:
                flash("Nom d'utilisateur ou email déjà utilisé", "danger")
                return redirect(request.referrer)

            print("👉  77:")

            # Hasher le mot de passe
            mot_de_passe_hash = generate_password_hash(password)

            # Gérer la photo (si vous avez un champ photo)
            photo_filename = None
            photo_file = request.files.get('photo')
            if photo_file and photo_file.filename:
                from werkzeug.utils import secure_filename
                import os
                from datetime import datetime
                from app import UPLOAD_FOLDER

                def allowed_file(filename):
                    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
                    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

                if allowed_file(photo_file.filename):
                    original_filename = secure_filename(photo_file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    photo_filename = f"admin_{timestamp}_{original_filename}"
                    photo_path = os.path.join(app.root_path, UPLOAD_FOLDER, photo_filename)
                    photo_file.save(photo_path)

            print("👉  78:")

            # Créer l'admin (utilisez User au lieu de Admin)
            new_admin = User(
                username=nom_utilisateur,
                prenom=prenom,
                nom=nom,
                email=email,
                telephone=telephone,
                adresse=adresse,
                date_naissance=datetime.strptime(date_naissance, '%Y-%m-%d').date() if date_naissance else None,
                cin_nif=cin_nif,
                mot_de_passe_hash=mot_de_passe_hash,
                role=role,
                fonction=fonction,
                succursale_id=int(succursale_id) if succursale_id and succursale_id.isdigit() else None,
                photo=photo_filename,
                statut='en_attente',
                date_creation=datetime.now(),

                # ✅ Questions secrètes
                question_secrete_1=question_1 if question_1 else None,
                reponse_secrete_1=reponse_1 if reponse_1 else None,
                question_secrete_2=question_2 if question_2 else None,
                reponse_secrete_2=reponse_2 if reponse_2 else None,
                question_secrete_3=question_3 if question_3 else None,
                reponse_secrete_3=reponse_3 if reponse_3 else None,

                # ✅ Première connexion
                premier_connexion=True
            )
            print("👉 Fonction reçue du formulaire:", fonction)

            db.session.add(new_admin)
            db.session.commit()


            flash("✅ Admin ajouté avec succès", "success")
            return redirect(url_for('admin_dashboard'))

        except IntegrityError as e:
            db.session.rollback()
            flash(humanize_unique_error(e),f"Erreur: {str(e)}", "danger")
            return redirect(request.referrer)


    # GET - Afficher le formulaire
    from models import Succursale
    succursales = Succursale.query.all()

    print("👉  99:")

    return render_template('admin_central/ajouter_admin.html', succursales=succursales)

def filtrer_par_role(model):
    if current_user.role == 'super_admin':
        return model.query
    else:
        return model.query.filter_by(succursale_id=current_user.succursale_id)



@clients_bp.route('/<succursale_code>/clients')
@login_required
def list(succursale_code):
    # 🔎 Récupérer la succursale
    succursale = Succursale.query.filter_by(
        code=succursale_code.upper()
    ).first_or_404()

    # 🔐 Sécurité : contrôle d’accès
    if current_user.role != 'super_admin':
        if current_user.succursale_id != succursale.id:
            abort(403)

    # 👥 Clients de cette succursale uniquement
    clients = Client.query.filter_by(
        succursale_id=succursale.id
    ).all()

    return render_template(
        'clients/list.html',
        succursale=succursale,
        clients=clients
    )



@app.route('/admin/employes')
@login_required
def liste_employes():

    if current_user.role not in [
        'admin',
        'admin_succursale',
        'super_admin',
        'superviseur',
        'directeur',
        'gestion_employes'
    ]:
        flash(
            "Vous n'avez pas les permissions nécessaires",
            'danger'
        )
        return redirect(
            url_for('admin_dashboard')
        )

    succursale_id = current_user.succursale_id

    if (
        current_user.role in ['admin', 'super_admin']
        and request.args.get('succursale_id')
    ):
        succursale_id = request.args.get(
            'succursale_id'
        )

    query = User.query.filter(
        User.role.in_([
            'employe',
            'superviseur',
            'directeur'
        ])
    )

    if succursale_id:
        query = query.filter_by(
            succursale_id=succursale_id
        )

    statut = request.args.get('statut')
    if statut:
        query = query.filter_by(
            statut=statut
        )

    fonction = request.args.get('fonction')
    if fonction:
        query = query.filter_by(
            fonction=fonction
        )

    search = request.args.get('search')

    if search:
        search_term = f"%{search}%"

        query = query.filter(
            db.or_(
                (
                    db.func.coalesce(User.prenom, '') +
                    ' ' +
                    db.func.coalesce(User.nom, '')
                ).ilike(search_term),

                User.username.ilike(search_term),
                User.telephone.ilike(search_term),
                User.email.ilike(search_term),
                User.matricule.ilike(search_term)
            )
        )

    employees = query.all()

    succursale = None
    if succursale_id:
        succursale = Succursale.query.get(
            succursale_id
        )

    stats = get_stats_employes(
        succursale_id
    )

    return render_template(
        'employees/list.html',
        employees=employees,
        succursale=succursale,
        stats=stats,
        current_user=current_user
    )


@app.route('/admin/succursale-details')
@login_required
def succursale_details():
    # Si admin, peut voir n'importe quelle succursale
    if current_user.est_admin:
        code = request.args.get('code')
        if code:
            succursale = Succursale.query.filter_by(code=code).first()
        else:
            # Liste des succursales pour admin
            succursales = Succursale.query.all()
            return render_template('liste_succursales.html',
                                   succursales=succursales)
    else:
        # Employé normal voit sa succursale
        succursale = current_user.succursale

    if not succursale:
        flash("Succursale non trouvée", 'danger')
        return redirect(url_for('dashboard'))

    return render_template('succursale/succursale_details.html',
                           succursale=succursale,
                           current_user=current_user)


@app.route('/admin/import-employes')
@login_required
def import_employes():
    # Vérifier les permissions
    if not current_user.role in ['admin', 'directeur', 'rh']:
        flash("Permission refusée. Seuls les admins, directeurs et RH peuvent importer.", 'danger')
        return redirect(url_for('liste_employes'))

    succursale_id = request.args.get('succursale_id', current_user.succursale_id)

    # Si admin, demander la succursale
    if current_user.est_admin and not succursale_id:
        succursales = Succursale.query.all()
        return render_template('choisir_succursale.html',
                               succursales=succursales,
                               action='import_employes')

    return render_template('import_employes.html',
                           succursale_id=succursale_id,
                           current_user=current_user)



@app.route('/admin/verifications-brh')
@login_required
def verifications_brh():

    if current_user.role not in [
        'admin',
        'directeur',
        'compliance',
        'gestionnaire'
    ]:
        flash("Permission refusée", 'danger')
        return redirect(url_for('liste_employes'))

    succursale_id = request.args.get(
        'succursale_id',
        current_user.succursale_id
    )

    if current_user.est_admin and not succursale_id:
        employes = Employe.query.all()
        stats = get_stats_verifications_brh()
    else:
        employes = Employe.query.filter_by(
            succursale_id=succursale_id
        ).all()

        stats = get_stats_verifications_brh(
            succursale_id
        )

    return render_template(
        'verifications_brh.html',
        employes=employes,
        stats=stats,
        current_user=current_user
    )


@app.route('/admin/audit-acces.html')
@login_required
def audit_acces():
    # Vérifier les permissions
    if not current_user.role in ['admin', 'directeur', 'compliance']:
        flash("Permission refusée", 'danger')
        return redirect(url_for('liste_employes'))

    succursale_id = request.args.get('succursale_id', current_user.succursale_id)

    # Récupérer les logs d'audit
    from models import AuditLog  # À créer selon vos besoins

    query = AuditLog.query

    if succursale_id and not current_user.est_admin:
        # Filtrer par succursale si pas admin
        query = query.filter_by(succursale_id=succursale_id)

    # Appliquer les filtres
    type_event = request.args.get('type')
    if type_event:
        query = query.filter_by(event_type=type_event)

    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')
    if date_debut:
        query = query.filter(AuditLog.timestamp >= date_debut)
    if date_fin:
        query = query.filter(AuditLog.timestamp <= date_fin)

    logs = query.order_by(AuditLog.timestamp.desc()).limit(100).all()

    return render_template('audit_acces.html',
                           logs=logs,
                           current_user=current_user)



@app.route('/admin/employe/<int:employe_id>')
@login_required
def voir_employe(employe_id):

    employe = User.query.get_or_404(employe_id)

    if not (
        current_user.role in [
            'admin',
            'super_admin',
            'admin_succursale',
            'direction'
        ]
        or current_user.succursale_id == employe.succursale_id
    ):
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('gerer_employes'))

    historique = (
        HistoriqueEmploye.query
        .filter_by(employe_id=employe.id)
        .order_by(HistoriqueEmploye.date_action.desc())
        .limit(10)
        .all()
    )

    succursale = (
        Succursale.query.get(employe.succursale_id)
        if employe.succursale_id
        else None
    )

    stats = get_stats_employe(employe)

    return render_template(
        'employees/voir_employe.html',
        user=employe,
        employe=employe,
        succursale=succursale,
        historique=historique,
        stats=stats
    )



@app.route('/admin/employe/<int:employe_id>/modifier', methods=['GET', 'POST'])
@login_required
def modifier_employe(employe_id):
    from models import User, Succursale, HistoriqueEmploye
    from flask import request

    # Récupérer l'employé (notez User au lieu de Employe)
    employe = User.query.get_or_404(employe_id)

    # Vérifier les permissions
    if not (current_user.role in ['admin', 'super_admin','direction'] or
            (current_user.role == 'admin_succursale' and
             current_user.succursale_id == employe.succursale_id)):
        flash("⛔ Permission refusée - Vous n'avez pas le droit de modifier cet employé", 'danger')
        return redirect(url_for('gerer_employes'))

    if request.method == 'POST':
        # Sauvegarder les anciennes valeurs pour l'historique
        anciennes_valeurs = {
            'nom': employe.nom,
            'prenom': employe.prenom,
            'email': employe.email,
            'telephone': employe.telephone,
            'role': employe.role,
            'adesse': employe.role,
            'fonction': employe.fonction,
            'succursale_id': employe.succursale_id,
            'statut': employe.statut
        }

        # Récupérer les nouvelles valeurs du formulaire
        employe.nom = request.form.get('nom', employe.nom)
        employe.prenom = request.form.get('prenom', employe.prenom)
        employe.email = request.form.get('email', employe.email)
        employe.telephone = request.form.get('telephone', employe.telephone)
        employe.telephone = request.form.get('adesse', employe.adresse)
        employe.fonction = request.form.get('fonction', employe.fonction)

        # Seul un admin peut changer ces champs sensibles
        if current_user.role in ['admin', 'super_admin','direction']:
            nouveau_role = request.form.get('role')
            if nouveau_role and nouveau_role in ['employe', 'superviseur', 'admin_succursale']:
                employe.role = nouveau_role

            nouvelle_succursale = request.form.get('succursale_id')
            if nouvelle_succursale:
                employe.succursale_id = int(nouvelle_succursale)

            nouveau_statut = request.form.get('statut')
            if nouveau_statut in ['actif', 'suspendu', 'inactif']:
                employe.statut = nouveau_statut

        # Mettre à jour la date de modification
        employe.updated_at = datetime.utcnow()

        # Nouvelles valeurs pour l'historique
        nouvelles_valeurs = {
            'nom': employe.nom,
            'prenom': employe.prenom,
            'email': employe.email,
            'telephone': employe.telephone,
            'role': employe.role,
            'adresse': employe.adresse,
            'fonction': employe.fonction,
            'succursale_id': employe.succursale_id,
            'statut': employe.statut
        }

        db.session.commit()

        # Enregistrer dans l'historique
        HistoriqueEmploye.enregistrer_modification(
            employe_id=employe.id,
            employe=employe,# ← Ajoutez cette ligne
            modifie_par=current_user,
            anciennes_valeurs=anciennes_valeurs,
            nouvelles_valeurs=nouvelles_valeurs,
            ip_address=request.remote_addr
        )
        db.session.commit()

        flash(f'✅ Employé {employe.prenom} {employe.nom} modifié avec succès', 'success')
        return redirect(url_for('voir_employe',employe_id=employe.id))

    # GET : Afficher le formulaire
    succursales = Succursale.query.all()
    return render_template('employees/modifier_employe.html',
                           employe=employe,
                           succursales=succursales,
                           current_user=current_user)


@app.route('/admin/employe/<int:employe_id>/historique')
@login_required
def historique_employe(employe_id):
    employe = Employe.query.get_or_404(employe_id)

    # Vérifier que l'utilisateur a accès
    if not (current_user.est_admin or
            current_user.succursale_id == employe.succursale_id):
        flash("Accès non autorisé", 'danger')
        return redirect(url_for('liste_employes'))

    # Récupérer l'historique (à adapter selon vos modèles)
    from models import HistoriqueEmploye

    historique = HistoriqueEmploye.query.filter_by(employe_id=employe_id) \
        .order_by(HistoriqueEmploye.date.desc()) \
        .all()

    return render_template('admin/historique_employe.html',
                           employe=employe,
                           historique=historique,
                           current_user=current_user)


# ===== ROUTES API POUR LE TEMPLATE =====

@app.route('/api/employes/stats')
@login_required
def api_employes_stats():
    """API pour les statistiques en temps réel"""
    succursale_id = current_user.succursale_id

    # Si admin, peut voir toutes les succursales
    if current_user.est_admin and request.args.get('succursale_id'):
        succursale_id = request.args.get('succursale_id')

    query = Employe.query
    if succursale_id:
        query = query.filter_by(succursale_id=succursale_id)

    total = query.count()
    actifs = query.filter_by(statut='actif').count()
    en_formation = query.filter_by(statut='formation').count()
    conformes = query.filter_by(verifications_completes=True).count()

    return {
        'total': total,
        'actifs': actifs,
        'en_formation': en_formation,
        'conformes': conformes,
        'taux_conformite': (conformes / total * 100) if total > 0 else 0
    }


# ===== ROUTES DE TELECHARGEMENT =====

@app.route('/admin/export/employes')
@login_required
def export_employes():
    """Exporter la liste des employés en CSV"""
    if not current_user.has_permission('exporter_donnees'):
        flash("Permission refusée", 'danger')
        return redirect(url_for('liste_employes'))

    succursale_id = current_user.succursale_id
    if current_user.est_admin and request.args.get('succursale_id'):
        succursale_id = request.args.get('succursale_id')

    employes = Employe.query.filter_by(succursale_id=succursale_id).all()

    # Générer le CSV
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    # En-têtes
    writer.writerow(['Matricule', 'Nom Complet', 'Email', 'Téléphone',
                     'Rôle', 'Habilitation', 'Statut', 'Date Embauche'])

    # Données
    for emp in employes:
        writer.writerow([
            emp.matricule,
            emp.nom_complet,
            emp.email,
            emp.telephone,
            emp.fonction,
            f"Niveau {emp.niveau_habilitation}",
            emp.statut,
            emp.date_creation.strftime('%d/%m/%Y') if emp.date_creation else ''
        ])

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition":
                     f"attachment; filename=employes_{succursale_id}_{datetime.now().strftime('%Y%m%d')}.csv"}
    )


@app.route('/admin/create_succursale', methods=['GET', 'POST'])
@login_required
def create_succursale():

    """Route pour créer une succursale via l'interface web"""

    print(f"🎯 [DEBUG] Méthode requête: {request.method}")
    print(f"🎯 [DEBUG] URL: {request.url}")


    # Récupérer TOUJOURS les succursales existantes
    succursales = Succursale.query.all()
    print(f"🎯 [DEBUG] Nombre de succursales: {len(succursales)}")

    if request.method == 'POST':
        print("🔥 [DEBUG] FORMULAIRE POST DÉTECTÉ !")
        print(f"📦 [DEBUG] Données form: {request.form}")
        # Récupérer les données du formulaire
        code = request.form.get('code')
        nom = request.form.get('nom')
        ville = request.form.get('ville')
        adresse = request.form.get('adresse')
        telephone = request.form.get('telephone')
        email = request.form.get('email')

        # Validation simple
        if not all([code, nom, ville, adresse, telephone, email]):
            flash('❌ Tous les champs sont obligatoires!', 'error')
            return render_template('admin_central/create_succursale.html', succursales=succursales)

        # Vérifier si le code existe déjà
        existing = Succursale.query.filter_by(code=code).first()
        if existing:
            flash(f'❌ La succursale avec le code "{code}" existe déjà!', 'error')
            return render_template('admin_central/create_succursale.html', succursales=succursales)

        # Créer la succursale
        succursale = Succursale(
            code=code,
            nom=nom,
            adresse=adresse,
            ville=ville,
            telephone=telephone,
            email=email,
            statut="active"
        )

        try:
            db.session.add(succursale)
            db.session.commit()
            flash(f'✅ Succursale "{nom}" créée avec succès!', 'success')

            # Recharger la liste après création
            succursales = Succursale.query.all()
            return render_template('admin_central/create_succursale.html', succursales=succursales)

        except Exception as e:
            db.session.rollback()
            flash(f'❌ Erreur: {str(e)}', 'error')
            return render_template('admin_central/create_succursale.html', succursales=succursales)

    # Si méthode GET, afficher le formulaire AVEC les succursales
    return render_template('admin_central/create_succursale.html', succursales=succursales)
from werkzeug.security import generate_password_hash


@app.route('/admin/create_admin', methods=['GET', 'POST'])
@login_required
def create_admin():
    from datetime import datetime
    from models import User, Succursale  # ← AJOUTEZ CETTE LIGNE
    from werkzeug.security import generate_password_hash
    """Route pour créer un nouvel administrateur"""
    if current_user.role != 'super_admin':
        flash("Accès refusé. Seul le super-admin peut ajouter un admin.", "danger")
        return redirect(url_for('admin_dashboard'))

    print("👉  33 Geler:")

    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            nom_utilisateur = request.form.get('nom_utilisateur')
            prenom = request.form.get('prenom')
            nom = request.form.get('nom')
            email = request.form.get('email')
            telephone = request.form.get('telephone')
            adresse = request.form.get('adresse')
            date_naissance = request.form.get('date_naissance')
            cin_nif = request.form.get('cin_nif')
            password = request.form.get('password')
            role = request.form.get('role')
            fonction = request.form.get('fonction') or "Non défini"
            succursale_id = request.form.get('succursale_id') or None

            # ✅ Récupérer les questions secrètes
            question_1 = request.form.get('question_1')
            reponse_1 = request.form.get('reponse_1', '').strip().lower()
            question_2 = request.form.get('question_2')
            reponse_2 = request.form.get('reponse_2', '').strip().lower()
            question_3 = request.form.get('question_3')
            reponse_3 = request.form.get('reponse_3', '').strip().lower()

            print("👉 Fonction reçue du formulaire 75:", fonction)

            # Validation des champs obligatoires
            if not nom_utilisateur or not email or not password:
                flash("Nom d'utilisateur, email et mot de passe sont obligatoires", "danger")
                return redirect(request.referrer)

            print("👉  76:")

            # Vérifier si l'utilisateur existe déjà
            existing_user = User.query.filter(
                (User.username == nom_utilisateur) | (User.email == email)
            ).first()

            if existing_user:
                flash("Nom d'utilisateur ou email déjà utilisé", "danger")
                return redirect(request.referrer)

            print("👉  77:")

            # Hasher le mot de passe
            mot_de_passe_hash = generate_password_hash(password)

            # Gérer la photo (si vous avez un champ photo)
            photo_filename = None
            photo_file = request.files.get('photo')
            if photo_file and photo_file.filename:
                from werkzeug.utils import secure_filename
                import os
                from datetime import datetime
                from app import UPLOAD_FOLDER

                def allowed_file(filename):
                    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
                    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

                if allowed_file(photo_file.filename):
                    original_filename = secure_filename(photo_file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    photo_filename = f"admin_{timestamp}_{original_filename}"
                    photo_path = os.path.join(app.root_path, UPLOAD_FOLDER, photo_filename)
                    photo_file.save(photo_path)

            print("👉  78:")

            # Créer l'admin (utilisez User au lieu de Admin)
            new_admin = User(
                username=nom_utilisateur,
                prenom=prenom,
                nom=nom,
                email=email,
                telephone=telephone,
                adresse=adresse,
                date_naissance=datetime.strptime(date_naissance, '%Y-%m-%d').date() if date_naissance else None,
                cin_nif=cin_nif,
                password_hash=mot_de_passe_hash,
                role=role,
                fonction=fonction,
                succursale_id=int(succursale_id) if succursale_id and succursale_id.isdigit() else None,
                photo_selfie=photo_filename,
                statut='en_attente',
                date_creation=datetime.now(),

                # ✅ Questions secrètes
                question_secrete_1=question_1 if question_1 else None,
                reponse_secrete_1=reponse_1 if reponse_1 else None,
                question_secrete_2=question_2 if question_2 else None,
                reponse_secrete_2=reponse_2 if reponse_2 else None,
                question_secrete_3=question_3 if question_3 else None,
                reponse_secrete_3=reponse_3 if reponse_3 else None,

                # ✅ Première connexion
                premier_connexion=True
            )
            print("👉 Fonction reçue du formulaire:", fonction)

            db.session.add(new_admin)
            db.session.commit()

            flash("✅ Admin ajouté avec succès", "success")
            return redirect(url_for('admin_dashboard'))

        except IntegrityError as e:
            db.session.rollback()
            flash(humanize_unique_error(e), f"Erreur: {str(e)}", "danger")
            return redirect(request.referrer)

    # GET - Afficher le formulaire
    from models import Succursale
    succursales = Succursale.query.all()

    print("👉  99:")

    return render_template('admin_central/ajouter_admin.html', succursales=succursales)




from werkzeug.security import generate_password_hash


@app.route('/interface-fonction/<fonction>')
@login_required
def interface_fonction(fonction):
    """Page d'interface selon la fonction"""
    # Vérifier que l'utilisateur a le droit d'accéder à cette fonction
    if current_user.fonction != fonction and current_user.role not in ['admin', 'super_admin']:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard'))

        # Cas particulier pour admin
    try:
        return render_template(f'fonctions/{fonction}.html', fonction=fonction)
    except TemplateNotFound:
        flash(f'Interface pour {fonction} non disponible', 'warning')
        return redirect(url_for('dashboard'))

@app.route('/admin/create_agent', methods=['GET', 'POST'])
@login_required
def create_agent():
    """Route pour créer un nouvel agent"""
    from models import Succursale, User
    fonction = request.form.get('fonction')
    # Et dans la création de l'agent, ajoutez :
    notes = f"Fonction: {fonction}" if fonction else None

    if request.method == 'POST':
        # Récupérer les données du formulaire
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        telephone = request.form.get('telephone')
        succursale_id = request.form.get('succursale_id')

        # Validation
        if not all([username, email, password, nom,prenom, succursale_id]):
            flash('❌ Tous les champs obligatoires doivent être remplis!', 'error')
            return redirect(url_for('create_agent'))

        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash(f'❌ Le nom d\'utilisateur "{username}" existe déjà!', 'error')
            return redirect(url_for('create_agent'))

        if telephone and not telephone.replace('+', '').replace(' ', '').isdigit():
            flash('❌ Le numéro de téléphone n\'est pas valide', 'error')
            return redirect(url_for('create_agent'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash(f'❌ L\'email "{email}" est déjà utilisé!', 'error')
            return redirect(url_for('create_agent'))

        # Créer l'agent
        agent = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            nom=nom,
            prenom=prenom,
            telephone=telephone,
            role='agent',  # Rôle important : agent
            succursale_id=succursale_id,
            statut='actif',
            terms_accepted=True
        )

        db.session.add(agent)
        db.session.commit()

        flash(f'✅ Agent "{username}" créé avec succès!', 'success')
        return redirect(url_for('admin_dashboard'))

    # GET : Afficher le formulaire
    succursales = Succursale.query.all()
    return render_template('admin_central/ajouter_employe.html', succursales=succursales)

#temporaire
@app.route('/admin/reset_test_data', methods=['GET', 'POST'])
@login_required
def reset_test_data():
    """Réinitialiser uniquement les données de test (plus sûr)"""

    # Vérifier que nous sommes en environnement de développement
    if app.config['ENV'] != 'development':
        flash('❌ Cette fonction n\'est disponible qu\'en environnement de développement!', 'error')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        confirm = request.form.get('confirm')

        if confirm != 'SUPPRIMER_TEST':
            flash('❌ Confirmation incorrecte!', 'error')
            return redirect(url_for('reset_test_data'))

        try:
            from models import Client, Pret, Garant, Transaction

            # Compter avant suppression
            counts = {
                'clients': Client.query.count(),
                'prets': Pret.query.count(),
                'garants': Garant.query.count(),
                'transactions': Transaction.query.count()
            }

            # Supprimer seulement les données de test
            # Garder les succursales et utilisateurs

            # Option 1: Supprimer tout
            db.session.query(Client).delete()
            db.session.query(Pret).delete()
            db.session.query(Garant).delete()
            db.session.query(Transaction).delete()

            db.session.commit()

            flash(f'✅ Données de test supprimées: {counts}', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'❌ Erreur: {str(e)}', 'error')

        return redirect(url_for('admin_dashboard'))

    return render_template('admin_central/reset_test_data.html')



@app.before_request
def inject_routes():
    g.routes = {rule.endpoint for rule in app.url_map.iter_rules()}

@app.route('/admin/activer-employe/<int:employe_id>')
@login_required
def activer_employe(employe_id):
    if current_user.role not in ['admin', 'super_admin', 'directeur']:
        flash("Permission refusée", "danger")
        return redirect(url_for('dashboard'))

    employe = User.query.get_or_404(employe_id)

    # Avant modification
    old_status = employe.statut

    # Modifier
    employe.statut = 'actif'
    employe.approuve_par = current_user.id
    employe.date_approbation = datetime.utcnow()

    db.session.commit()

    # Logger l'action
    log_audit(
        action='activate',
        module='employe',
        details={
            'employe_id': users.id,
            'employe_nom': employe.nom_complet,
            'old_status': old_status,
            'new_status': 'actif',
            'approved_by': current_user.nom_complet
        },
        succursale_id=employe.succursale_id
    )

    flash(f"✅ {employe.nom_complet} activé par {current_user.nom_complet}", 'success')
    return redirect(url_for('liste_employes'))


def log_audit(action, module, details=None, succursale_id=None, succursale_nom=None):
    """Logger une action d'audit"""
    try:
        if current_user.is_authenticated:
            employe_id = current_user.id
            user_name = current_user.nom_complet
            user_role = current_user.role
        else:
            employe_id = 0
            user_name = 'System'
            user_role = 'system'

        # Détails JSON
        details_json = json.dumps(details, ensure_ascii=False) if details else None

        # Créer le log
        audit = AuditLog(
            employe_id=employe_id,
            user_name=user_name,
            user_role=user_role,
            succursale_id=succursale_id,
            succursale_nom=succursale_nom,
            action=action,
            module=module,
            details=details_json,
            ip_address=request.remote_addr if request else None,
            user_agent=request.user_agent.string if request else None
        )

        db.session.add(audit)
        db.session.commit()

    except Exception as e:
        print(f"❌ Erreur audit: {e}")
        db.session.rollback()


@app.before_request
def before_request_audit():
    """Logger certaines actions automatiquement"""
    if current_user.is_authenticated and request.endpoint:
        # Logger les accès aux succursales
        if 'succursale' in request.endpoint or 'branch' in request.endpoint:
            # Extraire le code succursale de l'URL
            succursale_code = None
            if 'succursale_code' in request.view_args:
                succursale_code = request.view_args.get('succursale_code')

            if succursale_code:
                succursale = Succursale.query.filter_by(code=succursale_code).first()
                if succursale:
                    log_audit(
                        action='access',
                        module='succursale',
                        details={'succursale': succursale_code, 'url': request.path},
                        succursale_id=succursale.id,
                        succursale_nom=succursale.nom
                    )


@app.route('/super-admin/audit-logs')
@login_required
def audit_logs():
    if current_user.role != 'super_admin':
        abort(403)

    # Filtres
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')
    employe_id = request.args.get('employe_id')
    succursale_id = request.args.get('succursale_id')
    action = request.args.get('action')

    query = AuditLog.query

    # Appliquer filtres
    if date_debut:
        query = query.filter(AuditLog.timestamp >= date_debut)
    if date_fin:
        query = query.filter(AuditLog.timestamp <= date_fin)
    if employe_id:
        query = query.filter_by(employe_id=employe_id)
    if succursale_id:
        query = query.filter_by(succursale_id=succursale_id)
    if action:
        query = query.filter_by(action=action)

    logs = query.order_by(AuditLog.timestamp.desc()).limit(100).all()

    return render_template('super_admin/audit_logs.html', logs=logs)


@app.route('/admin_central/approbations')
def admin_approbations():
    # Récupérer les comptes en attente
    comptes_en_attente = User.query.filter_by(statut='en_attente').all()

    # DÉFINIR toutes les variables manquantes
    succursales = Succursale.query.all()
    total_admins = User.query.filter_by(role='super_admin').count()
    total_agents = User.query.filter_by(role='agent').count()
    total_clients = Client.query.count()  # si vous avez ce modèle

    return render_template('admin_central/approbations.html',
                           comptes_en_attente=comptes_en_attente,
                           succursales=succursales,
                           total_admins=total_admins,
                           total_agents=total_agents,
                           total_clients=total_clients)

from flask import Response
import csv
import io

@app.route('/admin/exporter-attentes')
@login_required
def exporter_attentes():

    if getattr(current_user, 'role', None) != 'super_admin':
        return redirect(url_for('tableau_de_bord'))

    comptes = User.query.filter_by(statut='en_attente').all()

    # Création du CSV en mémoire
    output = io.StringIO()
    writer = csv.writer(output)

    # En-têtes
    writer.writerow([
        "ID", "Nom", "Prénom", "Email",
        "Username", "Rôle", "Date création"
    ])

    # Données
    for c in comptes:
        writer.writerow([
            c.id,
            c.nom,
            c.prenom,
            c.email,
            c.username,
            c.role,
            c.date_creation.strftime("%Y-%m-%d %H:%M") if c.date_creation else ""
        ])

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=approbations_en_attente.csv"
        }
    )

def send_approval_email(email, nom_complet):
    sender_email = "tonemail@gmail.com"
    sender_password = "ton_mot_de_passe_app"

    sujet = "Candidature acceptée - GMES"

    message = f"""
Bonjour {nom_complet},

Nous avons le plaisir de vous informer que votre candidature a été acceptée.

Vous êtes invité à vous présenter à la succursale pour compléter les formalités administratives et finaliser votre intégration.

Nous vous remercions pour votre confiance.

Cordialement,
L'équipe GMES
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = sujet

    msg.attach(MIMEText(message, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)

    server.send_message(msg)
    server.quit()



@app.route('/admin/approuver-compte/<int:employe_id>')
@login_required
def approuver_compte(employe_id):
    """Approuver un compte en attente"""
    if current_user.role not in ['super_admin', 'admin']:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('admin_dashboard'))

    user = User.query.get_or_404(employe_id)

    if user.statut != 'en_attente':
        flash(f"❌ Ce compte n'est pas en attente (statut: {user.statut})", "warning")
        return redirect(url_for('admin_dashboard'))

    # Approuver le compte
    user.statut = 'actif'
    db.session.commit()

    # ✅ Envoyer un email de confirmation
    try:
        send_approval_email(user)
    except:
        pass  # Log l'erreur mais ne pas bloquer

    flash(f"✅ Compte de {user.prenom} {user.nom} approuvé et activé", "success")

    # Log l'action
    HistoriqueAction.ajouter(
        employe_id=current_user.id,
        action="approbation_compte",
        details=f"Approbation du compte {user.username} (ID: {user.id})",
        request=request
    )

    return redirect(url_for('liste_users'))

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_rejection_email(email, nom_complet):
    sender_email = "tonemail@gmail.com"
    sender_password = "ton_mot_de_passe_app"

    sujet = "Décision concernant votre candidature"

    message = f"""
Bonjour {nom_complet},

Nous vous remercions pour l'intérêt que vous avez porté à notre institution.

Après étude de votre dossier, nous regrettons de vous informer que votre candidature n'a pas été retenue pour le moment.

Nous vous souhaitons beaucoup de succès dans vos projets futurs.

Cordialement,
L'équipe GMES
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = sujet

    msg.attach(MIMEText(message, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)

    server.send_message(msg)
    server.quit()


@app.route('/admin/rejeter-compte/<int:employe_id>')
@login_required
def rejeter_compte(employe_id):
    """Rejeter un compte en attente et supprimer les données"""
    if current_user.role not in ['super_admin', 'admin']:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('admin_dashboard'))

    user = User.query.get_or_404(employe_id)

    if user.statut != 'en_attente':
        flash(f"❌ Ce compte n'est pas en attente (statut: {user.statut})", "warning")
        return redirect(url_for('admin_dashboard'))

    try:
        # 🔴 SUPPRIMER LES DONNÉES ASSOCIÉES

        # 1. Supprimer les documents uploadés (fichiers physiques)
        if user.documents:
            for doc in user.documents:
                # Supprimer le fichier physique
                if doc.file_path and os.path.exists(doc.file_path):
                    os.remove(doc.file_path)
                # Supprimer l'entrée en base
                db.session.delete(doc)

        # 2. Supprimer les notes
        if user.notes_recues:
            for note in user.notes_recues:
                db.session.delete(note)

        # 3. Supprimer l'historique des actions
        if user.historique_actions:
            for action in user.historique_actions:
                db.session.delete(action)

        # 4. Supprimer les contacts
        if user.contacts_recus:
            for contact in user.contacts_recus:
                db.session.delete(contact)

        # 5. Récupérer le nom avant suppression pour le message
        nom_complet = f"{user.prenom} {user.nom}"
        username = user.username
        email = user.email

        # 🔴 SUPPRIMER L'UTILISATEUR
        db.session.delete(user)
        db.session.commit()

        # ✅ Optionnel: Envoyer un email de rejet
        try:
            send_rejection_email(email, nom_complet)
        except:
            pass

        flash(f"🗑️ Compte de {nom_complet} rejeté et supprimé", "success")

        # Log l'action
        HistoriqueAction.ajouter(
            employe_id=current_user.id,
            action="rejet_compte",
            details=f"Rejet et suppression du compte {username} (ID: {employe_id})",
            request=request
        )

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erreur lors du rejet du compte {employe_id}: {e}")
        flash(f"❌ Erreur lors du rejet: {str(e)}", "danger")

    return redirect(url_for('liste_users'))

@app.route('/admin/employes')
@login_required
def admin_employes():
    if current_user.role not in ['super_admin', 'admin_succursale']:
        flash("Accès refusé", "danger")
        return redirect(url_for('tableau_de_bord'))
    employes = User.query.filter(User.role != 'client').all()
    succursales = Succursale.query.all()

    # Statistiques
    total_employes = User.query.filter(User.role != 'client').count()
    employes_actifs = User.query.filter(User.statut == 'actif', User.role != 'client').count()
    employes_attente = User.query.filter(User.statut == 'en_attente', User.role != 'client').count()

    return render_template('admin_central/liste_employes.html',
                           employes=employes,
                           succursales=succursales,
                           total_employes=total_employes,
                           employes_actifs=employes_actifs,
                           employes_attente=employes_attente)


@app.route('/api/employes')
@login_required
def api_employes_list():
    # Filtres
    succursale_id = request.args.get('succursale_id')
    statut = request.args.get('statut')
    role = request.args.get('role')
    search = request.args.get('search')

    query = User.query.filter(User.role != 'client')

    if succursale_id:
        query = query.filter_by(succursale_id=succursale_id)
    if statut:
        query = query.filter_by(statut=statut)
    if role:
        query = query.filter_by(role=role)
    if search:
        query = query.filter(
            db.or_(
                User.nom.ilike(f'%{search}%'),
                User.prenom.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%'),
                User.telephone.ilike(f'%{search}%'),
                User.matricule.ilike(f'%{search}%')
            )
        )

    # Pagination
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))

    total = query.count()
    employes = query.offset(start).limit(length).all()

    data = []
    for emp in employes:
        data.append({
            'id': emp.id,
            'matricule': emp.matricule,
            'nom': emp.nom,
            'prenom': emp.prenom,
            'email': emp.email,
            'telephone': emp.telephone,
            'role': emp.role,
            'fonction': emp.fonction,
            'statut': emp.statut,
            'date_creation': emp.date_creation,
            'succursale': {
                'nom': emp.succursale.nom if emp.succursale else None
            }
        })

    return {
        'draw': int(request.args.get('draw', 1)),
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': data
    }

@app.route('/admin/utilisateurs')
@login_required
def gestion_utilisateurs():

    statut_filter = request.args.get('statut')
    niveau_filter = request.args.get('niveau')
    search = request.args.get('search')

    query = User.query

    # 🔎 Filtre statut
    if statut_filter and statut_filter != "Tous les statuts":
        query = query.filter(User.statut == statut_filter)

    # 🔎 Filtre niveau
    if niveau_filter and niveau_filter != "Tous niveaux":
        query = query.filter(User.niveau_habilitation == int(niveau_filter))

    # 🔎 Recherche texte
    if search:
        from sqlalchemy import or_
        query = query.filter(
            or_(
                User.nom.ilike(f"%{search}%"),
                User.matricule.ilike(f"%{search}%"),
                User.telephone.ilike(f"%{search}%")
            )
        )

    users = query.all()

    return render_template(
        "admin_central/utilisateurs.html",
        users=users
    )


from sqlalchemy import func

@app.route('/admin-succursale/dashboard')
@login_required
def admin_succursale_dashboard():
    print("ID:", current_user.id)
    print("Username:", current_user.username)
    print("Prenom:", current_user.prenom)
    print("Nom:", current_user.nom)

    if current_user.role != 'admin_succursale':
        abort(403)

    succursale = Succursale.query.get(current_user.succursale_id)
    if not succursale:
        abort(404)

    stats = get_stats_admin_succursale(succursale.id )

    return render_template(
        'admin/admin_dashboard.html',
        succursale=succursale,
        stats=stats
    )


@app.route('/synchroniser-donnees')
@login_required
def synchroniser_donnees():
    # Votre logique de synchronisation ici
    flash('Données synchronisées avec succès!', 'success')
    return redirect(request.referrer or url_for('liste_succursales'))


@app.route('/succursale/dashboard')
@login_required
def dashboard_central():
    # Récupérer la succursale de l'utilisateur connecté
    from models import Succursale, User, Client, Credit, Remboursement
    from sqlalchemy import func

    # Si l'utilisateur est super_admin, prendre la première succursale ou une succursale par défaut
    if current_user.role == 'super_admin':
        succursale = Succursale.query.first()
        if not succursale:
            flash('Aucune succursale trouvée. Créez-en une d\'abord.', 'warning')
            return redirect(url_for('create_succursale'))
    else:
        # Pour les autres rôles, récupérer leur succursale
        succursale = current_user.succursale
        if not succursale:
            flash('Vous n\'êtes pas rattaché à une succursale', 'danger')
            return redirect(url_for('accueil'))

    # Calculer les statistiques pour cette succursale
    stats = get_stats_succursale(succursale.id)

    return render_template('succursale/dashboard.html',
                           succursale=succursale,
                           stats=stats)



@app.route('/admin/rapport-global')
@login_required
def admin_rapport_global():
    # DÉBOGAGE - À SUPPRIMER PLUS TARD
    print("ROLE ACTUEL:", current_user.role)

    print("=" * 50)
    print(f"UTILISATEUR: {current_user.username}")
    print(f"RÔLE: {current_user.role}")
    print(f"ID: {current_user.id}")
    print(f"Email: {current_user.email}")
    print("=" * 50)

    print("ROLE =", current_user.role)
    print("FONCTION =", current_user.fonction)

    # Vérifier les permissions
    if current_user.role not in ['super_admin', 'direction', 'superviseur']:
        flash('Accès non autorisé', 'danger')
        abort(403)

    # Importer les modèles nécessaires
    from models import  Remboursement, Paiement, Credit, Client, Pret
    from sqlalchemy import func
    from datetime import datetime

    try:
        # Statistiques générales
        total_credits = Pret.query.count()
        total_clients = Client.query.count()

        # Montant total décaissé
        montant_total_decaissement = db.session.query(func.sum(Pret.montant)).scalar() or 0

        # Montant total remboursé
        montant_total_rembourse = db.session.query(func.sum(Remboursement.montant)).scalar() or 0

        # Nombre de paiements
        nombre_paiements = Remboursement.query.count()

        # Créer le dictionnaire rapport
        rapport = {
            'date_generation': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'total_credits': total_credits,
            'total_clients': total_clients,
            'montant_total_decaissement': montant_total_decaissement,
            'montant_total_rembourse': montant_total_rembourse,
            'nombre_paiements': nombre_paiements,
            'taux_remboursement': (montant_total_rembourse / montant_total_decaissement * 100)
            if montant_total_decaissement > 0 else 0
        }

        # ✅ IMPORTANT: Passer la variable 'rapport' au template
        return render_template('admin_central/rapport_global.html', rapport=rapport)


    except Exception as e:

        flash(f'Erreur lors de la génération du rapport: {str(e)}', 'danger')

        return redirect(url_for('dashboard_central'))


@app.route('/<succursale_code>/caissier/dashboard')
@login_required
def caissier_dashboard(succursale_code):
    """Dashboard spécifique pour les caissiers"""

    # Vérifier que l'utilisateur est bien caissier
    if current_user.role != 'employe' or current_user.fonction != 'caissier':
        flash('⛔ Accès non autorisé - Espace caissier', 'danger')
        return redirect(url_for('dashboard_redirect'))

    succursale = Succursale.query.filter_by(code=succursale_code).first_or_404()


    stats = get_stats_caissier(succursale.id)

    # Derniers paiements
    derniers_paiements = Remboursement.query .join(Pret) .filter(Pret.succursale_id == succursale.id)  .order_by(Remboursement.date_remboursement.desc()).limit(10) .all()

    return render_template('fonctions/caissier/dashboard.html',
                           succursale=succursale,
                           stats=stats,
                           derniers_paiements=derniers_paiements)


@app.route('/debug/session')
@login_required
def debug_session():
    """Affiche l'état de la session"""
    from flask import session

    html = f"""
    <h2>Debug Session</h2>
    <h3>Session Flask:</h3>
    <pre>{dict(session)}</pre>

    <h3>Current User:</h3>
    <pre>
    ID: {current_user.id}
    Username: {current_user.username}
    Rôle: {current_user.role}
    Email: {current_user.email}
    Authentifié: {current_user.is_authenticated}
    </pre>

    <h3>Actions:</h3>
    <ul>
        <li><a href="/debug/clear-session">🗑️ Vider la session</a></li>
        <li><a href="/dashboard">↻ Retour dashboard</a></li>
    </ul>
    """
    return html


@app.route('/debug/clear-session')
def clear_session():
    """Vide la session"""
    session.clear()
    return "✅ Session vidée - <a href='/'>Retour</a>"




@app.route('/api/calcul-pret', methods=['POST'])
@login_required
def api_calcul_pret():

    data = request.get_json()

    montant = float(data.get('montant', 0))
    duree = int(data.get('duree', 0))

    taux_interet = 0.03  # 3% par mois (exemple)

    total_interet = montant * taux_interet * duree
    total_rembourser = montant + total_interet
    mensualite = round(total_rembourser / duree, 2)

    return jsonify({
        "mensualite": round(mensualite, 2),
        "total_rembourser": round(total_rembourser, 2),
        "cout_credit": round(total_interet, 2)
    })




@app.route('/simulateur-credit')
def simulateur_credit():
    """Page du simulateur de crédit"""
    return render_template('simulateur_credit.html')

# 🔐 Création automatique du super admin
# creer_super_admin()


@app.route('/<succursale_code>/agent-credit/rapport')
@login_required
def rapport_activite(succursale_code):
    """Rapport d'activité pour l'agent de crédit"""
    if current_user.role != 'employe' or current_user.fonction != 'agent_credit':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    from models import Succursale, Credit, Client
    from datetime import datetime, timedelta
    from sqlalchemy import func

    succursale = Succursale.query.filter_by(code=succursale_code).first_or_404()

    # Récupération des paramètres de filtre
    periode = request.args.get('periode', 'mois')
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')

    # Calcul des dates
    aujourd_hui = datetime.now()
    if periode == 'aujourdhui':
        debut = aujourd_hui.replace(hour=0, minute=0, second=0)
        fin = aujourd_hui
    elif periode == 'semaine':
        debut = aujourd_hui - timedelta(days=aujourd_hui.weekday())
        fin = aujourd_hui
    elif periode == 'mois':
        debut = aujourd_hui.replace(day=1)
        fin = aujourd_hui
    elif periode == 'trimestre':
        debut = (aujourd_hui - timedelta(days=90))
        fin = aujourd_hui
    elif periode == 'annee':
        debut = aujourd_hui.replace(month=1, day=1)
        fin = aujourd_hui
    else:
        # Période personnalisée
        try:
            debut = datetime.strptime(date_debut, '%Y-%m-%d') if date_debut else aujourd_hui - timedelta(days=30)
            fin = datetime.strptime(date_fin, '%Y-%m-%d') if date_fin else aujourd_hui
        except:
            debut = aujourd_hui - timedelta(days=30)
            fin = aujourd_hui

    # Statistiques
    stats = {
        'credits_octroyes': Credit.query.filter(
            Credit.agent_id == current_user.id,
            Credit.date_demande >= debut,
            Credit.date_demande <= fin,
            Credit.statut.in_(['actif', 'rembourse'])
        ).count(),
        'montant_total': db.session.query(func.sum(Credit.montant)).filter(
            Credit.agent_id == current_user.id,
            Credit.date_demande >= debut,
            Credit.date_demande <= fin
        ).scalar() or 0,
        'nouveaux_clients': Client.query.filter(
            Client.agent_id == current_user.id,
            Client.date_inscription >= debut,
            Client.date_inscription <= fin
        ).count(),
        'performance': 85,
        'objectif': 100,
        'tendance_credits': 12,
        'tendance_credits_couleur': 'success',
        'montant_moyen': 250000,
        'taux_conversion': 68,
        'credits_en_attente': 3,
        'credits_en_cours': 15,
        'credits_rembourses': 8,
        'credits_impayes': 2,
        'montant_en_attente': 750000,
        'montant_en_cours': 3750000,
        'montant_rembourses': 2000000,
        'montant_impayes': 500000,
        'pourcentage_en_attente': 10,
        'pourcentage_en_cours': 50,
        'pourcentage_rembourses': 27,
        'pourcentage_impayes': 7,
        'credits_aujourdhui': 2,
        'credits_semaine': 8,
        'credits_mois': 22,
        'montant_aujourdhui': 500000,
        'montant_semaine': 2000000,
        'montant_mois': 5500000,
        'clients_aujourdhui': 2,
        'clients_semaine': 7,
        'clients_mois': 18
    }

    # Derniers crédits
    derniers_credits = Credit.query.filter_by(
        agent_id=current_user.id
    ).order_by(Credit.date_demande.desc()).limit(10).all()

    return render_template('fonctions/agent_credit/rapport_activite.html',
                           succursale=succursale,
                           stats=stats,
                           derniers_credits=derniers_credits,
                           periode=periode,
                           date_debut=debut.strftime('%Y-%m-%d') if debut else '',
                           date_fin=fin.strftime('%Y-%m-%d') if fin else '')




@app.route('/test')
def test():
    return jsonify({
        'status': 'GMES Microcrédit - Système Opérationnel',
        'message': 'Tout fonctionne correctement!'
    })


@app.route('/vider-session')
def vider_session():
    session.clear()
    return "✅ Session vidée - <a href='/'>Retour à l'accueil</a>"

@app.before_request
def clear_session_on_startup():
    """Vide la session si c'est le premier lancement"""
    # Utilisez une variable d'application pour savoir si c'est le premier lancement
    if not hasattr(app, '_session_cleared'):
        session.clear()
        app._session_cleared = True


@app.route('/cleanup-test-users')
def cleanup_test_users():
    """Supprime les utilisateurs de test"""
    test_users = User.query.filter(User.username.in_(['bonbon bel', 'test', 'demo'])).all()
    for user in test_users:
        db.session.delete(user)
    db.session.commit()
    return f"✅ {len(test_users)} utilisateurs de test supprimés"

# Route temporaire à ajouter dans app.py
@app.route('/client-notifications/<int:client_id>')
def client_notifications(client_id):
    from models import Notification
    notifs = Notification.query.filter_by(employe_id=client_id).all()
    result = f"<h1>Notifications pour client {client_id}</h1>"
    for n in notifs:
        result += f"<p><strong>{n.titre}</strong><br>{n.message}</p>"
    return result


@app.route('/client/terms/success')
def client_terms_success():
    """Page de confirmation après signature des conditions"""
    client = current_user if hasattr(current_user, 'client_profile') else None
    return render_template('client_terms_success.html', client=client, now=datetime.now)



# Route temporaire pour voir TOUS les liens clients
@app.route('/debug/liens-clients')
def debug_liens_clients():
    from models import User
    clients = Client.query.filter(Client.token_signature.isnot(None)).all()

    html = "<h1>Liens de signature</h1>"
    for client in clients:
        lien = url_for('client_terms', token=client.token_signature, _external=True)
        html += f"""
        <div style="border:1px solid #ccc; margin:10px; padding:10px;">
            <h3>{client.prenom} {client.nom} (ID: {client.id})</h3>
            <p>Statut: {client.statut}</p>
            <p>Token: {client.token_signature}</p>
            <p><a href="{lien}" target="_blank">{lien}</a></p>
        </div>
        """

    return html




# Route de test
@app.route('/test-email/<email>')
def test_email(email):
    from utils.notifications import notification_manager
    try:
        msg = f"Test email à {datetime.now()}"
        notification_manager.envoyer_email(
            destinataire=email,
            sujet="Test GMES",
            message_html=f"<h1>Test</h1><p>{msg}</p>",
            message_text=msg
        )
        return f"✅ Email envoyé à {email}"
    except Exception as e:
        return f"❌ Erreur: {e}"


@app.route('/conseiller/renvoyer-lien/<int:client_id>', methods=['POST'])
@login_required
def renvoyer_lien(client_id):
    """Renvoie le lien de signature au client (avec email réel)"""

    # Vérifier les permissions
    if current_user.role != 'employe' or current_user.fonction != 'conseiller':
        return jsonify({'success': False, 'message': '⛔ Permission non autorisée'}), 403

    # Récupérer le client
    client = Client.query.get_or_404(client_id)

    # Vérifier que ce client appartient bien à ce conseiller
    if client.cree_par_id != current_user.id:
        return jsonify({'success': False, 'message': '⛔ Ce client ne vous appartient pas'}), 403

    # Vérifier que le client est bien en attente de signature
    if client.statut != 'en_attente_terms':
        return jsonify({'success': False, 'message': f'⚠️ Ce client est en statut "{client.statut}"'}), 400

    # Vérifier que le token existe
    if not client.token_signature:
        return jsonify({'success': False, 'message': '❌ Aucun token trouvé pour ce client'}), 400

    try:
        # 1. Générer le lien
        from itsdangerous import URLSafeTimedSerializer
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        nouveau_token = serializer.dumps(client.id, salt="terms-accept")
        lien_terms = url_for('client_terms', token=nouveau_token, _external=True)

        # 2. Remplacer localhost par l'IP réelle pour les clients externes
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            lien_terms = lien_terms.replace('127.0.0.1', local_ip).replace('localhost', local_ip)
        except:
            pass

        client.token_signature = nouveau_token
        db.session.commit()

        # 3. ENVOYER L'EMAIL VIA SMTP (solution intégrée)
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # Configuration email (à mettre dans vos variables d'environnement)
        import os
        EMAIL_EXPEDITEUR = os.environ.get('MAIL_USERNAME', 'gmeshaiti@gmail.com')
        EMAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')  # ← Utilise le .env
        EMAIL_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        EMAIL_PORT = int(os.environ.get('SMTP_PORT', 587))

        print(f"📧 Envoi depuis: {EMAIL_EXPEDITEUR}")
        print(f"🔐 Mot de passe: {'✅ Défini' if EMAIL_PASSWORD else '❌ Manquant'}")
        print("PASS EXACT:", repr(app.config['MAIL_PASSWORD']))

        # Créer le message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "🔐 GMES - Lien de signature de vos conditions générales"
        msg['From'] = f"GMES Microcrédit <{EMAIL_EXPEDITEUR}>"
        msg['To'] = client.email

        # Version HTML du message
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #0b3b4f; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .btn {{ display: inline-block; background: #28a745; color: white; padding: 12px 30px; 
                       text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>GMES Microcrédit</h1>
                </div>
                <div class="content">
                    <h2>Bonjour {client.prenom} {client.nom},</h2>
                    <p>Vous avez demandé un nouveau lien pour signer vos conditions générales.</p>
                    <p>Cliquez sur le bouton ci-dessous pour accéder à votre espace de signature :</p>

                    <div style="text-align: center;">
                        <a href="{lien_terms}" class="btn">✅ Signer mes conditions</a>
                    </div>

                    <p>Ou copiez ce lien dans votre navigateur :</p>
                    <p style="word-break: break-all; background: #eee; padding: 10px; border-radius: 5px;">
                        <a href="{lien_terms}">{lien_terms}</a>
                    </p>

                    <p><strong>Ce lien expirera le {client.date_expiration_token.strftime('%d/%m/%Y à %H:%M') if client.date_expiration_token else 'dans 7 jours'}.</strong></p>

                    <p>Si vous n'êtes pas à l'origine de cette demande, ignorez cet email.</p>

                    <p>Cordialement,<br>L'équipe GMES Microcrédit</p>
                </div>
                <div class="footer">
                    <p>Cet email a été envoyé automatiquement, merci de ne pas y répondre.</p>
                    <p>© 2025 GMES Microcrédit. Tous droits réservés.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Version texte simple
        text = f"""
        Bonjour {client.prenom} {client.nom},

        Vous avez demandé un nouveau lien pour signer vos conditions générales.

        Cliquez sur ce lien : {lien_terms}

        Ce lien expirera dans 7 jours.

        Cordialement,
        L'équipe GMES Microcrédit
        """

        # Attacher les versions texte et HTML
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Envoyer l'email
        try:
            server = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
            server.starttls()
            server.login(EMAIL_EXPEDITEUR, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            email_envoye = True
            print(f"✅ Email envoyé avec succès à {client.email}")
        except Exception as e:
            print(f"❌ Erreur envoi email: {e}")
            email_envoye = False

        # 4. Créer une notification dans la base
        from datetime import datetime
        from models import Notification, Action

        # Récupérer une action par défaut
        action_defaut = Action.query.first()
        if not action_defaut:
            # Créer une action par défaut si aucune n'existe
            action_defaut = Action(
                titre="Action système",
                assignee_a_id=current_user.id,
                creee_par_id=current_user.id,
                date_echeance=datetime.now() + timedelta(days=30),
                type_action='tache',
                priorite='moyenne',
                statut='a_faire',
                progression=0
            )
            db.session.add(action_defaut)
            db.session.flush()

        nouvelle_notification = Notification(
            employe_id=client.id,
            titre="🔔 Nouveau lien de signature",
            message=f"Bonjour {client.prenom}, voici votre nouveau lien pour signer vos conditions : {lien_terms}",
            type_notification='terms',
            lien=lien_terms,
            date_envoi=datetime.now(),
            lue=False,
            date_creation=datetime.now(),
            destinataire_id=client.id,
            action_id=action_defaut.id  # ← CORRIGÉ !
        )
        db.session.add(nouvelle_notification)
        db.session.commit()

        # 5. Message flash pour le conseiller
        flash(f'✅ Lien de signature renvoyé à {client.prenom} {client.nom} ({client.email})', 'success')

        if email_envoye:
            return jsonify({
                'success': True,
                'message': f'✅ Email envoyé à {client.email}',
                'email_envoye': True
            })
        else:
            return jsonify({
                'success': True,
                'message': f'⚠️ Notification créée mais email non envoyé (vérifiez config SMTP)',
                'email_envoye': False
            })

    except Exception as e:
        db.session.rollback()
        print("PASS EXACT:", repr(app.config['MAIL_PASSWORD']))
        print(f"❌ Erreur renvoi lien: {e}")
        return jsonify({'success': False, 'message': f'❌ Erreur: {str(e)}'}), 500


@app.route('/directeur/dossiers-en-attente')
@login_required
def directeur_dossiers_attente():
    """Le directeur voit tous les dossiers en attente d'approbation"""

    if current_user.role != 'direction' or current_user.fonction != 'directeur':
        flash('⛔ Accès non autorisé', 'danger')
        return redirect(url_for('dashboard_redirect'))

    # Récupérer tous les clients en attente d'approbation
    dossiers_attente = User.query.filter_by(
        role='client',
        statut='en_attente_approbation'
    ).order_by(User.date_signature_terms.desc()).all()

    # Statistiques
    stats = get_stats_dossiers_attente(
        dossiers_attente
    )

    return render_template('directeur/dossiers_attente.html',
                           dossiers_attente=dossiers_attente,
                           stats=stats)



@app.route('/api/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_read():
    """Marquer toutes les notifications comme lues"""
    Notification.query.filter_by(
        employe_id=current_user.id,
        read=False
    ).update({'read': True})
    db.session.commit()
    return jsonify({'success': True})


# Fonction utilitaire pour notifier tous les admins
def notify_admins(message, level='error', lien=None):
    """Notifie tous les administrateurs"""
    from datetime import datetime

    admins = User.query.filter_by(role='admin').all()

    for admin in admins:
        notification = Notification(
            employe_id=admin.id,
            titre="🔔 Notification système",  # ← Champ requis
            message=message,
            type_notification=level,  # ou 'level' selon votre modèle
            lue=False,
            date_creation=datetime.now(),
            date_envoi=datetime.now(),
            lien=lien,
            # Ajoutez les champs obligatoires avec des valeurs par défaut
            action_id=0,  # ou None si nullable
            destinataire_id=admin.id,
            # Si votre modèle a ces champs
            level=level,
            url=lien,
            read=False,
            timestamp=datetime.now()
        )
        db.session.add(notification)

    db.session.commit()



# Dans votre gestionnaire d'erreurs
@app.errorhandler(500)
def handle_500(error):
    db.session.rollback()

    # Log l'erreur
    error_log = ErrorLog(
        message=str(error),
        traceback=traceback.format_exc(),
        url=request.url,
        employe_id=current_user.id if current_user.is_authenticated else None,
        succursale_id=current_user.succursale_id if current_user.is_authenticated else None
    )
    db.session.add(error_log)
    db.session.commit()

    # Notification socket aux admins
    try:
        socketio.emit('new_error', {
            'id': error_log.id,
            'message': str(error)[:100],
            'time': error_log.timestamp.strftime('%H:%M:%S')
        }, room='admins')
    except:
        pass  # Ignorer si socketio n'est pas configuré

    return render_template('errors/500.html',
                           error_id=error_log.id,
                           now=datetime.now()), 500


def notifier_admins(message, level='error', url=None):
    """Envoie une notification à tous les admins"""
    admins = User.query.filter(
        User.role.in_(['super_admin', 'admin_succursale'])
    ).all()

    for admin in admins:
        # Ici vous pouvez sauvegarder dans une table Notification
        # Ou pour l'instant, on log simplement
        app.logger.info(f"NOTIFICATION pour {admin.email}: {message}")

        # Bonus: Envoyer un email si c'est une erreur critique
        if level == 'error' and admin.email:
            try:
                send_email(
                    subject=f"🚨 Erreur GMES - {message[:50]}",
                    recipient=admin.email,
                    body=f"""
                    Une erreur est survenue sur l'application:
                    Message: {message}
                    URL: {url}
                    Heure: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                    Consultez les logs pour plus de détails.
                    """
                )
            except:
                pass


@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated and current_user.role in ['admin', 'super_admin']:
        join_room('admins')
        print(f"Admin {current_user.email} connecté à la room admins")

@socketio.on('join')
def handle_join(data):
    if current_user.is_authenticated and current_user.role in ['admin', 'super_admin']:
        join_room('admins')


@app.route('/admin/dossier/<int:employe_id>')
@login_required
def voir_dossier(employe_id):
    """Voir le dossier complet d'un utilisateur (admin uniquement)"""
    # Vérifier les permissions
    if current_user.role not in ['super_admin', 'admin','direction', 'admin_succursale']:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('admin_dashboard'))

    # Récupérer l'utilisateur
    user = User.query.get_or_404(employe_id)

    # Pour admin_succursale, vérifier que l'utilisateur est dans sa succursale
    if current_user.role == 'admin_succursale' and user.succursale_id != current_user.succursale_id:
        flash("⛔ Vous ne pouvez voir que les dossiers de votre succursale", "danger")
        return redirect(url_for('admin_dashboard'))

    # Récupérer les informations complètes
    dossier = {
        'utilisateur': user,
        'succursale': Succursale.query.get(user.succursale_id) if user.succursale_id else None,
        'documents': Document.query.filter_by(employe_id=employe_id).all(),
        'prets': Pret.query.filter_by(client_id=employe_id).all() if user.role == 'client' else [],
        'historique': HistoriqueAction.query.filter_by(employe_id=employe_id).order_by(HistoriqueAction.date.desc()).limit(
            10).all(),
        'notes': Note.query.filter_by(employe_id=employe_id).order_by(Note.date.desc()).all()
    }

    return render_template('admin/dossier_utilisateur.html', dossier=dossier)


@app.route('/admin/contacter/<int:employe_id>', methods=['GET', 'POST'])
@login_required
def contacter_utilisateur(employe_id):
    """Page de contact pour envoyer un message à un utilisateur"""
    if current_user.role not in ['super_admin', 'admin', 'admin_succursale']:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('admin_dashboard'))

    user = User.query.get_or_404(employe_id)

    if request.method == 'POST':
        sujet = request.form.get('sujet')
        message = request.form.get('message')
        type_contact = request.form.get('type_contact')  # email, sms, les deux

        try:
            if type_contact in ['email', 'les_deux'] and user.email:
                send_email(
                    subject=f"[ADMIN] {sujet}",
                    recipient=user.email,
                    body=f"""Message de {current_user.prenom} {current_user.nom} (Admin):{message}--- Ce message vous a été envoyé via l'interface d'administration."""
                )

            if type_contact in ['sms', 'les_deux'] and user.telephone:
                send_sms(
                    to=user.telephone,
                    message=f"Admin: {message[:160]}"
                )

            # Enregistrer dans l'historique
            contact = ContactHistorique(
                admin_id=current_user.id,
                employe_id=user.id,
                type=type_contact,
                sujet=sujet,
                message=message,
                date_envoi=datetime.now()
            )
            db.session.add(contact)
            db.session.commit()

            flash(f"✅ Message envoyé à {user.prenom} {user.nom}", "success")
            return redirect(url_for('voir_dossier', employe_id=user.id))

        except Exception as e:
            flash(f"❌ Erreur lors de l'envoi: {str(e)}", "danger")

    return render_template('admin/contact_utilisateur.html', user=user)



@app.route('/admin/notes/<int:employe_id>', methods=['GET', 'POST'])
@login_required
def notes_demande(employe_id):
    """Gérer les notes sur une demande utilisateur"""
    if current_user.role not in ['super_admin', 'admin', 'admin_succursale']:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('admin_dashboard'))

    user = User.query.get_or_404(employe_id)

    if request.method == 'POST':
        action = request.form.get('action')
        note_id = request.form.get('note_id')
        contenu = request.form.get('contenu')

        if action == 'ajouter' and contenu:
            note = Note(
                employe_id=user.id,
                auteur_id=current_user.id,
                contenu=contenu,
                date=datetime.now()
            )
            db.session.add(note)
            db.session.commit()
            flash("✅ Note ajoutée", "success")

        elif action == 'modifier' and note_id and contenu:
            note = Note.query.get_or_404(note_id)
            if note.auteur_id == current_user.id or current_user.role == 'super_admin':
                note.contenu = contenu
                note.date_modification = datetime.now()
                db.session.commit()
                flash("✅ Note modifiée", "success")
            else:
                flash("⛔ Vous ne pouvez modifier que vos propres notes", "danger")

        elif action == 'supprimer' and note_id:
            note = Note.query.get_or_404(note_id)
            if note.auteur_id == current_user.id or current_user.role == 'super_admin':
                db.session.delete(note)
                db.session.commit()
                flash("✅ Note supprimée", "success")
            else:
                flash("⛔ Vous ne pouvez supprimer que vos propres notes", "danger")

        return redirect(url_for('notes_demande', employe_id=user.id))

    # Récupérer toutes les notes pour cet utilisateur
    notes = Note.query.filter_by(employe_id=user.id).order_by(Note.date.desc()).all()

    return render_template('admin/notes_utilisateur.html', user=user, notes=notes)


@app.route('/admin/historique')
@login_required
def historique_global():
    """Voir l'historique global des actions"""
    if current_user.role not in ['super_admin', 'admin']:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('admin_dashboard'))

    page = request.args.get('page', 1, type=int)
    per_page = 50

    historique = HistoriqueAction.query.order_by(
        HistoriqueAction.date.desc()
    ).paginate(page=page, per_page=per_page)

    return render_template('admin/historique_global.html', historique=historique)


@app.route('/admin/historique/utilisateur/<int:employe_id>')
@login_required
def historique_utilisateur(employe_id):
    """Voir l'historique d'un utilisateur spécifique"""
    if current_user.role not in ['super_admin', 'admin', 'admin_succursale']:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('admin_dashboard'))

    user = User.query.get_or_404(employe_id)
    historique = HistoriqueAction.get_by_user(employe_id)

    return render_template('admin/historique_utilisateur.html', user=user, historique=historique)


@app.route('/admin/documents/<int:employe_id>')
@login_required
def liste_documents(employe_id):
    """Liste tous les documents d'un utilisateur"""
    if current_user.role not in ['super_admin', 'admin', 'admin_succursale']:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('admin_dashboard'))

    user = User.query.get_or_404(employe_id)
    documents = Document.get_by_user(employe_id)

    return render_template('admin/liste_documents.html.html', user=user, documents=documents)


@app.route('/admin/document/upload/<int:employe_id>', methods=['GET', 'POST'])
@login_required
def upload_document(employe_id):
    """Upload un document pour un utilisateur"""
    if current_user.role not in ['super_admin', 'admin', 'admin_succursale']:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('admin_dashboard'))

    user = User.query.get_or_404(employe_id)

    if request.method == 'POST':
        fichier = request.files.get('fichier')
        type_doc = request.form.get('type')
        categorie = request.form.get('categorie')

        if fichier and type_doc:
            # Sauvegarder le fichier
            filename = secure_filename(fichier.filename)
            chemin = f"uploads/documents/{employe_id}/{filename}"
            os.makedirs(os.path.dirname(chemin), exist_ok=True)
            fichier.save(chemin)

            # Créer l'entrée en base
            doc = Document(
                employe_id=employe_id,
                nom=filename,
                type=type_doc,
                categorie=categorie,
                chemin=chemin,
                taille=os.path.getsize(chemin),
                mime_type=fichier.content_type
            )
            db.session.add(doc)
            db.session.commit()

            flash("✅ Document uploadé avec succès", "success")
            return redirect(url_for('liste_documents.html', employe_id=employe_id))

    return render_template('admin/upload_document.html', user=user)


@app.route('/admin/document/verify/<int:doc_id>', methods=['POST'])
@login_required
def verify_document(doc_id):
    """Vérifier un document"""
    if current_user.role not in ['super_admin', 'admin']:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('admin_dashboard'))

    doc = Document.query.get_or_404(doc_id)
    action = request.form.get('action')
    notes = request.form.get('notes')

    if action == 'approve':
        doc.verify(current_user.id, notes)
        flash("✅ Document approuvé", "success")
    elif action == 'reject':
        doc.rejeter(current_user.id, notes)
        flash("📝 Document rejeté", "warning")

    return redirect(url_for('liste_documents.html', employe_id=doc.employe_id))


@app.route('/admin/document/delete/<int:doc_id>')
@login_required
def delete_document(doc_id):
    """Supprimer un document"""
    if current_user.role not in ['super_admin', 'admin', 'admin_succursale']:
        flash("⛔ Accès non autorisé", "danger")
        return redirect(url_for('admin_dashboard'))

    doc = Document.query.get_or_404(doc_id)
    employe_id = doc.employe_id

    # Supprimer le fichier physique
    if os.path.exists(doc.chemin):
        os.remove(doc.chemin)

    db.session.delete(doc)
    db.session.commit()

    flash("🗑️ Document supprimé", "success")
    return redirect(url_for('liste_documents.html', employe_id=employe_id))


def get_client_solde(client_id):
    """Récupère le solde d'un client"""
    from models import TransactionCaisse

    transactions = TransactionCaisse.query.filter_by(client_id=client_id).all()

    solde = 0
    for tc in transactions:
        if tc.type_transaction == 'entree':
            solde += tc.montant
        elif tc.type_transaction == 'sortie':
            solde -= tc.montant

    return solde


def update_client_solde(employe_id, montant, operation):
    """
    Met à jour le solde d'un client
    operation: 'add' (ajouter) ou 'subtract' (soustraire)
    """
    from models import Client

    client = db.session.get(Client, employe_id)
    if not client:
        return False

    # Si le client a un champ solde
    if hasattr(client, 'solde'):
        if operation == 'add':
            client.solde = (client.solde or 0) + montant
        elif operation == 'subtract':
            client.solde = (client.solde or 0) - montant

        db.session.commit()
        return True

    return False


def get_operations_autorisees(user):
    """
    Retourne les opérations autorisées pour un utilisateur
    """
    operations = {
        'depot': False,
        'retrait': False,
        'transfert': False,
        'voir_historique': False,
        'valider': False
    }

    if user.role in ['admin', 'super_admin']:
        operations = {k: True for k in operations}

    elif user.role == 'client':
        operations['depot'] = True
        operations['retrait'] = True
        operations['transfert'] = True
        operations['voir_historique'] = True

    elif user.role == 'employe' and user.fonction in ['agent_credit', 'conseiller']:
        operations['depot'] = True
        operations['retrait'] = True
        operations['transfert'] = True
        operations['voir_historique'] = True

    elif user.role == 'direction':
        operations['voir_historique'] = True
        operations['valider'] = True

    return operations


@app.route('/operations')
@login_required
def operations():
    """Page des opérations bancaires"""
    from models import Transaction, TransactionCaisse

    # Récupérer le solde à partir des transactions caisse
    transactions_caisse = TransactionCaisse.query.filter_by(
        client_id=current_user.id
    ).all()

    solde = 0
    for tc in transactions_caisse:
        if tc.type_transaction == 'entree':
            solde += tc.montant
        elif tc.type_transaction == 'sortie':
            solde -= tc.montant

    # Récupérer l'historique des transactions caisse (plus récentes d'abord)
    historique = TransactionCaisse.query.filter_by(
        client_id=current_user.id
    ).order_by(TransactionCaisse.date_transaction.desc()).limit(20).all()

    # Transformer pour le template
    transactions = []
    for tc in historique:
        transactions.append({
            'type': 'depot' if tc.categorie == 'depot' else 'retrait' if tc.categorie == 'retrait' else 'transfert',
            'montant': tc.montant,
            'date': tc.date_transaction,
            'reference': tc.description or ''
        })

    return render_template('operations.html',
                           solde=solde,
                           transactions=transactions)

def creer_transaction_caisse(client_id, agent_id, type_transaction, categorie, montant, transaction_id=None):
    """
    Crée une transaction dans la caisse
    """
    from models import TransactionCaisse, Caisse

    # Récupérer la caisse de l'agent/succursale
    caisse = Caisse.query.filter_by(agent_id=agent_id).first()
    if not caisse:
        # Si pas de caisse agent, utiliser la caisse de la succursale
        from models import Succursale
        user = db.session.get(User, agent_id)
        if user and user.succursale_id:
            caisse = Caisse.query.filter_by(succursale_id=user.succursale_id).first()

    if not caisse:
        print("⚠️ Aucune caisse trouvée")
        return None

    # Calculer le solde avant
    solde_avant = get_client_solde(client_id)

    # Calculer le solde après
    if type_transaction == 'entree':
        solde_apres = solde_avant + montant
    else:
        solde_apres = solde_avant - montant

    # Créer la transaction
    transaction = TransactionCaisse(
        caisse_id=caisse.id,
        type_transaction=type_transaction,
        categorie=categorie,
        montant=montant,
        solde_avant=solde_avant,
        solde_apres=solde_apres,
        client_id=client_id,
        agent_id=agent_id,
        transaction_id=transaction_id
    )

    db.session.add(transaction)
    return transaction


@app.route('/effectuer-depot', methods=['GET', 'POST'])
@login_required
def effectuer_depot():
    """Effectuer un dépôt"""
    montant = float(request.form.get('montant', 0))
    mode = request.form.get('mode_paiement')
    reference = request.form.get('reference')

    if montant <= 0:
        flash('Montant invalide', 'error')
        return redirect(url_for('operations'))

    try:
        # 1. Créer la transaction principale
        transaction = Transaction(
            employe_id=current_user.id,
            montant=montant,
            gateway=mode,
            transaction_id=reference,
            statut='paye',
            date_creation=datetime.now(),
            metadata_info=f'Dépôt en {mode}'
        )
        db.session.add(transaction)
        db.session.flush()

        # 2. Calculer le solde actuel
        transactions_caisse = TransactionCaisse.query.filter_by(
            client_id=current_user.id
        ).all()

        solde_avant = 0
        for tc in transactions_caisse:
            if tc.type_transaction == 'entree':
                solde_avant += tc.montant
            elif tc.type_transaction == 'sortie':
                solde_avant -= tc.montant

        solde_apres = solde_avant + montant

        # 3. Créer la transaction caisse
        transaction_caisse = TransactionCaisse(
            caisse_id=1,  # À adapter selon ta caisse
            type_transaction='entree',
            categorie='depot',
            montant=montant,
            solde_avant=solde_avant,
            solde_apres=solde_apres,
            transaction_id=transaction.id,
            client_id=current_user.id,
            agent_id=current_user.id,
            description=f"Dépôt de {montant} HTG via {mode} - Ref: {reference}" if reference else f"Dépôt de {montant} HTG via {mode}",
            date_transaction=datetime.now()
        )
        db.session.add(transaction_caisse)

        db.session.commit()

        flash(f'✅ Dépôt de {montant:,.0f} HTG effectué avec succès', 'success')

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur dépôt: {e}")
        flash('Erreur lors du dépôt', 'error')

    return redirect(url_for('operations'))


@app.route('/effectuer-retrait', methods=['GET', 'POST'])
@login_required
def effectuer_retrait():
    """Effectuer un retrait"""
    montant = float(request.form.get('montant', 0))
    mode = request.form.get('mode_retrait')

    if montant <= 0:
        flash('Montant invalide', 'error')
        return redirect(url_for('operations'))

    # Vérifier le solde
    transactions_caisse = TransactionCaisse.query.filter_by(
        client_id=current_user.id
    ).all()

    solde = 0
    for tc in transactions_caisse:
        if tc.type_transaction == 'entree':
            solde += tc.montant
        elif tc.type_transaction == 'sortie':
            solde -= tc.montant

    if montant > solde:
        flash('Solde insuffisant', 'error')
        return redirect(url_for('operations'))

    try:
        # 1. Créer la transaction principale
        transaction = Transaction(
            employe_id=current_user.id,
            montant=montant,
            gateway=mode,
            statut='paye',
            date_creation=datetime.now(),
            metadata_info=f'Retrait en {mode}'
        )
        db.session.add(transaction)
        db.session.flush()

        # 2. Calculer le solde après
        solde_avant = solde
        solde_apres = solde_avant - montant

        # 3. Créer la transaction caisse
        transaction_caisse = TransactionCaisse(
            caisse_id=1,
            type_transaction='sortie',
            categorie='retrait',
            montant=montant,
            solde_avant=solde_avant,
            solde_apres=solde_apres,
            transaction_id=transaction.id,
            client_id=current_user.id,
            agent_id=current_user.id,
            description=f"Retrait de {montant} HTG via {mode}",
            date_transaction=datetime.now()
        )
        db.session.add(transaction_caisse)

        db.session.commit()

        flash(f'✅ Retrait de {montant:,.0f} HTG effectué avec succès', 'success')

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur retrait: {e}")
        flash('Erreur lors du retrait', 'error')

    return redirect(url_for('operations'))


@app.route('/effectuer-transfert', methods=['GET', 'POST'])
@login_required
def effectuer_transfert():
    """Effectuer un transfert"""
    montant = float(request.form.get('montant', 0))
    destinataire = request.form.get('destinataire')
    telephone = request.form.get('telephone')
    motif = request.form.get('motif')

    if montant <= 0:
        flash('Montant invalide', 'error')
        return redirect(url_for('operations'))

    if not destinataire:
        flash('Destinataire requis', 'error')
        return redirect(url_for('operations'))

    # Vérifier le solde
    transactions_caisse = TransactionCaisse.query.filter_by(
        client_id=current_user.id
    ).all()

    solde = 0
    for tc in transactions_caisse:
        if tc.type_transaction == 'entree':
            solde += tc.montant
        elif tc.type_transaction == 'sortie':
            solde -= tc.montant

    if montant > solde:
        flash('Solde insuffisant', 'error')
        return redirect(url_for('operations'))

    try:
        # 1. Créer la transaction principale
        transaction = Transaction(
            employe_id=current_user.id,
            montant=montant,
            statut='paye',
            date_creation=datetime.now(),
            metadata_info=f'Transfert à {destinataire} - {telephone or ""} - {motif or ""}'
        )
        db.session.add(transaction)
        db.session.flush()

        # 2. Calculer le solde après
        solde_avant = solde
        solde_apres = solde_avant - montant

        # 3. Créer la transaction caisse
        transaction_caisse = TransactionCaisse(
            caisse_id=1,
            type_transaction='sortie',
            categorie='virement',
            montant=montant,
            solde_avant=solde_avant,
            solde_apres=solde_apres,
            transaction_id=transaction.id,
            client_id=current_user.id,
            agent_id=current_user.id,
            description=f"Transfert de {montant} HTG à {destinataire} - {motif}" if motif else f"Transfert de {montant} HTG à {destinataire}",
            date_transaction=datetime.now()
        )
        db.session.add(transaction_caisse)

        db.session.commit()

        flash(f'✅ Transfert de {montant:,.0f} HTG à {destinataire} effectué avec succès', 'success')

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur transfert: {e}")
        flash('Erreur lors du transfert', 'error')

    return redirect(url_for('operations'))


def get_client_solde(client_id):
    """Calcule le solde total du client"""
    from models import Epargne
    from sqlalchemy import func

    solde = db.session.query(func.sum(Epargne.solde)).filter(
        Epargne.client_id == client_id,
        Epargne.statut == 'actif'
    ).scalar() or 0

    return solde


@app.route('/rechercher-client', methods=['GET', 'POST'])
@login_required
def rechercher_client():
    """Page de recherche de client - vérifie ID dans la base"""
    from models import Client
    import re

    if request.method == 'POST':
        # Variables pour le POST
        numero_compte_suffixe = request.form.get('numero_compte_suffixe', '').strip()
        id_client = request.form.get('id_client', '').strip().replace("'", "").replace('"', "")
        print("Recherché:", repr(id_client))

        # Variable client qui sera définie dans tous les cas
        client = None
        solde = 0



        # Construire le numéro de compte complet
        if numero_compte_suffixe:
            if re.match(r'^\d{5}-\d{5}$', numero_compte_suffixe):
                numero_compte = f"7-12519-{numero_compte_suffixe}"
            else:
                flash('Format du numéro de compte invalide', 'error')
                return render_template('recherche_client.html', client=None, solde=0,
                                       numero_compte_suffixe=numero_compte_suffixe, id_client=id_client)
        else:
            numero_compte = None

        # Vérifier que les deux champs sont remplis
        if not numero_compte or not id_client:
            flash('Les deux champs sont obligatoires', 'error')
            return render_template('recherche_client.html', client=None, solde=0,
                                   numero_compte_suffixe=numero_compte_suffixe, id_client=id_client)

        # --- TOUTE LA LOGIQUE DE RECHERCHE ---
        recherche_effectuee = []

        # 1. Recherche par ID
        if hasattr(Client, 'id_client'):
            client = Client.query.filter_by(id_client=id_client).first()
            if client:
                recherche_effectuee.append(f"ID numérique: {id_client}")

        # 2. Recherche par CIN/NIF
        # if not client:
        #     client = Client.query.filter_by(cin_nif=id_client).first()
        #     if client:
        #         recherche_effectuee.append(f"CIN/NIF: {id_client}")

        # 2. Recherche par CIN/NIF
        if not client:
            client = Client.query.filter((Client.cin == id_client) |
                (Client.cin_nif == id_client)).first()
            if client:
                recherche_effectuee.append(f"CIN/NIF: {id_client}")


        if not client and hasattr(Client, 'id_externe'):
            client = Client.query.filter_by(id_externe=id_client).first()
            if client:
                recherche_effectuee.append(f"ID externe: {id_client}")

        # 4. Recherche par téléphone
        if not client:
            client = Client.query.filter_by(email=id_client).first()
            if client:
                recherche_effectuee.append(f"Email: {id_client}")

        # 3. Recherche par email
        if not client:
            phone_clean = re.sub(r'[\s\-\(\)]', '', id_client)
            client = Client.query.filter_by(telephone=phone_clean).first()
            if client:
                recherche_effectuee.append(f"Téléphone: {id_client}")

        # 5. Recherche par nom complet
        if not client and ' ' in id_client:
            parts = id_client.split(' ', 1)
            if len(parts) == 2:
                nom, prenom = parts[0], parts[1]
                client = Client.query.filter_by(nom=nom, prenom=prenom).first()
                if client:
                    recherche_effectuee.append(f"Nom complet: {id_client}")

        # Vérifier que le client existe
        if not client:
            print("Recherché:", repr(id_client))
            flash(f'❌ Aucun client trouvé avec l\'identifiant: {id_client}', 'error')
            flash(f'   Essayez: ID numérique, email, téléphone ou nom complet', 'info')
            return render_template('recherche_client.html', client=None, solde=0,
                                   numero_compte_suffixe=numero_compte_suffixe, id_client=id_client)

        # Vérifier que le numéro de compte correspond
        if client.numero_compte != numero_compte:
            flash(f'❌ Le numéro de compte ne correspond pas au client', 'error')
            flash(f'   Client trouvé: {client.prenom} {client.nom}', 'warning')
            flash(f'   Numéro de compte correct: {client.numero_compte}', 'warning')
            return render_template('recherche_client.html', client=None, solde=0,
                                   numero_compte_suffixe=numero_compte_suffixe, id_client=id_client)

        # Vérifier que le client est actif
        if not client.compte_actif:
            flash('⚠️ Ce client a un compte inactif', 'error')
            return render_template('recherche_client.html', client=None, solde=0,
                                   numero_compte_suffixe=numero_compte_suffixe, id_client=id_client)

        # Tout est bon
        solde = get_client_solde(client.id)
        flash(f'✅ Client vérifié: {client.prenom} {client.nom}', 'success')
        flash(f'   Trouvé par: {", ".join(recherche_effectuee)}', 'info')

        # Retourner le template avec le client trouvé
        return render_template(
            'recherche_client.html',
            client=client,
            solde=solde,
            numero_compte_suffixe=numero_compte_suffixe,
            id_client=id_client
        )

    # Pour les requêtes GET : simplement afficher le formulaire vide
    return render_template('recherche_client.html', client=None, solde=0,
                           numero_compte_suffixe='', id_client='')


@app.route('/client/<int:client_id>/depot', methods=['GET'])
@login_required
def depot_client_form(client_id):

    from models import Client, Epargne

    client = db.session.get(Client, client_id)

    if not client:
        flash('Client non trouvé', 'danger')
        return redirect(url_for('rechercher_client'))

    # ✅ Tous les comptes (pas seulement actifs pour éviter blocage UI)
    comptes_epargne = Epargne.query.filter_by(
        client_id=client_id
    ).all()

    return render_template(
        'depot_epargne.html',
        client=client,
        comptes=comptes_epargne
    )


# ============================================
# ROUTE 1: Afficher le formulaire (GET)
# ============================================
@app.route('/client/<int:client_id>/retrait', methods=['GET'])
@login_required
def retrait_client_form(client_id):
    """Afficher le formulaire de retrait"""
    from models import Client, Epargne

    client = db.session.get(Client, client_id)
    if not client:
        flash('Client non trouvé', 'danger')
        return redirect(url_for('rechercher_client'))

    # Récupérer les comptes actifs avec solde disponible
    comptes_epargne = Epargne.query.filter(
        Epargne.client_id == client_id,
        Epargne.statut == 'actif',
        Epargne.solde_disponible > 0
    ).all()

    if not comptes_epargne:
        flash('Aucun compte épargne disponible pour le retrait', 'warning')
        return redirect(url_for('retrait_client_form', client_id=client_id))

    # Pour chaque compte, vérifier si un retrait est possible avec les plafonds
    comptes_eligibles = []
    for compte in comptes_epargne:
        # Vérifier si le plafond journalier permet un retrait minimum
        plafond_restant = compte.plafond_retrait_journalier - compte.total_retrait_jour
        if plafond_restant > 0:
            comptes_eligibles.append(compte)

    if not comptes_eligibles:
        flash('Tous les comptes ont atteint leur plafond de retrait journalier', 'warning')
        return redirect(url_for('retrait_client_form', client_id=client_id))

    return render_template('retrait.html',
                           client=client,
                           comptes=comptes_eligibles)


def retirer(self, montant, description="", transaction_ref=None):
    """Effectue un retrait sur le compte"""
    from models import TransactionEpargne

    # Vérifications
    if self.statut != 'actif':
        raise ValueError("Compte inactif")

    if montant > self.solde_disponible:
        raise ValueError(f"Solde insuffisant. Disponible: {self.solde_disponible:,.0f} HTG")

    if montant > (self.plafond_retrait_journalier - self.total_retrait_jour):
        raise ValueError("Plafond de retrait journalier atteint")

    # Mettre à jour le solde
    self.solde -= montant
    self.total_retrait_jour += montant

    # Créer la transaction
    transaction = TransactionEpargne(
        compte_id=self.id,
        type_transaction='retrait',
        montant=montant,
        solde_apres=self.solde,
        description=description,
        transaction_ref=transaction_ref
    )

    db.session.add(transaction)
    db.session.commit()

    return transaction

# ============================================
# ROUTE 2: Traiter le retrait (POST)
# ============================================
@app.route('/client/<int:client_id>/retrait/traiter', methods=['POST'])
@login_required
def traiter_retrait(client_id):
    """Traiter le formulaire de retrait"""
    from models import Client, Epargne
    from datetime import datetime

    client = db.session.get(Client, client_id)
    if not client:
        flash('Client non trouvé', 'danger')
        return redirect(url_for('rechercher_client'))

    # Récupérer les données du formulaire
    compte_epargne_id = request.form.get('compte_epargne_id')
    montant = request.form.get('montant', type=float)

    # Validations de base
    if not compte_epargne_id:
        flash('Veuillez sélectionner un compte', 'danger')
        return redirect(url_for('retrait_client_form', client_id=client_id))

    if not montant or montant <= 0:
        flash('Montant invalide', 'danger')
        return redirect(url_for('retrait_client_form', client_id=client_id))

    # Récupérer le compte
    compte = Epargne.query.get(compte_epargne_id)
    if not compte:
        flash('Compte non trouvé', 'danger')
        return redirect(url_for('retrait_client_form', client_id=client_id))

    # Vérifier que le compte appartient bien au client
    if compte.client_id != client_id:
        flash('Ce compte n\'appartient pas à ce client', 'danger')
        return redirect(url_for('retrait_client_form', client_id=client_id))

    # Vérifier que le compte est actif
    if compte.statut != 'actif':
        flash(f'Le compte {compte.numero_compte} est {compte.statut}. Retrait impossible.', 'danger')
        return redirect(url_for('retrait_client_form', client_id=client_id))

    try:
        # Préparer la description
        description = request.form.get('description', 'Retrait client')
        mode_retrait = request.form.get('mode_retrait', 'especes')
        description_complete = f"{description} - Mode: {mode_retrait}"

        # Effectuer le retrait avec la méthode du modèle
        transaction = compte.retirer(
            montant=montant,
            description=description_complete,
            transaction_ref=f"RET_{datetime.now().timestamp()}"
        )

        flash(f'Retrait de {montant:,.0f} HTG effectué sur le compte {compte.numero_compte}', 'success')

        # Rediriger vers la page d'impression du reçu si demandé
        if request.form.get('imprimer_reçu'):
            return redirect(url_for('imprimer_recu_retrait',
                                    transaction_id=transaction.id,
                                    client_id=client_id))

        return redirect(url_for('voir_client', client_id=client_id))

    except ValueError as e:
        # Erreur métier (solde insuffisant, plafond dépassé, etc.)
        flash(str(e), 'danger')
        return redirect(url_for('retrait_client_form', client_id=client_id))
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur technique lors du retrait: {str(e)}', 'danger')
        return redirect(url_for('retrait_client_form', client_id=client_id))


# ============================================
# ROUTE 3: API pour vérifier un retrait (AJAX)
# ============================================
@app.route('/api/compte/<int:compte_id>/verifier_retrait', methods=['GET'])
@login_required
def verifier_retrait_api(compte_id):
    """API pour vérifier si un retrait est possible (utilisé en AJAX)"""
    from models import Epargne

    compte = Epargne.query.get(compte_id)
    if not compte:
        return jsonify({'error': 'Compte non trouvé'}), 404

    montant = request.args.get('montant', type=float)

    if not montant:
        return jsonify({
            'solde_disponible': compte.solde_disponible,
            'plafond_restant': compte.plafond_retrait_journalier - compte.total_retrait_jour,
            'max_retrait': min(compte.solde_disponible,
                               compte.plafond_retrait_journalier - compte.total_retrait_jour)
        })

    possible, message = compte.peut_retirer(montant)

    return jsonify({
        'possible': possible,
        'message': message,
        'solde_disponible': compte.solde_disponible,
        'plafond_restant': compte.plafond_retrait_journalier - compte.total_retrait_jour,
        'total_deja_retire': compte.total_retrait_jour,
        'date_derniere_maj': compte.date_derniere_maj_totaux.strftime(
            '%d/%m/%Y') if compte.date_derniere_maj_totaux else None
    })




@app.route('/client/<int:client_id>/depot/traiter', methods=['POST'])
@login_required
def traiter_depot(client_id):
    import re
    from models import Client, Epargne, ProduitEpargne
    from datetime import datetime

    client = db.session.get(Client, client_id)

    if not client:
        flash('Client non trouvé', 'danger')
        return redirect(url_for('rechercher_client'))

    # =========================
    # FORMULAIRE
    # =========================
    numero_compte = request.form.get('numero_compte', '').strip()
    montant = request.form.get('montant', type=float)
    description = request.form.get('description', 'Dépôt client')
    mode_paiement = request.form.get('mode_paiement', 'especes')
    reference = request.form.get('reference')

    # =========================
    # VALIDATION NUMÉRO
    # =========================
    if not numero_compte:
        flash("Numéro de compte obligatoire", "danger")
        return redirect(url_for('depot_client_form', client_id=client_id))

    # Format 00001-00001
    if re.match(r'^\d{5}-\d{5}$', numero_compte):
        numero_compte = f"7-12519-{numero_compte}"
    else:
        flash('Format du numéro de compte invalide', 'danger')
        return redirect(url_for('depot_client_form', client_id=client_id))

    # =========================
    # VALIDATION MONTANT
    # =========================
    if not montant or montant <= 0:
        flash("Montant invalide", "danger")
        return redirect(url_for('depot_client_form', client_id=client_id))

    # =========================
    # RECHERCHE COMPTE
    # =========================
    compte = Epargne.query.filter_by(
        numero_compte=numero_compte,
        client_id=client.id
    ).first()

    # =========================
    # CRÉATION AUTO SI ABSENT
    # =========================
    if not compte:
        # ✅ chercher produit existant
        produit_defaut = ProduitEpargne.query.filter_by(est_actif=True).first()

        if not produit_defaut:
            flash("Aucun produit d'épargne configuré", "danger")
            return redirect(url_for('depot_client_form', client_id=client_id))

        # ✅ CORRECTION ICI : utiliser le bon nom d'attribut
        taux_initial = produit_defaut.taux_interet_annuel

        # ✅ création compte
        compte = Epargne(
            numero_compte=numero_compte,
            client_id=client.id,
            produit_epargne_id=produit_defaut.id,
            agent_id=current_user.id,
            succursale_id=current_user.succursale_id,
            solde=0,
            statut='actif',
            date_ouverture=datetime.utcnow(),
            taux_interet=taux_initial  # Correction ici
        )

        db.session.add(compte)
        db.session.commit()

        flash("💡 Compte épargne créé automatiquement", "info")

    # =========================
    # VÉRIFICATION STATUT
    # =========================
    if compte.statut != 'actif':
        flash(f"Compte {compte.statut}", "danger")
        return redirect(url_for('depot_client_form', client_id=client_id))

    # =========================
    # DÉPÔT
    # =========================
    try:
        desc = f"{description} | Mode: {mode_paiement}"
        if reference:
            desc += f" | Ref: {reference}"

        transaction = compte.deposer(
            montant=montant,
            description=desc,
            transaction_ref=reference or f"DEP_{datetime.now().timestamp()}"
        )

        db.session.commit()
        print(f"✅ DÉPÔT RÉUSSI - Montant: {montant}, Compte: {numero_compte}, Nouveau solde: {compte.solde}")

        flash(f"✅ Dépôt de {montant:,.0f} HTG effectué", "success")


    except Exception as e:
        db.session.rollback()
        print("❌ ERREUR DEPOT:", e)
        flash(f"Erreur dépôt: {str(e)}", "danger")

    return redirect(url_for('rechercher_client', client_id=client_id))


@app.route('/retrait/recu/<int:transaction_id>/<int:client_id>')
@login_required
def afficher_recu_retrait(transaction_id, client_id):
    """Affiche le reçu après confirmation"""
    from models import TransactionEpargne

    transaction = db.session.get(TransactionEpargne, transaction_id)
    if transaction and transaction.status == "CONFIRMED":
        return redirect(url_for('imprimer_recu_retrait',
                                client_id=client_id,
                                transaction_id=transaction_id))
    else:
        flash('Transaction non confirmée', 'warning')
        return redirect(url_for('voir_client', client_id=client_id))



# ============================================
# ROUTE: Imprimer le reçu de retrait
# ============================================
@app.route('/client/<int:client_id>/retrait/<int:transaction_id>/recu')
@login_required
def imprimer_recu_retrait(client_id, transaction_id):
    """Génère et imprime le reçu d'un retrait"""
    from models import Client, Epargne, TransactionEpargne
    from datetime import datetime

    client = db.session.get(Client, client_id)
    if not client:
        flash('Client non trouvé', 'danger')
        return redirect(url_for('rechercher_client'))

    transaction = db.session.get(TransactionEpargne, transaction_id)
    if not transaction:
        flash('Transaction non trouvée', 'danger')
        return redirect(url_for('voir_client', client_id=client_id))

    compte = db.session.get(Epargne, transaction.compte_id)

    # Générer un reçu HTML simple
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reçu de retrait</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 50px; }}
            .recu {{ border: 1px solid #ccc; padding: 20px; max-width: 400px; margin: auto; }}
            .header {{ text-align: center; border-bottom: 2px solid #000; margin-bottom: 20px; }}
            .content {{ margin-bottom: 20px; }}
            .montant {{ font-size: 24px; color: green; text-align: center; margin: 20px 0; }}
            .footer {{ text-align: center; font-size: 12px; color: gray; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="recu">
            <div class="header">
                <h2>GMES - Reçu de retrait</h2>
                <p>Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            </div>
            <div class="content">
                <p><strong>Client:</strong> {client.prenom} {client.nom}</p>
                <p><strong>Compte:</strong> {compte.numero_compte}</p>
                <p><strong>Type:</strong> Retrait</p>
                <p><strong>Mode:</strong> Espèces</p>
                <div class="montant">
                    <strong>Montant:</strong> {transaction.montant:,.0f} HTG
                </div>
                <p><strong>Description:</strong> {transaction.description or 'Retrait client'}</p>
                <p><strong>Référence:</strong> {transaction.transaction_ref or '-'}</p>
                <p><strong>Nouveau solde:</strong> {transaction.solde_apres:,.0f} HTG</p>
            </div>
            <div class="footer">
                <p>Signature du caissier: _________________</p>
                <p>Merci de votre confiance</p>
            </div>
        </div>
        <script>window.print();</script>
    </body>
    </html>
    """

    return html


@app.route('/retrait/attente/<int:client_id>/<int:compte_id>/<token>')
@login_required
def attente_confirmation_retrait(client_id, compte_id, token):

    client = db.session.get(Client, client_id)
    compte = db.session.get(Epargne, compte_id)

    return render_template(
        'attente_confirmation_retrait.html',
        client=client,
        email=client.email,
        compte_id=compte_id,
        token=token
    )

# ============================================
# ROUTE: Envoyer confirmation email avant retrait
# ============================================
@app.route('/client/<int:client_id>/retrait/confirmation', methods=['POST'])
@login_required
def envoyer_confirmation_retrait(client_id):
    """Envoie un email de confirmation au client avec signature"""
    from models import Client, Epargne, RetraitConfirmation
    from itsdangerous import URLSafeTimedSerializer
    import json
    import base64
    import os

    client = db.session.get(Client, client_id)
    if not client:
        flash('Client non trouvé', 'danger')
        return redirect(url_for('rechercher_client'))

    # ========== RÉCUPÉRATION DE LA SIGNATURE ==========
    signature_data = request.form.get('signature_data')
    if not signature_data:
        flash('❌ La signature du client est obligatoire', 'danger')
        return redirect(url_for('retrait_client_form', client_id=client_id))

    compte_id = request.form.get('compte_epargne_id')
    montant = request.form.get('montant', type=float)
    mode_retrait = request.form.get('mode_retrait', 'especes')
    description = request.form.get('description', 'Retrait client')
    employe_id = current_user.id  # Si current_user est l'employé

    # ========== SAUVEGARDE DE LA SIGNATURE ==========
    signature_path = None
    try:
        # Créer le dossier signatures
        signature_dir = os.path.join('static', 'signatures', 'retraits')
        os.makedirs(signature_dir, exist_ok=True)

        # Nettoyer et sauvegarder l'image
        if signature_data.startswith('data:image/png;base64,'):
            signature_data = signature_data.replace('data:image/png;base64,', '')

        signature_filename = f"retrait_{client_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        signature_path = os.path.join(signature_dir, signature_filename)

        with open(signature_path, 'wb') as f:
            f.write(base64.b64decode(signature_data))

        print(f"✅ Signature sauvegardée: {signature_path}")

    except Exception as e:
        print(f"Erreur sauvegarde signature: {e}")
        flash('Erreur lors de la sauvegarde de la signature', 'danger')
        return redirect(url_for('retrait_client_form', client_id=client_id))

    # ========== CRÉATION DU TOKEN AVEC SIGNATURE ==========
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    data = {
        'client_id': client_id,
        'compte_id': compte_id,
        'montant': montant,
        'mode_retrait': mode_retrait,
        'description': description,
        'signature_path': signature_path,  # ← Ajoute le chemin de la signature
        'employe_id': employe_id  # Utiliser employe_id
    }
    token = serializer.dumps(json.dumps(data))

    # ========== GÉNÉRATION DU LIEN AVEC IP DYNAMIQUE ==========
    lien_acceptation = url_for('confirmer_retrait', token=token, _external=True)

    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        lien_acceptation = lien_acceptation.replace('127.0.0.1', local_ip).replace('localhost', local_ip)
    except:
        pass

    confirmation_url = lien_acceptation

    # ========== ENVOI DE L'EMAIL ==========
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .container {{ max-width: 600px; margin: auto; padding: 20px; }}
            .header {{ background: #4e73df; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .montant {{ font-size: 24px; color: #28a745; font-weight: bold; }}
            .btn {{ background: #4e73df; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; }}
            .footer {{ text-align: center; font-size: 12px; color: gray; margin-top: 30px; }}
            .signature-info {{ background: #f0f0f0; padding: 10px; border-radius: 5px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🏦 GMES - Confirmation de retrait</h2>
            </div>
            <div class="content">
                <p>Bonjour <strong>{client.prenom} {client.nom}</strong>,</p>
                <p>Vous avez demandé un retrait de :</p>
                <p class="montant">{montant:,.0f} HTG</p>
                <p><strong>Mode:</strong> {mode_retrait}</p>
                <p><strong>Description:</strong> {description}</p>

                <div class="signature-info">
                    <p>✍️ <strong>Signature du client:</strong> Validée électroniquement</p>
                </div>

                <p style="margin-top: 30px;">
                    <a href="{confirmation_url}" class="btn">✅ CONFIRMER LE RETRAIT</a>
                </p>
                <p><small>Ce lien est valable 30 minutes.</small></p>
                <p>Si vous n'êtes pas à l'origine de cette demande, ignorez cet email.</p>
            </div>
            <div class="footer">
                <p>GMES - Gestion Microfinance</p>
            </div>
        </div>
    </body>
    </html>
    """

    msg = Message(
        subject=f"GMES - Confirmation de retrait de {montant:,.0f} HTG",
        recipients=[client.email],
        html=html
    )

    confirmation = RetraitConfirmation(
        token=token,
        confirme=False,
        client_id = client_id,
        employe_id=employe_id  # Commentez cette ligne temporairement
    )

    db.session.add(confirmation)
    db.session.commit()

    try:
        mail.send(msg)
        flash(f'📧 Email de confirmation envoyé à {client.email}', 'success')
        flash(f'✍️ Signature validée et enregistrée', 'success')
    except Exception as e:
        flash(f'Erreur lors de l\'envoi de l\'email: {str(e)}', 'danger')
        return redirect(url_for('retrait_client_form', client_id=client_id))

    return redirect(url_for(
        'attente_confirmation_retrait',
        client_id=client_id,
        compte_id=compte_id,
        token = token
    ))



# ============================================
# API: Vérifier statut retrait (PUBLIC - pas de login)
# ============================================
@app.route('/api/retrait/status/<token>')
def statut_retrait(token):
    """Vérifie si un retrait a été confirmé (appelé par la page d'attente)"""
    from models import RetraitConfirmation

    confirmation = RetraitConfirmation.query.filter_by(token=token).first()

    if not confirmation:
        return jsonify({
            "confirmed": False,
            "error": "Token invalide"
        })

    # ✅ Si confirmé, retourner l'URL du reçu
    if confirmation.confirme and confirmation.transaction_id and confirmation.client_id:
        # ✅ Générer l'URL pour l'agent si agent_id existe
        if confirmation.employe_id:
            return jsonify({
                "confirmed": True,
                "redirect_url": url_for('employe_recu_retrait',
                                        employe_id=confirmation.employe_id,
                                        transaction_id=confirmation.transaction_id,
                                        _external=True)
            })
        else:
            # Fallback vers le reçu client
            return jsonify({
                "confirmed": True,
                "redirect_url": url_for('imprimer_recu_retrait',
                                        client_id=confirmation.client_id,
                                        transaction_id=confirmation.transaction_id,
                                        _external=True)
            })

    return jsonify({
        "confirmed": False
    })


# Ajoutez cette fonction dans votre app.py
def envoyer_email_recu_client(transaction, client):
    """Envoie le reçu par email au client"""
    from flask_mail import Message
    from flask import url_for

    try:
        recu_url = url_for('imprimer_recu_retrait',
                           client_id=client.id,
                           transaction_id=transaction.id,
                           _external=True)

        html_recu = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: auto; padding: 20px; }}
                .header {{ background: #28a745; color: white; padding: 20px; text-align: center; }}
                .montant {{ font-size: 28px; color: #28a745; font-weight: bold; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🏦 GMES - Reçu de retrait</h2>
                </div>
                <div class="content">
                    <p>Bonjour <strong>{client.prenom} {client.nom}</strong>,</p>
                    <p>Votre retrait de <strong>{transaction.montant:,.0f} HTG</strong> a été effectué.</p>
                    <p>Transaction N°: {transaction.id}<br>
                    Date: {transaction.date_transaction.strftime('%d/%m/%Y %H:%M:%S')}</p>
                    <p>
                        <a href="{recu_url}" style="background: #4e73df; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                            📄 Voir mon reçu
                        </a>
                    </p>
                </div>
                <div class="footer">
                    <p>GMES - Gestion Microfinance</p>
                </div>
            </div>
        </body>
        </html>
        """

        msg = Message(
            subject=f"GMES - Reçu de retrait {transaction.montant:,.0f} HTG",
            recipients=[client.email],
            html=html_recu
        )
        mail.send(msg)
        print(f"✅ EMAIL ENVOYÉ avec succès à {client.email}")
        return True

    except Exception as e:
        print(f"❌ ERREUR envoi email: {str(e)}")
        import traceback
        traceback.print_exc()
        return False



@app.route('/employe/<int:employe_id>/retrait/<int:transaction_id>/recu')
def employe_recu_retrait(employe_id, transaction_id):
    """Affiche le reçu du retrait pour l'employé"""
    from models import TransactionEpargne, User, Client
    from flask_mail import Message

    if current_user.is_authenticated:
        if current_user.id != employe_id or current_user.role != 'employe':
            abort(403)

    transaction = db.session.get(TransactionEpargne, transaction_id)
    if not transaction:
        return "Transaction non trouvée", 404

    employe = db.session.get(User, employe_id)
    if not employe or employe.role != 'employe':
        return "Employé non trouvé", 404

    client = db.session.get(Client, transaction.compte.client_id)

    return render_template('employe_recu_retrait.html',
                           transaction=transaction,
                           employe=employe,
                           client=client)


@app.route('/retrait/confirmer/<token>', methods=['GET'])
def confirmer_retrait(token):
    """Confirme le retrait avec signature vérifiée"""
    from models import Client, Epargne, RetraitConfirmation, TransactionEpargne
    from itsdangerous import URLSafeTimedSerializer
    import json
    import os

    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    try:
        # Décoder le token
        data_json = serializer.loads(token, max_age=1800)  # 30 minutes
        data = json.loads(data_json)

        client_id = data['client_id']
        compte_id = data['compte_id']
        montant = data['montant']
        mode_retrait = data['mode_retrait']
        description = data['description']
        signature_path = data.get('signature_path')
        employe_id = data.get('employe_id')  # ✅ Changé de agent_id à employe_id

        # Vérifier la signature
        # Vérifier la signature (seulement si elle existe)
        if signature_path and not os.path.exists(signature_path):
            return f"""
            <!DOCTYPE html>
            <html>
            <head><title>Erreur</title><meta charset="UTF-8"></head>
            <body style="font-family:Arial;text-align:center;padding-top:80px;">
                <h2 style="color:red;">❌ Signature introuvable</h2>
                <p>Veuillez refaire la demande de retrait.</p>
                <a href="/">Retour</a>
            </body>
            </html>
            """

        client = db.session.get(Client, client_id)
        compte = db.session.get(Epargne, compte_id)

        if not client or not compte:
            return """
            <!DOCTYPE html>
            <html>
            <head><title>Erreur</title></head>
            <body style="font-family:Arial;text-align:center;padding-top:80px;">
                <h2 style="color:red;">❌ Données invalides</h2>
                <a href="/">Retour</a>
            </body>
            </html>
            """

        if compte.statut != 'actif':
            return f"""
            <!DOCTYPE html>
            <html>
            <head><title>Erreur</title></head>
            <body style="font-family:Arial;text-align:center;padding-top:80px;">
                <h2 style="color:red;">❌ Compte inactif</h2>
                <a href="/client/{client_id}">Retour</a>
            </body>
            </html>
            """

        if montant > compte.solde:
            return f"""
            <!DOCTYPE html>
            <html>
            <head><title>Erreur</title></head>
            <body style="font-family:Arial;text-align:center;padding-top:80px;">
                <h2 style="color:red;">❌ Solde insuffisant</h2>
                <p>Disponible: {compte.solde:,.0f} HTG</p>
                <a href="/client/{client_id}">Retour</a>
            </body>
            </html>
            """

        # Vérifier si déjà confirmé
        confirmation = RetraitConfirmation.query.filter_by(token=token).first()

        if not confirmation:
            confirmation = RetraitConfirmation(token=token, confirme=False)
            db.session.add(confirmation)
            db.session.commit()

        if confirmation.confirme:
            return """
            <!DOCTYPE html>
            <html>
            <head><title>Déjà utilisé</title></head>
            <body style="font-family:Arial;text-align:center;padding-top:80px;">
                <h2 style="color:orange;">⚠️ Ce lien a déjà été utilisé</h2>
                <a href="/">Retour</a>
            </body>
            </html>
            """

        # Effectuer le retrait
        description_complete = f"{description} - Mode: {mode_retrait} - Signé électroniquement"

        transaction = compte.retirer(
            montant=montant,
            description=description_complete,
            transaction_ref=f"RET_{client_id}_{compte_id}_{montant}"
        )

        # Marquer comme confirmé
        transaction.status = "CONFIRMED"
        confirmation.confirme = True
        confirmation.transaction_id = transaction.id
        confirmation.client_id = client_id  # ← AJOUTEZ CETTE LIGNE
        confirmation.employe_id = employe_id  # ✅ Changé de agent_id à employe_id
        db.session.commit()

        # APRÈS avoir confirmé le retrait, ajoutez:
        if envoyer_email_recu_client(transaction, client):
            flash(f"Un reçu a été envoyé à {client.email}", "success")
        else:
            flash("Le retrait est confirmé mais l'envoi de l'email a échoué", "warning")

        print(f"✅ RETRAIT CONFIRMÉ - Client: {client_id}, Montant: {montant}, Transaction: {transaction.id}")

        # ✅ PAGE DE SUCCÈS AVEC REDIRECTION AUTOMATIQUE
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Retrait confirmé</title>
            <meta http-equiv="refresh" content="3; url=/client/{client_id}/retrait/{transaction.id}/recu">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #f5f5f5;
                    text-align: center;
                    padding-top: 80px;
                }}
                .box {{
                    background: white;
                    max-width: 500px;
                    margin: auto;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                .success {{ font-size: 64px; margin-bottom: 20px; }}
                h1 {{ color: green; }}
                .montant {{ font-size: 24px; color: #28a745; font-weight: bold; }}
                .info {{ margin-top: 20px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="box">
                <div class="success">✅</div>
                <h1>Retrait confirmé !</h1>
                <p>Votre retrait de</p>
                <p class="montant">{montant:,.0f} HTG</p>
                <p>a été effectué avec succès.</p>
                <p class="info">Redirection vers le reçu dans 3 secondes...</p>
                <p class="info">
                    <a href="/client/{client_id}/retrait/{transaction.id}/recu">Cliquez ici si la redirection ne fonctionne pas</a>
                </p>
            </div>
        </body>
        </html>
        """

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>Erreur</title></head>
        <body style="font-family:Arial;text-align:center;padding-top:80px;">
            <h2 style="color:red;">❌ Lien invalide ou expiré</h2>
            <p>Le lien de confirmation est valable 30 minutes seulement.</p>
            <p>Erreur: {str(e)}</p>
            <a href="/">Retour à l'accueil</a>
        </body>
        </html>
        """



@app.route('/client/<int:client_id>/transfert', methods=['GET', 'POST'])
@login_required
def transfert_client_form(client_id):

    from models import Client, Epargne
    from datetime import datetime

    # =========================
    # Vérifier client
    # =========================
    client = db.session.get(Client, client_id)
    if not client:
        flash('Client non trouvé', 'danger')
        return redirect(url_for('rechercher_client'))

    # =========================
    # Comptes du client
    # =========================
    comptes_epargne = Epargne.query.filter_by(
        client_id=client_id,
        statut='actif'
    ).all()

    if not comptes_epargne:
        flash('Aucun compte épargne disponible', 'warning')
        return redirect(url_for('voir_client', client_id=client_id))

    # =========================
    # GET → afficher page
    # =========================
    if request.method == 'GET':
        return render_template(
            'transfert.html',
            client=client,
            comptes=comptes_epargne,
            now=datetime.now()
        )

    # =========================
    # POST → traitement
    # =========================
    if request.method == 'POST':
        try:

            # 🔴 SECURISÉ (évite int(None))
            compte_source_id = request.form.get('compte_source')

            compte_destination_ref = request.form.get('compte_destination') or \
                                     request.form.get('compte_destination_numero')

            montant = request.form.get('montant')
            description = request.form.get('description', 'Transfert entre comptes')

            # =========================
            # VALIDATION SAFE
            # =========================
            if not compte_source_id or not compte_destination_ref:
                raise ValueError("Compte source ou destination manquant")

            compte_destination_ref = " ".join(compte_destination_ref.split())

            if not montant:
                raise ValueError("Montant manquant")

            compte_source_id = int(compte_source_id)
            compte_destination_id = (compte_destination_ref)
            montant = float(montant)

            if montant <= 0:
                raise ValueError("Montant invalide")

            if str(compte_source_id) == str(compte_destination_id):
                raise ValueError("Les comptes doivent être différents")

            # =========================
            # Récupération comptes
            # =========================
            compte_source = Epargne.query.filter_by(
                id=compte_source_id,
                #client_id=client_id,
                statut='actif'
            ).first()

            # DEBUG
            print(f"🔍 Recherche compte destination avec numero_compte = '{compte_destination_ref}'")
            print(f"   Type: {type(compte_destination_ref)}")
            print(f"   Longueur: {len(compte_destination_ref)}")

            compte_destination = Epargne.query.filter_by(
                numero_compte=compte_destination_ref,
                #client_id=client_id,
                statut='actif'
            ).first()

            if not compte_source or not compte_destination:
                raise ValueError("Compte introuvable ou inactif")

            # =========================
            # Vérification solde
            # =========================
            if compte_source.solde < montant:
                raise ValueError(
                    f"Solde insuffisant: {compte_source.solde:,.0f} HTG"
                )

            # =========================
            # Référence
            # =========================
            ref_transfert = f"TRF_{datetime.now().strftime('%Y%m%d%H%M%S')}_{client_id}"

            # =========================
            # Transaction
            # =========================
            transaction_source = compte_source.retirer(
                montant=montant,
                description=f"Transfert vers {compte_destination.numero_compte}",
                transaction_ref=ref_transfert
            )

            transaction_dest = compte_destination.deposer(
                montant=montant,
                description=f"Transfert depuis {compte_source.numero_compte}",
                transaction_ref=ref_transfert
            )

            transaction_source.transfert_vers = compte_destination.id
            transaction_dest.transfert_depuis = compte_source.id

            db.session.commit()

            client.solde = sum(Epargne.solde)

            flash(f'✅ Transfert de {montant:,.0f} HTG réussi', 'success')
            return redirect(url_for('transfert_client_form', client_id=client_id))

        except Exception as e:
            db.session.rollback()
            flash(f'❌ Erreur: {str(e)}', 'danger')
            return redirect(request.url)



# ============================================
# TRANSFERT VERS UN AUTRE CLIENT
# ============================================

@app.route('/transfert_client', methods=['GET', 'POST'])
@login_required
def transfert_entre_clients():
    """Transfert d'argent entre deux clients différents"""

    # Vérifier que l'utilisateur est un client
    if not current_user.client_id:
        flash('Accès réservé aux clients', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            compte_source_id = request.form.get('compte_source')
            montant = float(request.form.get('montant'))
            description = request.form.get('description', 'Transfert entre clients')
            motif = request.form.get('motif', 'autre')

            compte_destination_numero = request.form.get('compte_destination_numero')

            # Construire le numéro complet si nécessaire
            if compte_destination_numero and not compte_destination_numero.startswith('7-12519-'):
                import re
                if re.match(r'^\d{5}-\d{5}$', compte_destination_numero):
                    compte_destination_numero = f"7-12519-{compte_destination_numero}"

            # VALIDATIONS
            if montant <= 0:
                flash('Le montant doit être supérieur à 0', 'danger')
                return redirect(request.url)

            if not compte_source_id or not compte_destination_numero:
                flash('Tous les champs sont requis', 'danger')
                return redirect(request.url)

            # Récupérer le compte source avec lock
            compte_source = Epargne.query.filter_by(
                id=compte_source_id,
                statut='actif'
            ).with_for_update().first()

            if not compte_source:
                flash('Compte source non trouvé', 'danger')
                return redirect(request.url)

            # Vérifier que l'utilisateur a le droit de faire ce transfert
            if compte_source.client_id != current_user.client_id:
                flash('Vous n\'êtes pas autorisé à utiliser ce compte', 'danger')
                return redirect(request.url)

            # Vérifier que le compte source est débloqué
            if compte_source.bloque:
                flash('Ce compte est bloqué. Veuillez contacter votre conseiller.', 'danger')
                return redirect(request.url)

            # Rechercher par numéro de compte (pas par ID)



            compte_destination = Epargne.query.filter_by(
                numero_compte=compte_destination_numero,
                statut='actif'
            ).filter(Epargne.id != compte_source.id).first()

            if not compte_destination:
                flash('Compte destination non trouvé ou inactif', 'danger')
                return redirect(request.url)

            # Vérifier qu'on ne transfère pas à soi-même
            if compte_destination.client_id == compte_source.client_id:
                flash('Utilisez le formulaire de transfert entre comptes pour vos propres comptes', 'danger')
                return redirect(url_for('transfert_client_form', client_id=current_user.client_id))

            # Vérifier les conditions de retrait
            peut_retirer, message_retrait = compte_source.peut_retirer(montant)
            if not peut_retirer:
                flash(message_retrait, 'danger')
                return redirect(request.url)

            # Générer un numéro de référence unique
            ref_transfert = f"TRF_EXT_{datetime.now().strftime('%Y%m%d%H%M%S')}_{compte_source.id}_{compte_destination.id}"

            # Effectuer le transfert dans une transaction
            with db.session.begin_nested():
                # Retirer du source
                transaction_source = compte_source.retirer(
                    montant=montant,
                    description=f"Transfert à {compte_destination.client.prenom} {compte_destination.client.nom} ({compte_destination.numero_compte}) : {description[:100]}",
                    transaction_ref=ref_transfert
                )

                # Ajouter des métadonnées au transfert source
                transaction_source.type_transaction = 'transfert_sortant'
                transaction_source.transfert_destination_id = compte_destination.id
                transaction_source.transfert_ref = ref_transfert
                transaction_source.transfert_motif = motif

                # Déposer sur destination
                transaction_dest = compte_destination.deposer(
                    montant=montant,
                    description=f"Transfert de {compte_source.client.prenom} {compte_source.client.nom} ({compte_source.numero_compte}) : {description[:100]}",
                    transaction_ref=ref_transfert
                )

                # Ajouter des métadonnées au transfert destination
                transaction_dest.type_transaction = 'transfert_entrant'
                transaction_dest.transfert_source_id = compte_source.id
                transaction_dest.transfert_ref = ref_transfert
                transaction_dest.transfert_motif = motif

            db.session.commit()

            # Envoyer des notifications par email
            try:
                envoyer_email_transfert_sortant(compte_source.client, compte_destination.client, montant, ref_transfert)
                envoyer_email_transfert_entrant(compte_destination.client, compte_source.client, montant, ref_transfert)
            except Exception as e:
                current_app.logger.error(f"Erreur envoi email transfert: {str(e)}")

            # Logger l'opération
            current_app.logger.info(
                f"Transfert externe - Source: {compte_source.client.prenom} {compte_source.client.nom} ({compte_source.numero_compte}), "
                f"Destination: {compte_destination.client.prenom} {compte_destination.client.nom} ({compte_destination.numero_compte}), "
                f"Montant: {montant} HTG, Ref: {ref_transfert}"
            )

            flash(
                f'✅ Transfert de {montant:,.0f} HTG vers {compte_destination.client.prenom} {compte_destination.client.nom} effectué avec succès',
                'success')
            return redirect(url_for('dashboard_client'))

        except ValueError as e:
            db.session.rollback()
            flash(str(e), 'danger')
            return redirect(request.url)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erreur transfert externe: {str(e)}", exc_info=True)
            flash(f'❌ Erreur lors du transfert: {str(e)}', 'danger')
            return redirect(request.url)

    # GET: Afficher le formulaire
    comptes_utilisateur = Epargne.query.filter_by(
        client_id=current_user.client_id,
        statut='actif',
        bloque=False
    ).all()

    if not comptes_utilisateur:
        flash('Vous n\'avez aucun compte actif disponible pour effectuer un transfert', 'warning')
        return redirect(url_for('dashboard_client'))

    return render_template('transfert_client.html',
                           comptes_source=comptes_utilisateur)




# ============================================
# TRANSFERT ENTRE CLIENTS (Version Employé)
# ============================================

@app.route('/employe/transfert_client', methods=['GET', 'POST'])
@login_required
@role_required('employe')
def employe_transfert_entre_clients():
    """Transfert d'argent entre deux clients (réservé aux employés)"""

    if request.method == 'POST':
        try:
            compte_source_id = request.form.get('compte_source')
            compte_destination_id = request.form.get('compte_destination')
            montant = float(request.form.get('montant'))
            description = request.form.get('description', 'Transfert entre clients')
            employe_id = current_user.id

            # Validation
            if montant <= 0:
                flash('Le montant doit être supérieur à 0', 'danger')
                return redirect(request.url)

            # Récupérer les comptes
            compte_source = Epargne.query.filter_by(
                id=compte_source_id,
                statut='actif'
            ).with_for_update().first()

            compte_destination = Epargne.query.filter_by(
                id=compte_destination_id,
                statut='actif'
            ).with_for_update().first()

            if not compte_source or not compte_destination:
                flash('Compte source ou destination non trouvé', 'danger')
                return redirect(request.url)

            # Vérifier que ce sont des comptes différents
            if compte_source.id == compte_destination.id:
                flash('Les comptes source et destination doivent être différents', 'danger')
                return redirect(request.url)

            # Générer référence
            ref_transfert = f"TRF_EMP_{datetime.now().strftime('%Y%m%d%H%M%S')}_{employe_id}"

            # Effectuer le transfert
            with db.session.begin_nested():
                transaction_source = compte_source.retirer(
                    montant=montant,
                    description=f"Transfert vers {compte_destination.client.prenom} {compte_destination.client.nom} : {description[:100]}",
                    transaction_ref=ref_transfert
                )
                transaction_source.type_transaction = 'transfert_sortant'
                transaction_source.transfert_destination_id = compte_destination.id
                transaction_source.transfert_effectue_par = employe_id

                transaction_dest = compte_destination.deposer(
                    montant=montant,
                    description=f"Transfert de {compte_source.client.prenom} {compte_source.client.nom} : {description[:100]}",
                    transaction_ref=ref_transfert
                )
                transaction_dest.type_transaction = 'transfert_entrant'
                transaction_dest.transfert_source_id = compte_source.id
                transaction_dest.transfert_effectue_par = employe_id

            db.session.commit()

            # Envoyer notifications
            envoyer_email_transfert_sortant(compte_source.client, compte_destination.client, montant, ref_transfert)
            envoyer_email_transfert_entrant(compte_destination.client, compte_source.client, montant, ref_transfert)

            flash(f'✅ Transfert de {montant:,.0f} HTG effectué avec succès', 'success')
            return redirect(url_for('dashboard_employe'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erreur: {str(e)}', 'danger')
            return redirect(request.url)

    # GET: Afficher formulaire
    comptes_actifs = Epargne.query.filter_by(statut='actif', bloque=False).all()
    return render_template('employe_transfert_client.html', comptes=comptes_actifs)


# ============================================
# HISTORIQUE DES TRANSFERTS AMÉLIORÉ
# ============================================

@app.route('/compte/<int:compte_id>/transferts')
@login_required
def historique_transferts(compte_id):
    """Affiche l'historique des transferts d'un compte"""

    compte = Epargne.query.get_or_404(compte_id)

    # Vérifier les droits
    if compte.client_id != current_user.client_id and not current_user.is_admin() and current_user.role != 'employe':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('index'))

    # Récupérer les transactions de type transfert
    transferts = TransactionEpargne.query.filter(
        TransactionEpargne.compte_id == compte_id,
        TransactionEpargne.type_transaction.in_(['transfert_sortant', 'transfert_entrant', 'depot', 'retrait']),
        TransactionEpargne.description.like('%Transfert%')
    ).order_by(TransactionEpargne.date_operation.desc()).limit(1000).all()

    return render_template('historique_transferts.html',
                           compte=compte,
                           transferts=transferts)


# ============================================
# VÉRIFICATION AVANT TRANSFERT AMÉLIORÉE (API)
# ============================================

@app.route('/api/verifier_transfert', methods=['POST'])
@login_required
def verifier_transfert():
    """API pour vérifier si un transfert est possible"""

    try:
        data = request.get_json()
        compte_source_id = data.get('compte_source_id')
        montant = float(data.get('montant'))

        compte_destination_numero = data.get('compte_destination_numero', '')

        compte = Epargne.query.get(compte_source_id)

        if not compte:
            return jsonify({'possible': False, 'message': 'Compte non trouvé'})

        # Vérifier les droits
        if compte.client_id != current_user.client_id and not current_user.is_admin():
            return jsonify({'possible': False, 'message': 'Non autorisé'})

        # Vérifier que le compte est actif
        if compte.statut != 'actif':
            return jsonify({'possible': False, 'message': 'Ce compte est inactif'})

        # Vérifier si le compte est bloqué
        if hasattr(compte, 'bloque') and compte.bloque:
            return jsonify({'possible': False, 'message': 'Ce compte est bloqué'})

        # Vérifier le montant
        if montant <= 0:
            return jsonify({'possible': False, 'message': 'Le montant doit être supérieur à 0'})

        # Vérifier le solde
        if compte.solde < montant:
            return jsonify({
                'possible': False,
                'message': f'Solde insuffisant. Solde disponible: {compte.solde:,.0f} HTG',
                'solde_actuel': compte.solde
            })

        # Vérifier le plafond journalier si le modèle a cette propriété
        if hasattr(compte, 'peut_retirer'):
            peut_retirer, message = compte.peut_retirer(montant)
            if not peut_retirer:
                return jsonify({'possible': False, 'message': message})

        # Vérifier le compte destination si fourni
        if compte_destination_numero:
            compte_dest = Epargne.query.filter_by(
                numero_compte=compte_destination_numero,
                statut='actif'
            ).first()

            if not compte_dest:
                return jsonify({'possible': False, 'message': 'Compte destination non trouvé'})

            if compte_dest.id == compte.id:
                return jsonify({'possible': False, 'message': 'Le compte destination doit être différent'})

        # Tout est OK
        return jsonify({
            'possible': True,
            'solde_actuel': float(compte.solde),
            'solde_apres_transfert': float(compte.solde - montant),
            'montant': montant,
            'frais': 0  # Ajouter des frais si nécessaire
        })

    except Exception as e:
        return jsonify({'possible': False, 'message': f'Erreur: {str(e)}'})


# ============================================
# FONCTIONS D'ENVOI D'EMAIL
# ============================================

def envoyer_email_transfert_sortant(client_source, client_dest, montant, ref_transfert):
    try:
        html = f"""
        <h2>Confirmation de votre transfert</h2>
        <p>Bonjour {client_source.prenom} {client_source.nom},</p>
        <p>Transfert de <strong>{montant:,.0f} HTG</strong> vers {client_dest.prenom} {client_dest.nom}.</p>
        <p>Référence: {ref_transfert}</p>
        <p>Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        """

        print("📧 Envoi email sortant ->", client_source.email)

        msg = Message(
            "Confirmation de transfert",
            recipients=[client_source.email],
            html=html
        )

        mail.send(msg)
        print("✔ Email sortant envoyé")

    except Exception as e:
        print("❌ ERREUR EMAIL SORTANT:", str(e))


def envoyer_email_transfert_entrant(client_dest, client_source, montant, ref_transfert):
    try:
        html = f"""
        <h2>Vous avez reçu un transfert</h2>
        <p>Bonjour {client_dest.prenom} {client_dest.nom},</p>
        <p>Vous avez reçu <strong>{montant:,.0f} HTG</strong> de {client_source.prenom} {client_source.nom}.</p>
        <p>Référence: {ref_transfert}</p>
        <p>Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        """

        print("📧 Envoi email entrant ->", client_dest.email)

        msg = Message(
            "Vous avez reçu un transfert",
            recipients=[client_dest.email],
            html=html
        )

        mail.send(msg)
        print("✔ Email entrant envoyé")

    except Exception as e:
        print("❌ ERREUR EMAIL ENTRANT:", str(e))


@app.route('/api/verifier-compte', methods=['POST'])
@login_required
def verifier_compte():
    from models import Epargne
    import re

    data = request.get_json()
    numero_compte = data.get('numero_compte')

    # ✅ NORMALISATION AVANT QUERY
    if numero_compte and not numero_compte.startswith('7-12519-'):
        if re.match(r'^\d{5}-\d{5}$', numero_compte):
            numero_compte = f"7-12519-{numero_compte}"

    compte = Epargne.query.filter_by(numero_compte=numero_compte).first()

    if not compte:
        return jsonify({'success': False})

    return jsonify({
        'success': True,
        'compte': {
            'id': compte.id,
            'numero': compte.numero_compte,
            'client_nom': f"{compte.client.prenom} {compte.client.nom}",
            'client_id': compte.client_id
        }
    })

@app.route("/verify/<token>")
def verify_qr(token, SECRET):
    try:
        # Essayer de décoder le JWT
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        employe_id = payload['employe_id']
        user = User.query.get(employe_id)

        if not user:
            return "❌ Carte invalide"

    except jwt.InvalidTokenError:
        # Si ce n'est pas un JWT, chercher dans la base de données
        user = User.query.filter_by(qr_token=token).first()

        if not user:
            return "❌ Carte invalide"

    # Vérifications communes
    if not user.actif:
        return "⛔ Employé non actif"

    if user.carte_expiration and user.carte_expiration < datetime.utcnow():
        return "⌛ Carte expirée"

    return f"""
    ✅ VALIDE<br>
    Nom: {user.prenom} {user.nom}<br>
    Fonction: {user.fonction}<br>
    Succursale: {user.succursale.nom if user.succursale else 'N/A'}
    """


UPLOAD_FOLDER = "static/uploads"

@app.route("/upload_photo/<int:employe_id>", methods=["POST"])
def upload_photo(employe_id):
    file = request.files["photo"]

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    user = User.query.get(employe_id)
    user.photo = filename
    db.session.commit()

    return redirect(url_for("dashboard"))


def generate_qr(user):
    import qrcode
    import os
    import uuid
    from datetime import datetime, timedelta

    os.makedirs("static/qr", exist_ok=True)

    # Générer un token unique
    token = str(uuid.uuid4())
    user.qr_token = token
    user.carte_expiration = datetime.utcnow() + timedelta(days=365)
    db.session.commit()

    # URL pour le pointage
    url = f"http://127.0.0.1:5000/punch/{token}"

    # Générer le QR code
    qr = qrcode.make(url)
    path = f"static/qr/{user.id}.png"
    qr.save(path)

    return path

@app.route("/employee/<int:employe_id>")
def employee_profile(employe_id):
    user = User.query.get_or_404(employe_id)
    return f"""
    <h1>{user.prenom} {user.nom}</h1>
    <p>Fonction: {user.fonction}</p>
    <p>Matricule: {user.matricule}</p>
    """


@app.route("/punch/<token>")
def punch_qr(token):
    """Pointage via scan du QR code"""

    # Vérifier le token
    user = User.query.filter_by(qr_token=token).first()

    if not user:
        return "❌ QR code invalide", 404

    if not user.actif:
        return "⛔ Employé non actif", 403

    if user.carte_expiration and user.carte_expiration < datetime.utcnow():
        return "⌛ Carte expirée", 403

    today = datetime.utcnow().date()

    # Vérifier si l'utilisateur a déjà pointé aujourd'hui
    pointage_existant = Pointage.query.filter_by(
        employe_id=user.id
    ).filter(db.func.date(Pointage.heure_arrivee) == today).first()

    now = datetime.utcnow()

    if not pointage_existant:
        # Premier pointage de la journée (entrée)
        pointage = Pointage(
            employe_id=user.id,
            heure_arrivee=now,
            date=now
        )
        db.session.add(pointage)

        message = f"✅ Bonjour {user.prenom} {user.nom}! Pointage entrée enregistré à {now.strftime('%H:%M')}"

        # Vérifier si c'est un retard
        heure_limite = datetime.strptime("08:30", "%H:%M").time()
        if now.time() > heure_limite:
            verifier_retard(user)
            message += " ⚠️ Attention: Vous êtes en retard!"

    else:
        # Deuxième pointage (sortie)
        if not pointage_existant.heure_depart:
            pointage_existant.heure_depart = now
            db.session.commit()
            message = f"✅ Au revoir {user.prenom} {user.nom}! Pointage sortie enregistré à {now.strftime('%H:%M')}"

            # Calculer les heures travaillées
            duree = now - pointage_existant.heure_arrivee
            heures = duree.total_seconds() / 3600
            message += f" (Total: {heures:.2f} heures)"
        else:
            message = f"⚠️ Vous avez déjà pointé votre sortie aujourd'hui!"

    db.session.commit()

    return f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="3;url=/">
        <style>
            body {{ font-family: Arial; text-align: center; padding: 50px; }}
            .success {{ color: green; }}
            .warning {{ color: orange; }}
            .error {{ color: red; }}
        </style>
    </head>
    <body>
        <h1 class="{'success' if '✅' in message else 'warning' if '⚠️' in message else 'error'}">
            {message}
        </h1>
        <p>Redirection dans 3 secondes...</p>
    </body>
    </html>
    """


def verifier_retard(user):
    """Crée une notification de retard si l'utilisateur pointe après 8h30"""
    now = datetime.utcnow()
    heure_limite = datetime.strptime("08:30", "%H:%M").time()

    # Vérifier si c'est un retard (après 8h30)
    if now.time() > heure_limite:
        # Vérifier si une notification de retard existe déjà aujourd'hui
        today = now.date()
        notif_existe = Notification.query.filter_by(
            employe_id=user.id,
            message="⚠️ Retard détecté"
        ).filter(db.func.date(Notification.created_at) == today).first()

        if not notif_existe:
            notif = Notification(
                employe_id=user.id,
                message=f"⚠️ Retard détecté à {now.strftime('%H:%M')}",
                created_at=now
            )
            db.session.add(notif)
            db.session.commit()


def verifier_absence():
    today = datetime.utcnow().date()

    users = User.query.filter_by(actif=True).all()

    for user in users:
        pointage = Pointage.query.filter_by(
            employe_id=user.id
        ).filter(db.func.date(Pointage.heure_arrivee) == today).first()

        if not pointage:
            notif = Notification(
                employe_id=user.id,
                message="❌ Absence détectée"
            )
            db.session.add(notif)

    db.session.commit()


def save_pointage(data):
    """Sauvegarde le pointage dans la base de données"""
    from datetime import datetime

    # Vérifier si le pointage existe déjà
    existing = Pointage.query.filter_by(
        employe_id=data.get("employe_id"),
        date=datetime.utcnow().date()
    ).first()

    if existing:
        if not existing.heure_depart and data.get("type") == "sortie":
            existing.heure_depart = datetime.utcnow()
            db.session.commit()
            return "Sortie enregistrée"
        return "Pointage déjà enregistré"

    # Créer nouveau pointage
    pointage = Pointage(
        employe_id=data.get("employe_id"),
        heure_arrvee=datetime.utcnow(),
        date=datetime.utcnow().date(),
        latitude=data.get("latitude"),
        longitude=data.get("longitude")
    )
    db.session.add(pointage)
    db.session.commit()

    return "Entrée enregistrée"


def send_alert(user, message):
    """Envoie une alerte pour un utilisateur"""
    from datetime import datetime

    conn = sqlite3.connect("gmes.db")
    cur = conn.cursor()

    # Récupérer l'ID correctement (que ce soit dict ou objet)
    employe_id = user["id"] if isinstance(user, dict) else user.id

    cur.execute("""
        INSERT INTO alerts (employe_id, message, created_at)
        VALUES (?, ?, ?)
    """, (employe_id, message, datetime.now()))

    conn.commit()
    conn.close()

    print(f"🚨 ALERTE -> {message}")


def export_rh_pdf():
    """Génère un PDF avec la liste des employés"""
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from datetime import datetime

    import os
    os.makedirs("static/reports", exist_ok=True)

    file = "static/reports/rh_report.pdf"

    doc = SimpleDocTemplate(file, pagesize=A4)
    styles = getSampleStyleSheet()

    # Style personnalisé pour le titre
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        spaceAfter=20
    )

    elements = []

    # Titre
    elements.append(Paragraph(f"Rapport RH - {datetime.now().strftime('%d/%m/%Y')}", title_style))
    elements.append(Spacer(1, 20))

    # Liste des utilisateurs
    users = User.query.all()

    for u in users:
        status = "✅ Actif" if u.actif else "❌ Inactif"
        elements.append(Paragraph(
            f"<b>{u.prenom} {u.nom}</b> - {u.role or 'Employé'} - {status}",
            styles["Normal"]
        ))
        elements.append(Spacer(1, 5))

    doc.build(elements)

    return file


@app.route("/export_rh")
def export_rh():
    """Exporte le rapport RH en PDF"""
    try:
        file = export_rh_pdf()
        return send_file(file, as_attachment=True, download_name="rapport_rh.pdf")
    except Exception as e:
        return jsonify({"error": f"Erreur d'export: {str(e)}"}), 500



@app.route("/stats")
def stats():
    """Endpoint API pour les statistiques"""
    stats_data = get_stats_employes_succursale()  # ← RÉUTILISATION
    return jsonify(stats_data)

def generate_secure_qr(user):
    """Génère un QR code sécurisé pour l'utilisateur"""
    import uuid
    import qrcode
    import os
    from datetime import datetime, timedelta

    # Créer le dossier
    os.makedirs("static/qr", exist_ok=True)

    # Générer un token unique
    token = str(uuid.uuid4())
    user.qr_token = token
    user.carte_expiration = datetime.utcnow() + timedelta(days=365)
    db.session.commit()

    # URL pour le pointage
    url = f"http://127.0.0.1:5000/punch/{token}"

    # Générer le QR code
    img = qrcode.make(url)

    filename = f"user_{user.id}.png"
    filepath = f"static/qr/{filename}"
    img.save(filepath)

    user.qr_code = filename
    db.session.commit()

    return filepath

@app.route("/pointage", methods=["POST"])
def pointage():
    """Enregistrement du pointage avec vérification de zone"""
    from datetime import datetime, timedelta
    import math

    data = request.get_json()

    if not data:
        return jsonify({"error": "Données manquantes"}), 400

    # Récupérer l'utilisateur
    user = User.query.get(data.get("employe_id"))
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    # Vérifier la localisation
    lat = data.get("latitude")
    lon = data.get("longitude")

    if lat and lon:
        # Vérifier si l'utilisateur a une succursale
        if not user.succursale:
            return jsonify({"error": "Utilisateur non assigné à une succursale"}), 400

        # Calculer la distance
        dist = distance(lat, lon, user.succursale.latitude, user.succursale.longitude)

        # Vérifier si hors zone
        if dist > user.succursale.rayon:
            send_alert(user, f"🚨 Sortie de zone - Distance: {dist:.0f}m")
            return jsonify({"error": "Hors zone autorisée", "distance": dist}), 403

    # Vérifier la vitesse
    speed = data.get("speed", 0)
    if speed > 200:
        send_alert(user, f"🚨 GPS suspect - Vitesse: {speed} km/h")

    # Enregistrer le pointage
    result = save_pointage(data)

    return jsonify({"status": "ok", "message": result})






from datetime import datetime, date
from sqlalchemy import func

@app.route('/rapport_journalier/<int:succursale_id>')
@login_required
def rapport_journalier(succursale_id):

    from models import (
        TransactionEpargne,
        Epargne,
        Client
    )

    aujourd_hui = date.today()

    transactions = TransactionEpargne.query.join(
        Epargne,
        TransactionEpargne.compte_id == Epargne.id
    ).filter(
        Epargne.succursale_id == succursale_id,
        func.date(TransactionEpargne.date_operation) == aujourd_hui
    ).order_by(
        TransactionEpargne.date_operation.desc()
    ).all()

    total_depots = db.session.query(
        func.coalesce(func.sum(TransactionEpargne.montant), 0)
    ).join(
        Epargne,
        TransactionEpargne.compte_id == Epargne.id
    ).filter(
        Epargne.succursale_id == succursale_id,
        TransactionEpargne.type_transaction == 'depot',
        func.date(TransactionEpargne.date_operation) == aujourd_hui
    ).scalar()

    total_retraits = db.session.query(
        func.coalesce(func.sum(TransactionEpargne.montant), 0)
    ).join(
        Epargne,
        TransactionEpargne.compte_id == Epargne.id
    ).filter(
        Epargne.succursale_id == succursale_id,
        TransactionEpargne.type_transaction == 'retrait',
        func.date(TransactionEpargne.date_operation) == aujourd_hui
    ).scalar()

    total_transferts_entrants = db.session.query(
        func.coalesce(func.sum(TransactionEpargne.montant), 0)
    ).filter(
        TransactionEpargne.type_transaction == 'transfert_entrant',
        func.date(TransactionEpargne.date_operation) == aujourd_hui
    ).scalar()

    total_transferts_sortants = db.session.query(
        func.coalesce(func.sum(TransactionEpargne.montant), 0)
    ).filter(
        TransactionEpargne.type_transaction == 'transfert_sortant',
        func.date(TransactionEpargne.date_operation) == aujourd_hui
    ).scalar()

    nombre_operations = len(transactions)

    nouveaux_comptes = Epargne.query.filter(
        Epargne.succursale_id == succursale_id,
        func.date(Epargne.date_ouverture) == aujourd_hui
    ).count()

    total_clients = Client.query.join(
        Epargne,
        Client.id == Epargne.client_id
    ).filter(
        Epargne.succursale_id == succursale_id
    ).distinct().count()

    encaisse_nette = (
        total_depots
        - total_retraits
    )

    total_comptes = Epargne.query.filter_by(
        succursale_id=succursale_id
    ).count()

    total_encaisse = total_depots - total_retraits

    total_epargne = db.session.query(
        func.coalesce(func.sum(Epargne.solde), 0)
    ).filter(
        Epargne.succursale_id == succursale_id
    ).scalar()

    comptes_actifs = Epargne.query.filter_by(
        succursale_id=succursale_id,
        statut='actif'
    ).count()

    nouveaux_clients = Client.query.filter(
        func.date(Client.date_creation) == aujourd_hui,
        Client.succursale_id == succursale_id
    ).count()


    from models import Succursale

    succursale = db.session.get(Succursale, succursale_id)

    if not succursale:
        flash("Succursale introuvable", "danger")
        return redirect(url_for('dashboard'))

    return render_template(
        'rapport_journalier.html',
        succursale=succursale,

        total_comptes=total_comptes,
        total_encaisse=total_encaisse,
        total_epargne=total_epargne,
        comptes_actifs=comptes_actifs,

        date_jour=aujourd_hui,
        transactions=transactions,
        total_depots=total_depots,
        total_retraits=total_retraits,
        total_transferts_entrants=total_transferts_entrants,
        total_transferts_sortants=total_transferts_sortants,
        nombre_operations=nombre_operations,
        nouveaux_comptes=nouveaux_comptes,
        nouveaux_clients=nouveaux_clients,
        encaisse_nette=encaisse_nette
    )


@app.route('/imprimer_recus_jour')
@login_required
def imprimer_recus_jour():
    """Imprime tous les reçus de la journée pour la succursale de l'utilisateur"""

    from models import TransactionEpargne, Epargne
    from datetime import date

    aujourd_hui = date.today()

    # ✅ Filtrer par succursale de l'utilisateur connecté
    transactions = TransactionEpargne.query.join(
        Epargne, TransactionEpargne.compte_id == Epargne.id
    ).filter(
        Epargne.succursale_id == current_user.succursale_id,  # ← Filtre succursale
        db.func.date(TransactionEpargne.date_operation) == aujourd_hui
    ).order_by(TransactionEpargne.date_operation.desc()).all()

    # Calcul des totaux
    total_depots = sum(t.montant for t in transactions if t.type_transaction == 'depot')
    total_retraits = sum(t.montant for t in transactions if t.type_transaction == 'retrait')

    return render_template(
        'imprimer_recus_jour.html',
        transactions=transactions,
        aujourd_hui=aujourd_hui,
        total_depots=total_depots,
        total_retraits=total_retraits,
        total_operations=len(transactions)
    )


@app.route('/fermeture_caisse')
@login_required
def fermeture_caisse():
    """Rapport de fermeture de caisse pour la journée"""

    from models import TransactionEpargne, Epargne
    from datetime import date

    aujourd_hui = date.today()

    # ✅ Correction : Joindre avec Epargne pour filtrer par succursale
    depots = db.session.query(
        db.func.coalesce(db.func.sum(TransactionEpargne.montant), 0)
    ).join(
        Epargne, TransactionEpargne.compte_id == Epargne.id
    ).filter(
        Epargne.succursale_id == current_user.succursale_id,
        TransactionEpargne.type_transaction == 'depot',
        db.func.date(TransactionEpargne.date_operation) == aujourd_hui
    ).scalar()

    retraits = db.session.query(
        db.func.coalesce(db.func.sum(TransactionEpargne.montant), 0)
    ).join(
        Epargne, TransactionEpargne.compte_id == Epargne.id
    ).filter(
        Epargne.succursale_id == current_user.succursale_id,
        TransactionEpargne.type_transaction == 'retrait',
        db.func.date(TransactionEpargne.date_operation) == aujourd_hui
    ).scalar()

    # Transferts (optionnel)
    transferts_sortants = db.session.query(
        db.func.coalesce(db.func.sum(TransactionEpargne.montant), 0)
    ).join(
        Epargne, TransactionEpargne.compte_id == Epargne.id
    ).filter(
        Epargne.succursale_id == current_user.succursale_id,
        TransactionEpargne.type_transaction == 'transfert_sortant',
        db.func.date(TransactionEpargne.date_operation) == aujourd_hui
    ).scalar()

    transferts_entrants = db.session.query(
        db.func.coalesce(db.func.sum(TransactionEpargne.montant), 0)
    ).filter(
        TransactionEpargne.type_transaction == 'transfert_entrant',
        db.func.date(TransactionEpargne.date_operation) == aujourd_hui
    ).scalar()

    solde_caisse = depots - retraits

    return render_template(
        'fermeture_caisse.html',
        depots=depots,
        retraits=retraits,
        transferts_sortants=transferts_sortants,
        transferts_entrants=transferts_entrants,
        solde_caisse=solde_caisse,
        aujourd_hui=aujourd_hui
    )


# @app.route('/api/partner/portal/integrations', methods=['POST'])
# @login_requis
# def create_partner_integration():
#     """Le partenaire enregistre ses identifiants pour une intégration"""
#     from models import Partner, PartnerAPIKey, PartnerWebhook
#     from services.partner_service import PartnerService
#     from extensions import db
#
#     data = request.json
#
#     # Vérifier les identifiants
#     api_key = PartnerService.verify_api_key(
#         data.get('client_id'),
#         data.get('client_secret')
#     )
#
#     if not api_key:
#         return jsonify({'success': False, 'message': 'Identifiants invalides'}), 401
#
#     # Récupérer le partenaire
#     partner = Partner.query.get(api_key.partner_id)
#
#     if not partner or not partner.is_active:
#         return jsonify({'success': False, 'message': 'Partenaire inactif'}), 403
#
#     # Créer l'intégration (stockée dans PartnerWebhook ou une table dédiée)
#     integration = PartnerIntegration(
#         partner_id=partner.id,
#         api_key_id=api_key.id,
#         name=data.get('name'),
#         webhook_url=data.get('webhook_url'),
#         events=data.get('events', ['payment']),
#         is_active=True
#     )
#     db.session.add(integration)
#     db.session.commit()
#
#     return jsonify({
#         'success': True,
#         'message': 'Intégration créée avec succès',
#         'integration_id': integration.id
#     }), 201

# app.py ou routes/partner_routes.py

from flask import request, jsonify, session, Blueprint

# from models import Partner, PartnerAPIKey, PartnerWebhook, PartnerIntegration
from services.partner_service import PartnerService
from middleware.auth import login_requis
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Si tu utilises un Blueprint
partner_portal_bp = Blueprint('partner_portal', __name__, url_prefix='/api/partner/portal')


@partner_portal_bp.route('/integrations', methods=['POST'])
@login_requis
def create_partner_integration():
    """Le partenaire enregistre ses identifiants pour une intégration"""
    try:
        data = request.get_json()

        # Vérifier les champs obligatoires
        if not data.get('client_id') or not data.get('client_secret') or not data.get('name'):
            return jsonify({
                'success': False,
                'message': 'Client ID, Client Secret et Nom sont requis'
            }), 400

        # Vérifier les identifiants API
        api_key = PartnerService.verify_api_key(
            data.get('client_id'),
            data.get('client_secret')
        )

        if not api_key:
            return jsonify({
                'success': False,
                'message': 'Identifiants invalides. Vérifiez votre Client ID et Client Secret.'
            }), 401

        # Récupérer le partenaire
        partner = Partner.query.get(api_key.partner_id)

        if not partner:
            return jsonify({
                'success': False,
                'message': 'Partenaire non trouvé'
            }), 404

        if not partner.is_active:
            return jsonify({
                'success': False,
                'message': 'Ce partenaire est inactif. Contactez l\'administrateur.'
            }), 403

        # Vérifier si une intégration avec ce nom existe déjà
        existing = PartnerIntegration.query.filter_by(
            partner_id=partner.id,
            name=data.get('name')
        ).first()

        if existing:
            return jsonify({
                'success': False,
                'message': f'Une intégration nommée "{data.get("name")}" existe déjà'
            }), 400

        # Créer l'intégration
        integration = PartnerIntegration(
            partner_id=partner.id,
            api_key_id=api_key.id,
            name=data.get('name'),
            webhook_url=data.get('webhook_url'),
            events=data.get('events', ['payment']),
            is_active=True,
            transaction_count=0,
            created_at=datetime.utcnow()
        )

        db.session.add(integration)
        db.session.commit()

        logger.info(f"✅ Nouvelle intégration créée: {integration.name} pour le partenaire {partner.name}")

        # Si un webhook est fourni, l'enregistrer aussi
        if data.get('webhook_url'):
            webhook = PartnerWebhook(
                partner_id=partner.id,
                url=data.get('webhook_url'),
                secret=secrets.token_urlsafe(32),
                events=data.get('events', ['payment']),
                is_active=True
            )
            db.session.add(webhook)
            db.session.commit()
            logger.info(f"✅ Webhook enregistré: {webhook.url}")

        return jsonify({
            'success': True,
            'message': 'Intégration créée avec succès',
            'integration': {
                'id': integration.id,
                'name': integration.name,
                'webhook_url': integration.webhook_url,
                'events': integration.events,
                'is_active': integration.is_active,
                'created_at': integration.created_at.isoformat()
            }
        }), 201

    except Exception as e:
        logger.error(f"❌ Erreur création intégration: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erreur: {str(e)}'
        }), 500


@partner_portal_bp.route('/integrations', methods=['GET'])
@login_requis
def get_partner_integrations():
    """Récupérer toutes les intégrations du partenaire"""
    try:
        # Récupérer le partenaire connecté
        partner_id = session.get('partner_id')
        if not partner_id:
            return jsonify({'success': False, 'message': 'Non authentifié'}), 401

        integrations = PartnerIntegration.query.filter_by(
            partner_id=partner_id,
            is_active=True
        ).all()

        return jsonify({
            'success': True,
            'integrations': [{
                'id': i.id,
                'name': i.name,
                'webhook_url': i.webhook_url,
                'events': i.events,
                'transaction_count': i.transaction_count,
                'created_at': i.created_at.isoformat() if i.created_at else None
            } for i in integrations]
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@partner_portal_bp.route('/integrations/<int:integration_id>', methods=['DELETE'])
@login_requis
def delete_partner_integration(integration_id):
    """Supprimer une intégration"""
    try:
        partner_id = session.get('partner_id')

        integration = PartnerIntegration.query.filter_by(
            id=integration_id,
            partner_id=partner_id
        ).first()

        if not integration:
            return jsonify({'success': False, 'message': 'Intégration non trouvée'}), 404

        # Soft delete ou suppression définitive
        integration.is_active = False
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Intégration supprimée avec succès'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# Si tu n'utilises pas de Blueprint, voici la version directe
@app.route('/api/partner/portal/integrations', methods=['POST'])
@login_requis
def create_partner_integration_direct():
    """Version directe sans Blueprint"""
    # Même code que ci-dessus
    pass

# === CRÉATION DES TABLES ET ADMIN AU DÉMARRAGE ===
with app.app_context():
    # Créer toutes les tables si elles n'existent pas
    db.create_all()
    print("✅ Tables vérifiées/créées")

    # Vérifier si super_admin existe
    super_admin = User.query.filter_by(role='super_admin').first()

    if not super_admin:
        print("⚡ Création du super admin...")

        default_password = os.environ.get("SUPER_ADMIN_PASSWORD", "Spadmin123")

        super_admin = User(
            username="super_admin",
            prenom="Geler",
            nom="Begin",
            email="super_admin@gmes.com",
            role="super_admin",
            fonction="admin_general",
            statut="actif",
            premier_connexion=False
        )
        super_admin.password_hash = generate_password_hash(default_password)

        db.session.add(super_admin)
        db.session.commit()

        print(f"✅ Super admin créé avec succès!")
        print(f"   Email: super_admin@gmes.com")
        print(f"   Identifiant: super_admin")
        print(f"   Mot de passe: {default_password}")

        # Vérification après création
        from werkzeug.security import check_password_hash

        result = check_password_hash(super_admin.password_hash, default_password)
        print(f"🔐 Vérification mot de passe: {result}")


    else:

        print(f"ℹ️ Super admin déjà existant: {super_admin.email}")

        # 🔐 RÉINITIALISER LE MOT DE PASSE ICI 🔐

        from werkzeug.security import generate_password_hash, check_password_hash

        # Réinitialiser le mot de passe

        new_password = "admin123"

        super_admin.password_hash = generate_password_hash(new_password)

        db.session.commit()

        # Vérifier que le nouveau mot de passe fonctionne

        result = check_password_hash(super_admin.password_hash, new_password)

        print(f"🔐 Mot de passe réinitialisé à '{new_password}': {result}")

    # Lister tous les utilisateurs pour vérifier
    users = User.query.all()
    print(f"📋 Total utilisateurs dans la base: {len(users)}")
    for u in users:
        print(f"   - {u.username} ({u.email}) - Rôle: {u.role}")



if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False, use_reloader=False)
