# services/partner_service.py
from database import db
from models import Partner, PartnerAPIKey, PartnerWebhook, PartnerIntegration
import secrets
import hashlib
import uuid
import secrets
import hashlib
import hmac
import json
import requests
from datetime import datetime, timedelta
from flask import current_app
import uuid




class PartnerService:

    @staticmethod
    def verify_api_key(client_id, client_secret):
        from models import PartnerAPIKey
        """Vérifier les identifiants API"""
        api_key = PartnerAPIKey.query.filter_by(client_id=client_id, is_active=True).first()

        if not api_key:
            return None

        # Vérifier expiration
        if api_key.expires_at and api_key.expires_at < datetime.utcnow():
            return None

        # Vérifier secret (support des deux formats de hash)
        secret_hashed = hashlib.sha256(client_secret.encode()).hexdigest()

        if api_key.client_secret == secret_hashed or api_key.client_secret == client_secret:
            # Mettre à jour dernière utilisation
            api_key.last_used_at = datetime.utcnow()
            api_key.requests_count += 1
            api_key.daily_requests += 1
            db.session.commit()
            return api_key

        return None

    @staticmethod
    def trigger_webhook(partner_id, event, payload):
        """Déclencher un webhook pour un partenaire"""
        webhooks = PartnerWebhook.query.filter_by(partner_id=partner_id, is_active=True).all()

        for webhook in webhooks:
            if event in webhook.events:
                try:
                    signature = hmac.new(
                        webhook.secret.encode(),
                        json.dumps(payload).encode(),
                        hashlib.sha256
                    ).hexdigest()

                    response = requests.post(
                        webhook.url,
                        json={
                            'event': event,
                            'timestamp': datetime.utcnow().isoformat(),
                            'data': payload
                        },
                        headers={'X-GmesPay-Signature': signature},
                        timeout=5
                    )

                    webhook.last_triggered_at = datetime.utcnow()
                    if response.status_code >= 400:
                        webhook.failed_attempts += 1

                except Exception as e:
                    webhook.failed_attempts += 1
                    current_app.logger.error(f"Webhook failed: {str(e)}")

        db.session.commit()