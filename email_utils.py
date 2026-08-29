  import os
import requests
import json


def send_email_via_brevo(to_email, subject, html_content, from_name="GMES Microcrédit"):
    """
    Envoie un email via l'API Brevo
    """

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "api-key": os.environ.get('BREVO_API_KEY'),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "sender": {
            "name": from_name,
            "email": "gmeshaiti@gmail.com"  # Votre email vérifié sur Brevo
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

    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)

        if response.status_code == 201:
            print(f"✅ Email envoyé avec succès à {to_email}")

            print("📧 FROM:", data["sender"]["email"])
            print("📧 TO:", to_email)

            return {"success": True, "data": response.json()}
        else:
            print(f"❌ Erreur: {response.status_code} - {response.text}")
            return {"success": False, "error": response.text, "status_code": response.status_code}

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
        return {"success": False, "error": str(e)}