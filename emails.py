import os
import threading
import requests
from flask import render_template

# ============================================
# CONFIGURATION EMAIL - VERSION API BREVO
# ============================================

BREVO_API_KEY = os.environ.get('BREVO_API_KEY')
APP_URL = os.environ.get('APP_URL', 'https://gmeshaiti.onrender.com')

# Email expéditeur (doit être vérifié sur Brevo)
FROM_EMAIL = "gmeshaiti@gmail.com"
FROM_NAME = "GMES Microcrédit"


# ============================================
# FONCTION DE BASE POUR ENVOYER UN EMAIL
# ============================================

def send_email(to_email, subject, html_content, from_email=None, from_name=None):
    """
    Envoie un email via l'API Brevo
    """
    if not BREVO_API_KEY:
        print("⚠️ Email non configuré (BREVO_API_KEY manquant)")
        return False

    try:
        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        data = {
            "sender": {
                "name": from_name or FROM_NAME,
                "email": from_email or FROM_EMAIL
            },
            "to": [
                {
                    "email": to_email,
                    "name": to_email.split('@')[0]
                }
            ],
            "subject": subject,
            "htmlContent": html_content
        }

        response = requests.post(url, json=data, headers=headers, timeout=30)

        print("=" * 60)
        print("DESTINATAIRE :", to_email)
        print("STATUS :", response.status_code)
        print("REPONSE :", response.text)
        print("=" * 60)

        if response.status_code == 201:
            print(f"✅ Email envoyé à {to_email}")
            return True
        else:
            print(f"❌ Erreur envoi email à {to_email}: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Erreur envoi email à {to_email}: {str(e)}")
        return False


def send_email_async(to_email, subject, html_content, from_email=None):
    """Envoyer un email en tâche de fond"""
    thread = threading.Thread(
        target=send_email,
        args=(to_email, subject, html_content, from_email)
    )
    thread.daemon = True
    thread.start()
    return True


# ============================================
# EMAILS SPÉCIFIQUES
# ============================================

def send_welcome_email(employe, mot_de_passe_temp):
    """Email de bienvenue pour un nouvel employé"""
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; background-color: #f4f4f4;">
        <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h1 style="color: #2c3e50; text-align: center;">Bienvenue chez GMES Haiti 🎉</h1>

            <p>Bonjour <strong>{employe.prenom} {employe.nom}</strong>,</p>

            <p>Votre compte a été créé avec succès sur la plateforme GMES Haiti.</p>

            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin-top: 0;">📋 Vos identifiants de connexion</h3>
                <p><strong>Nom d'utilisateur :</strong> {employe.username}</p>
                <p><strong>Mot de passe :</strong> {mot_de_passe_temp}</p>
            </div>

            <p><strong>Rôle :</strong> {employe.role}</p>
            <p><strong>Fonction :</strong> {employe.fonction}</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{APP_URL}" 
                   style="background-color: #3498db; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                    🔗 Accéder à la plateforme
                </a>
            </div>

            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">

            <p style="color: #7f8c8d; font-size: 14px;">
                ⚠️ <strong>Important :</strong> Changez votre mot de passe lors de votre première connexion.
            </p>

            <p style="color: #7f8c8d; font-size: 12px; text-align: center;">
                Cet email a été envoyé automatiquement. Merci de ne pas y répondre.<br>
                © 2026 GMES Haiti - Tous droits réservés.
            </p>
        </div>
    </body>
    </html>
    """

    return send_email_async(
        to_email=employe.email,
        subject="Bienvenue sur GMES Haiti 🎉",
        html_content=html_content
    )


def send_approval_email(employe):
    """Email de confirmation d'approbation de compte"""
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; background-color: #f4f4f4;">
        <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h1 style="color: #27ae60; text-align: center;">✅ Compte approuvé</h1>

            <p>Bonjour <strong>{employe.prenom} {employe.nom}</strong>,</p>

            <p>Votre compte a été <strong style="color: #27ae60;">approuvé</strong> avec succès.</p>

            <p>Vous pouvez maintenant vous connecter à la plateforme :</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{APP_URL}" 
                   style="background-color: #27ae60; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                    🔗 Se connecter
                </a>
            </div>

            <p style="color: #7f8c8d; font-size: 12px; text-align: center;">
                © 2026 GMES Haiti - Tous droits réservés.
            </p>
        </div>
    </body>
    </html>
    """

    return send_email_async(
        to_email=employe.email,
        subject="Votre compte GMES Haiti est approuvé ✅",
        html_content=html_content
    )


def send_rejection_email(employe, motif=None):
    """Email de rejet de compte"""
    motif_text = f"<p><strong>Motif :</strong> {motif}</p>" if motif else ""

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; background-color: #f4f4f4;">
        <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h1 style="color: #e74c3c; text-align: center;">❌ Compte rejeté</h1>

            <p>Bonjour <strong>{employe.prenom} {employe.nom}</strong>,</p>

            <p>Nous regrettons de vous informer que votre demande de création de compte a été <strong style="color: #e74c3c;">rejetée</strong>.</p>

            {motif_text}

            <p>Si vous avez des questions, veuillez contacter l'administration.</p>

            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">

            <p style="color: #7f8c8d; font-size: 12px; text-align: center;">
                © 2026 GMES Haiti - Tous droits réservés.
            </p>
        </div>
    </body>
    </html>
    """

    return send_email_async(
        to_email=employe.email,
        subject="Demande de compte GMES Haiti - Rejetée ❌",
        html_content=html_content
    )


def send_password_reset_email(employe, reset_token):
    """Email de réinitialisation de mot de passe"""
    reset_link = f"{APP_URL}/reset-password/{reset_token}"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; background-color: #f4f4f4;">
        <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h1 style="color: #2c3e50; text-align: center;">🔐 Réinitialisation du mot de passe</h1>

            <p>Bonjour <strong>{employe.prenom} {employe.nom}</strong>,</p>

            <p>Vous avez demandé à réinitialiser votre mot de passe. Cliquez sur le bouton ci-dessous :</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" 
                   style="background-color: #e67e22; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                    🔑 Réinitialiser mon mot de passe
                </a>
            </div>

            <p style="color: #7f8c8d; font-size: 14px;">
                ⚠️ Ce lien expire dans 1 heure.
            </p>

            <p style="color: #7f8c8d; font-size: 12px; text-align: center;">
                Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.
            </p>
        </div>
    </body>
    </html>
    """

    return send_email_async(
        to_email=employe.email,
        subject="Réinitialisation de votre mot de passe GMES Haiti 🔑",
        html_content=html_content
    )


def send_password_reset_confirmation_email(employe):
    """Email de confirmation de changement de mot de passe"""
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; background-color: #f4f4f4;">
        <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h1 style="color: #27ae60; text-align: center;">✅ Mot de passe changé</h1>

            <p>Bonjour <strong>{employe.prenom} {employe.nom}</strong>,</p>

            <p>Votre mot de passe a été <strong style="color: #27ae60;">réinitialisé avec succès</strong>.</p>

            <p>Si vous n'êtes pas à l'origine de cette modification, contactez immédiatement l'administration.</p>

            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">

            <p style="color: #7f8c8d; font-size: 12px; text-align: center;">
                © 2026 GMES Haiti - Tous droits réservés.
            </p>
        </div>
    </body>
    </html>
    """

    return send_email_async(
        to_email=employe.email,
        subject="Confirmation - Mot de passe changé 🔐",
        html_content=html_content
    )


def send_transfer_notification_email(employe, ancienne_succursale, nouvelle_succursale):
    """Notification de transfert de succursale"""
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; background-color: #f4f4f4;">
        <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h1 style="color: #3498db; text-align: center;">🔄 Transfert de succursale</h1>

            <p>Bonjour <strong>{employe.prenom} {employe.nom}</strong>,</p>

            <p>Vous avez été transféré(e) de succursale.</p>

            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Ancienne succursale :</strong> {ancienne_succursale}</p>
                <p><strong>Nouvelle succursale :</strong> {nouvelle_succursale}</p>
            </div>

            <p style="color: #7f8c8d; font-size: 12px; text-align: center;">
                © 2026 GMES Haiti - Tous droits réservés.
            </p>
        </div>
    </body>
    </html>
    """

    return send_email_async(
        to_email=employe.email,
        subject="Transfert de succursale GMES Haiti 🔄",
        html_content=html_content
    )


