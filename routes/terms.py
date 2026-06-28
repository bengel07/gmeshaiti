from flask import Blueprint, request, render_template
from datetime import datetime
from database import db
from models import Client
from utils.notifications import notification_manager

terms_bp = Blueprint('terms', __name__, url_prefix='/terms')


@terms_bp.route('/accept/<token>', methods=['GET', 'POST'])
def accept_terms(token):

    print("=" * 50)
    print(f"📍 Route accept_terms appelée")
    print(f"📝 Méthode: {request.method}")
    print(f"🔗 Token reçu: {token[:20]}...")

    client_id = notification_manager._verify_terms_token(token)
    print(f"👤 Client ID extrait: {client_id}")

    if not client_id:
        return render_template("terms_invalid.html"), 400

    client = db.session.get(Client, client_id)
    if not client:
        return render_template("terms_invalid.html"), 404


    # Déjà accepté
    if client.terms_accepted:
        print(f"ℹ️ Client {client.email} avait déjà accepté")
        return render_template("terms_already_accepted.html", client=client)

    # Validation volontaire (POST)
    if request.method == "POST":
        client.terms_accepted = True
        client.terms_accepted_at = datetime.utcnow()

        # Preuve électronique
        client.terms_signature_ip = request.remote_addr
        client.terms_signature_user_agent = request.headers.get("User-Agent")

        db.session.commit()

        from models import Pret
        from app import notifier_directeurs_demande_pret

        pret_en_attente = Pret.query.filter_by(client_id=client.id, statut='en_attente').first()

        if pret_en_attente:
            # Notifier le directeur que le client a accepté
            notifier_directeurs_demande_pret(pret_en_attente)
            print(f"✅ Directeur notifié pour le prêt #{pret_en_attente.id}")
        else:
            print(f"ℹ️ Aucun prêt en attente trouvé pour le client {client.id}")

        return render_template("terms_success.html", client=client)

    # Lecture des CGU (GET)
    return render_template("terms.html", client=client)
