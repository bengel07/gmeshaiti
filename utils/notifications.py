import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime
import logging
from itsdangerous import URLSafeTimedSerializer
from flask import url_for
from flask_mail import Message

# # Import différé pour éviter circularité
from models import Client,Notification, Pret, User , Employe # REMPLACÉ PAR IMPORT LOCAL
from database import db

def get_client_model():
    return Client

def get_pret_model():
    return Pret

def get_user_model():
    return User



# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from datetime import datetime

import sqlite3


class NotificationManager:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_username = os.getenv('MAIL_USERNAME', 'gmeshaiti@gmail.com')
        self.smtp_password = os.getenv('MAIL_PASSWORD', 'qgjd lrgh azxi mpvd')
        self.sms_api_key = os.getenv('SMS_API_KEY')
        self.sms_api_secret = os.getenv('SMS_API_SECRET')

        # SMS Short Code / Sender ID
        self.sms_sender = os.getenv('SMS_SENDER', 'GMES')  # ici ton short code ou "GMES"
        self.sms_provider = "shortcode"  # mode simulation/local

    def _generate_terms_token(self, client_id):
        """
        Génère un token sécurisé pour accepter les terms
        """
        secret_key = os.getenv("SECRET_KEY", "dev_secret")  # ou ton SECRET_KEY Flask
        s = URLSafeTimedSerializer(secret_key)
        return s.dumps(client_id, salt="terms-accept")

    def _verify_terms_token(self, token, max_age=86400):
        """
        Vérifie un token Terms (24h par défaut)
        """
        secret_key = os.getenv("SECRET_KEY", "dev_secret")
        s = URLSafeTimedSerializer(secret_key)
        return s.loads(token, salt="terms-accept", max_age=max_age)

    def notifier_acceptation_terms(self, client, lien_terms=None):
        """
        Envoie un email au client pour qu'il accepte les Terms & Conditions
        """
        if not lien_terms:
            # Si le lien n'est pas fourni, le générer
            token = self._generate_terms_token(client.id)
            lien_terms = url_for("terms.accept_terms", token=token, _external=True)

        sujet = "📄 Veuillez accepter les Conditions d'utilisation – GMES"
        message_html = f"""
            <html>
            <body>
                <h2>Bonjour {client.prenom},</h2>
                <p>Votre dossier a été créé avec succès par votre conseiller.</p>
                <p>Avant de continuer, merci d'accepter nos <strong>Conditions d'utilisation</strong>.</p>
                <p>Cliquez sur le lien ci-dessous pour accepter :</p>
                <p style="text-align: center;">
                    <a href="{lien_terms}" style="background: #28a745; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        ✅ Accepter les Conditions
                    </a>
                </p>
                <p>Ou copiez ce lien : <br> {lien_terms}</p>
                <p>Ce lien est valable 7 jours.</p>
                <p>Merci,<br>L'équipe GMES Microcrédit</p>
            </body>
            </html>
        """

        message_text = f"""
    Bonjour {client.prenom},

    Votre dossier a été créé avec succès. Veuillez accepter nos Conditions d'utilisation via ce lien :
    {lien_terms}

    Ce lien est valable 7 jours.

    Merci,
    GMES Microcrédit
        """

        if client.email:
            self.envoyer_email(client.email, sujet, message_html, message_text)
            return True


        # Optionnel: envoyer un SMS
        sms_message = f"GMES: Bonjour {client.prenom}, acceptez vos Conditions ici: {lien_terms}"
        self.envoyer_sms(client.telephone, sms_message)

        return False

    def envoyer_email(self, destinataire, sujet, message_html, message_text=None):
        """
        Envoie un email de notification
        """
        try:
            if not self.smtp_username or not self.smtp_password:
                logger.warning("Configuration SMTP manquante - Email simulé")
                self._simuler_email(destinataire, sujet, message_html)
                return True

            # Création du message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = sujet
            msg['From'] = self.smtp_username
            msg['To'] = destinataire

            # Partie texte
            if message_text:
                part1 = MIMEText(message_text, 'plain')
                msg.attach(part1)

            # Partie HTML
            part2 = MIMEText(message_html, 'html')
            msg.attach(part2)

            # Envoi
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            logger.info(f"Email envoyé à {destinataire}: {sujet}")
            return True

        except Exception as e:
            logger.error(f"Erreur envoi email à {destinataire}: {e}")
            # Simulation en cas d'erreur
            self._simuler_email(destinataire, sujet, message_html)
            return False

    def envoyer_sms(self, telephone, message):
        """
        Envoi de SMS via short code ou simulation.
        Affiche GMES ou short code, pas besoin d'API.
        """
        try:
            # Ici on simule l'envoi avec short code
            sender = self.sms_sender  # GMES ou code 5 chiffres

            # Simulation / Logging
            logger.info(f"📱 [SMS SHORT CODE] À: {telephone}")
            logger.info(f"📱 De: {sender}")
            logger.info(f"📱 Message: {message}")

            # Ici tu peux intégrer un vrai provider local plus tard
            # Ex: Digicel Business SMS, Flow Business SMS

            return True

        except Exception as e:
            logger.error(f"Erreur envoi SMS à {telephone}: {e}")
            return False


    def _simuler_email(self, destinataire, sujet, message):
        """Simule l'envoi d'email pour le développement"""
        logger.info(f"📧 [SIMULATION] Email à {destinataire}")
        logger.info(f"📧 Sujet: {sujet}")
        logger.info(f"📧 Message: {message[:100]}...")

    def _simuler_sms(self, telephone, message):
        """Simule l'envoi de SMS pour le développement"""
        logger.info(f"📱 [SIMULATION] SMS à {telephone}")
        logger.info(f"📱 Message: {message}")

    # Notifications spécifiques au microcrédit
    def notifier_approbation_pret(self, client, pret):
        """Notification d'approbation de prêt"""
        sujet = "🎉 Votre prêt a été approuvé !"

        message_html = f"""
        <html>
        <body>
            <h2>Félicitations {client.prenom} !</h2>
            <p>Votre demande de prêt a été <strong>approuvée</strong>.</p>

            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <h3>Détails du prêt :</h3>
                <ul>
                    <li><strong>Montant :</strong> {pret.montant} HTG</li>
                    <li><strong>Durée :</strong> {pret.duree_mois} mois</li>
                    <li><strong>Mensualité :</strong> {pret.mensualite} HTG</li>
                    <li><strong>Date d'approbation :</strong> {pret.date_approbation.strftime('%d/%m/%Y')}</li>
                </ul>
            </div>

            <p>Vous pouvez maintenant accéder à votre espace client pour plus de détails.</p>
            <p><em>L'équipe GMES Microcrédit</em></p>
        </body>
        </html>
        """

        message_text = f"""
        Félicitations {client.prenom} !
        Votre prêt de {pret.montant} HTG a été approuvé.
        Mensualité: {pret.mensualite} HTG sur {pret.duree_mois} mois.
        """

        # Envoyer email
        if client.email:
            self.envoyer_email(client.email, sujet, message_html, message_text)

        # Envoyer SMS
        sms_message = f"GMES: Prêt approuvé! {pret.montant}HTG, {pret.mensualite}HTG/mois. Rendez-vous sur votre espace client."
        self.envoyer_sms(client.telephone, sms_message)

    def notifier_rejet_pret(self, client, pret, motif=None):
        """Notification de rejet de prêt"""
        sujet = "❌ Votre demande de prêt"

        message_html = f"""
        <html>
        <body>
            <h2>Bonjour {client.prenom},</h2>
            <p>Votre demande de prêt n'a malheureusement pas été approuvée.</p>

            {f'<p><strong>Motif :</strong> {motif}</p>' if motif else ''}

            <p>Nous vous encourageons à :</p>
            <ul>
                <li>Vérifier vos informations personnelles</li>
                <li>Consulter nos conseillers</li>
                <li>Soumettre une nouvelle demande ultérieurement</li>
            </ul>

            <p><em>L'équipe GMES Microcrédit</em></p>
        </body>
        </html>
        """

        if client.email:
            self.envoyer_email(client.email, sujet, message_html)

        sms_message = f"GMES: Votre demande de prêt n'a pas été approuvée. Consultez votre email pour plus de détails."
        self.envoyer_sms(client.telephone, sms_message)

    def notifier_remboursement_reussi(self, client, remboursement):
        """Notification de remboursement réussi"""
        sujet = "✅ Remboursement confirmé"

        message_html = f"""
        <html>
        <body>
            <h2>Merci {client.prenom} !</h2>
            <p>Votre remboursement de <strong>{remboursement.montant} HTG</strong> a été enregistré avec succès.</p>

            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <p><strong>Date :</strong> {remboursement.date_remboursement.strftime('%d/%m/%Y à %H:%M')}</p>
                <p><strong>Méthode :</strong> {remboursement.type_paiement}</p>
                <p><strong>Référence :</strong> {remboursement.reference}</p>
            </div>

            <p>Votre solde a été mis à jour dans votre espace client.</p>
            <p><em>L'équipe GMES Microcrédit</em></p>
        </body>
        </html>
        """

        if client.email:
            self.envoyer_email(client.email, sujet, message_html)

        sms_message = f"GMES: Remboursement de {remboursement.montant}HTG confirmé. Merci!"
        self.envoyer_sms(client.telephone, sms_message)

    def notifier_rappel_remboursement(self, client, pret, jours_restants):
        """Rappel de remboursement"""
        sujet = "⏰ Rappel de remboursement"

        message_html = f"""
        <html>
        <body>
            <h2>Rappel important</h2>
            <p>Bonjour {client.prenom},</p>

            <p>Votre prochaine échéance de remboursement approche :</p>
            <div style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <p><strong>Montant :</strong> {pret.mensualite} HTG</p>
                <p><strong>Jours restants :</strong> {jours_restants}</p>
                <p><strong>Prêt :</strong> #{pret.id} - {pret.montant} HTG</p>
            </div>

            <p>Vous pouvez effectuer votre remboursement depuis votre espace client.</p>
            <p><em>L'équipe GMES Microcrédit</em></p>
        </body>
        </html>
        """

        if client.email:
            self.envoyer_email(client.email, sujet, message_html)

        sms_message = f"GMES: Rappel! {jours_restants}j pour rembourser {pret.mensualite}HTG. Prêt #{pret.id}"
        self.envoyer_sms(client.telephone, sms_message)

    def notifier_nouveau_groupe(self, client, groupe):
        """Notification de nouvel adhérent à un groupe"""
        sujet = "👥 Bienvenue dans votre groupe de solidarité"

        message_html = f"""
        <html>
        <body>
            <h2>Bienvenue {client.prenom} !</h2>
            <p>Vous avez rejoint le groupe <strong>{groupe.nom}</strong>.</p>

            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <p><strong>Groupe :</strong> {groupe.nom}</p>
                <p><strong>Code :</strong> {groupe.code_groupe}</p>
                <p><strong>Zone :</strong> {groupe.zone}</p>
            </div>

            <p>Vous pouvez maintenant bénéficier des avantages des prêts solidaires.</p>
            <p><em>L'équipe GMES Microcrédit</em></p>
        </body>
        </html>
        """

        if client.email:
            self.envoyer_email(client.email, sujet, message_html)

        sms_message = f"GMES: Bienvenue au groupe {groupe.nom}! Code: {groupe.code_groupe}"
        self.envoyer_sms(client.telephone, sms_message)

    def notifier_verification_annuelle():
        today = datetime.utcnow()
        clients = Client.query.filter(Client.verification_next_due <= today).all()

        for client in clients:
            if not client.notification_sent:
                sujet = "🔒 Vérifiez votre identité – Action requise"
                message_html = f"""
                <html><body>
                <h2>Bonjour {client.prenom},</h2>
                <p>Il est temps de vérifier votre identité pour continuer à utiliser votre compte GMES.</p>
                <p>Soumettez un nouveau selfie et vos photos de visage.</p>
                <p>Si vous ne pouvez pas le faire en ligne, venez en agence pour qu’un employé vous aide.</p>
                </body></html>
                """
                message_text = f"Bonjour {client.prenom}, il est temps de vérifier votre identité GMES. Veuillez soumettre un nouveau selfie."

                if client.email:
                    notification_manager.envoyer_email(client.email, sujet, message_html, message_text)
                if client.telephone:
                    sms_message = f"GMES: Veuillez vérifier votre identité pour continuer à utiliser votre compte."
                    notification_manager.envoyer_sms(client.telephone, sms_message)

                # Marquer la notification comme envoyée et bloquer le compte
                client.notification_sent = True
                client.blocked_until_verification = True
                db.session.commit()


    # ========== NOUVELLES MÉTHODES À AJOUTER ==========

    def send_approval_notification(self, pret):
        """Envoyer une notification pour l'approbation d'un prêt"""
        try:
            client = pret.client
            if not client:
                logger.error(f"Client non trouvé pour le prêt #{pret.id}")
                return False

            # 1. Email au client
            sujet = "✅ Votre prêt a été approuvé"
            message_html = f"""
            <html>
            <body>
                <h2>Félicitations {client.prenom} !</h2>
                <p>Votre demande de prêt a été <strong>approuvée</strong>.</p>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
                    <p><strong>Montant demandé :</strong> {pret.montant_demande or pret.montant} Gdes</p>
                    <p><strong>Montant accordé :</strong> {pret.montant_accorde or pret.montant_demande} Gdes</p>
                    <p><strong>Durée :</strong> {pret.duree_mois} mois</p>
                    <p><strong>Taux :</strong> {pret.taux_interet}%</p>
                </div>
                <p>Notre équipe vous contactera pour finaliser.</p>
            </body>
            </html>
            """
            if client.email:
                self.envoyer_email(client.email, sujet, message_html)

            # 2. SMS au client
            sms_message = f"GMES: Pret approuve! {pret.montant_accorde} Gdes, {pret.duree_mois} mois. Contactez votre agence."
            if client.telephone:
                self.envoyer_sms(client.telephone, sms_message)

            # 3. Notification dans la base de données
            self._create_db_notification(
                user_id=pret.agent_id,
                client_id=client.id,
                title="Prêt approuvé",
                message=f"Le prêt #{pret.id} a été approuvé",
                pret_id=pret.id
            )

            # 4. Email à l'agent
            if pret.agent and pret.agent.email:
                sujet_agent = f"Prêt approuvé - {client.prenom} {client.nom}"
                msg_agent = f"Le prêt #{pret.id} pour {client.prenom} {client.nom} a été approuvé."
                self.envoyer_email(pret.agent.email, sujet_agent, f"<p>{msg_agent}</p>", msg_agent)

            return True
        except Exception as e:
            logger.error(f"Erreur send_approval_notification: {e}")
            return False

    def send_refusal_notification(self, pret):
        """Envoyer une notification pour le refus d'un prêt"""
        try:
            client = pret.client
            motif = getattr(pret, 'motif_refus', 'Non spécifié')

            if not client:
                return False

            # 1. Email au client
            sujet = "❌ Mise à jour sur votre demande de prêt"
            message_html = f"""
            <html>
            <body>
                <h2>Bonjour {client.prenom},</h2>
                <p>Votre demande de prêt n'a pas été approuvée.</p>
                <div style="background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107;">
                    <strong>Motif :</strong> {motif}
                </div>
                <p>Nous restons à votre disposition pour d'autres opportunités.</p>
            </body>
            </html>
            """
            if client.email:
                self.envoyer_email(client.email, sujet, message_html)

            # 2. SMS au client
            sms_message = f"GMES: Votre demande de pret a ete refusee. Plus de details par email."
            if client.telephone:
                self.envoyer_sms(client.telephone, sms_message)

            # 3. Notification DB
            self._create_db_notification(
                user_id=pret.agent_id,
                client_id=client.id,
                title="Prêt refusé",
                message=f"Le prêt #{pret.id} a été refusé. Motif: {motif}",
                pret_id=pret.id,
                notification_type="danger"
            )

            return True
        except Exception as e:
            logger.error(f"Erreur send_refusal_notification: {e}")
            return False

    def send_more_information_notification(self, pret, demande_details):
        """Envoyer une notification pour demander plus d'informations"""
        try:
            client = pret.client

            if not client:
                return False

            # 1. Email au client
            sujet = "ℹ️ Informations supplémentaires requises"
            message_html = f"""
            <html>
            <body>
                <h2>Bonjour {client.prenom},</h2>
                <p>Pour finaliser votre demande de prêt, nous avons besoin de :</p>
                <div style="background: #fff3cd; padding: 15px; border-radius: 5px;">
                    {demande_details}
                </div>
                <p>Veuillez fournir ces informations à votre agent ou en agence.</p>
            </body>
            </html>
            """
            if client.email:
                self.envoyer_email(client.email, sujet, message_html)

            # 2. SMS
            sms_message = f"GMES: Veuillez fournir des infos supplementaires pour votre pret. Consultez votre email."
            if client.telephone:
                self.envoyer_sms(client.telephone, sms_message)

            # 3. Notification DB
            self._create_db_notification(
                user_id=pret.agent_id,
                client_id=client.id,
                title="Informations demandées",
                message=f"Pour le prêt #{pret.id}: {demande_details}",
                pret_id=pret.id,
                requires_action=True
            )

            # 4. Email à l'agent
            if pret.agent and pret.agent.email:
                sujet_agent = f"Infos demandées - {client.prenom} {client.nom}"
                msg_agent = f"Le directeur demande: {demande_details}\nPrêt #{pret.id}"
                self.envoyer_email(pret.agent.email, sujet_agent, f"<p>{msg_agent}</p>", msg_agent)

            # Mettre à jour le statut
            pret.status = 'informations_requises'
            db.session.commit()

            return True
        except Exception as e:
            logger.error(f"Erreur send_more_information_notification: {e}")
            return False

    # def _create_db_notification(self, user_id=None, client_id=None, title="", message="",
    #                             pret_id=None, notification_type="info", requires_action=False):
    #     """Créer une notification en base de données"""
    #     try:
    #         notif = Notification(
    #             user_id=user_id,
    #             client_id=client_id,
    #             title=title,
    #             message=message,
    #             type=notification_type,
    #             pret_id=pret_id,
    #             requires_action=requires_action,
    #             created_at=datetime.now(),
    #             is_read=False
    #         )
    #         db.session.add(notif)
    #         db.session.commit()
    #         return notif
    #     except Exception as e:
    #         logger.error(f"Erreur création notification DB: {e}")
    #         db.session.rollback()
    #         return None

    def _create_db_notification(self, destinataire_id=None, client_id=None, titre="", message="",
                                pret_id=None, notification_type="info", requires_action=False,
                                acteur_id=None, lien=None):
        """Créer une notification en base de données"""

        try:
            from models import Notification, Action
            from database import db
            from datetime import datetime

            # Créer une action associée (obligatoire car action_id est NOT NULL)
            action = None
            if pret_id:
                action = Action.query.filter_by(pret_id=pret_id).first()

            if not action:
                action = Action(
                    pret_id=pret_id,
                    type_action=notification_type,
                    date_action=datetime.now(),
                    description=message[:200] if message else "Notification système"
                )
                db.session.add(action)
                db.session.flush()

            # Créer la notification avec TOUS les champs requis
            notif = Notification(
                # Champs obligatoires selon votre modèle
                employe_id=destinataire_id,  # ← employe_id (destinataire)
                destinataire_id=destinataire_id,  # ← votre champ redondant mais obligatoire
                acteur_id=acteur_id,
                action_id=action.id,  # ← OBLIGATOIRE (NOT NULL)

                # Champs de contenu
                titre=titre,
                message=message,
                type_notification=notification_type,
                type=notification_type,

                # Champs de lecture
                lue=False,
                read=False,
                requires_action=requires_action,
                is_read=False,

                # Dates
                date_creation=datetime.now(),
                date_envoi=datetime.now(),
                timestamp=datetime.now(),
                created_at=datetime.now(),

                # Liens
                lien=lien or f"/direction/pret/{pret_id}/view" if pret_id else None,
                url=lien or f"/direction/pret/{pret_id}/view" if pret_id else None,

                # Relations
                pret_id=pret_id,
                client_id=client_id,

                # Autres
                level="info" if notification_type == "success" else notification_type,
                error_id=None
            )

            db.session.add(notif)
            db.session.commit()
            print(f"✅ Notification créée: {titre} pour employé {destinataire_id}")
            return notif

        except Exception as e:
            print(f"❌ Erreur création notification DB: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return None

    def calculer_mensualite(montant, taux_annuel, duree_mois):
        """Calculer la mensualité d'un prêt"""
        if montant and taux_annuel and duree_mois:
            taux_mensuel = taux_annuel / 100 / 12
            facteur = (1 + taux_mensuel) ** duree_mois
            mensualite = montant * taux_mensuel * facteur / (facteur - 1)
            return mensualite
        return 0

# Instance globale
notification_manager = NotificationManager()