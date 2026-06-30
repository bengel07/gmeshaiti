# routes/payments.py
from flask import Blueprint, jsonify, request, abort
from datetime import datetime
from database import db
from models import Transaction, Client, Remboursement
from routes.mobile_api import token_required
from utils.notifications import notification_manager

# Créer le Blueprint
payments_bp = Blueprint('payments', __name__, url_prefix='/api/payments')

# Importer token_required depuis auth (ou le définir ici)
# from routes.auth import token_required  # Assurez-vous que token_required

@app.route('/api/payments/initier', methods=['POST'])
@token_required
def initier_paiement(current_user):

    if not client.terms_accepted:
        abort(403)

    """Initie un paiement digital"""
    data = request.json

    # Validation des données
    montant = data.get('montant')
    gateway = data.get('gateway')
    pret_id = data.get('pret_id')

    if not all([montant, gateway, pret_id]):
        return jsonify({'error': 'Données manquantes'}), 400

    # Enregistrer la transaction
    transaction = Transaction(
        employe_id=current_user.id,
        pret_id=pret_id,
        montant=montant,
        gateway=gateway,
        statut='en_attente',
        date_creation=datetime.utcnow()
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        'transaction_id': transaction.id,
        'statut': 'initie'
    }), 201


@app.route('/api/payments/confirmer', methods=['POST'])
def confirmer_paiement():
    """Webhook pour confirmation de paiement"""
    data = request.json

    # Vérifier la signature (important pour la sécurité)
    transaction_id = data.get('transaction_id')
    statut = data.get('statut')

    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({'error': 'Transaction non trouvée'}), 404

    if statut == 'completed':
        transaction.statut = 'paye'
        transaction.date_confirmation = datetime.utcnow()

        # Mettre à jour le remboursement
        remboursement = Remboursement(
            pret_id=transaction.pret_id,
            client_id=transaction.employe_id,
            montant=transaction.montant,
            statut='paye',
            type_paiement=transaction.gateway,
            reference=f"{transaction.gateway}_{transaction.id}"
        )

        db.session.add(remboursement)
        db.session.commit()

        # Notifier l'utilisateur
        notification_manager.notifier_remboursement_reussi(
            Client.query.get(transaction.employe_id),
            remboursement
        )

    return jsonify({'status': 'success'})