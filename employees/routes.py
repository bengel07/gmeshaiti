from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import Employe, User, Loan, Transaction, Account, Client
from database import db

employees_bp = Blueprint('employees', __name__, url_prefix='/employees')


@employees_bp.route('/dashboard')
@login_required
def employe_dashboard():
    # Vérifier que c'est bien un employé/admin
    if not hasattr(current_user, 'role'):
        abort(403, "Accès réservé au personnel")

    # Si c'est un client, rediriger vers le dashboard client
    if current_user.role == 'client':
        return redirect(url_for('clients.dashboard'))

    # Vérifier l'acceptation des termes (pour tous les utilisateurs)
    if not current_user.terms_accepted:
        return redirect(url_for("terms.accept_terms_notice"))

    # Statistiques pour le tableau de bord employé/admin
    total_clients = Client.query.count()
    pending_loans = Loan.query.filter_by(status='pending').count()
    pending_transactions = Transaction.query.filter_by(status='pending').count()

    # Selon le rôle, utiliser un template différent
    if current_user.role in ['admin_succursale', 'admin_principal']:
        template = 'admin_dashboard.html'
    else:
        template = 'employe_dashboard.html'

    return render_template(template,
                           total_clients=total_clients,
                           pending_loans=pending_loans,
                           pending_transactions=pending_transactions,
                           user=current_user)

@employees_bp.route('/clients')
@login_required
def manage_clients():
    page = request.args.get('page', 1, type=int)
    per_page = 20

    clients = User.query.paginate(page=page, per_page=per_page)

    return jsonify({
        'clients': [{
            'id': client.id,
            'account_number': client.account_number,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'email': client.email,
            'phone': client.phone,
            'is_approved': client.is_approved
        } for client in clients.items],
        'total_pages': clients.pages,
        'current_page': page
    })


@employees_bp.route('/approve_client/<int:client_id>', methods=['POST'])
@login_required
def approve_client(client_id):
    client = User.query.get_or_404(client_id)
    client.is_approved = True

    # Envoyer une notification au client
    from utils.notifications import send_account_approval_notification
    send_account_approval_notification(client)

    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Client approuvé'})


@employees_bp.route('/process_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def process_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    action = request.json.get('action')  # 'approve' or 'reject'

    if action == 'approve':
        transaction.status = 'completed'
        transaction.processed_by = current_user.id

        # Mettre à jour le solde du compte
        account = Account.query.filter_by(employe_id=transaction.employe_id).first()
        if transaction.type == 'deposit':
            account.balance += transaction.amount
        elif transaction.type == 'withdrawal':
            account.balance -= transaction.amount

    elif action == 'reject':
        transaction.status = 'rejected'
        transaction.processed_by = current_user.id

    db.session.commit()

    return jsonify({'status': 'success', 'message': f'Transaction {action}ée'})
