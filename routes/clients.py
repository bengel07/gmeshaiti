from flask import Blueprint, render_template, request, jsonify, session, abort, redirect, url_for
from flask_login import login_required, current_user
from models import User, Transaction, Epargne
from database import db
from models import Client, Succursale
from utils.security import filtrer_par_role


clients_bp = Blueprint('clients', __name__, url_prefix='/clients')



# @clients_bp.route('/<succursale_code>')
# @login_required
# def list(succursale_code):
#
#     succursale = Succursale.query.filter_by(code=succursale_code).first_or_404()
#
#     clients = filtrer_par_role(Client).filter_by(
#         succursale_id=succursale.id
#     ).all()
#
#     return render_template(
#         'clients/list.html',
#         succursale=succursale,
#         clients=clients
#     )

@clients_bp.route('/dashboard')
@login_required
def client_dashboard():
    # Vérifier que c'est bien un client
    if not hasattr(current_user, 'role') or current_user.role != 'client':
        # Si c'est un employé/admin, rediriger vers le dashboard employé
        if hasattr(current_user, 'role') and current_user.role in ['employee', 'admin_succursale', 'admin_principal']:
            return redirect(url_for('employees.employee_dashboard'))
        abort(403, "Accès réservé aux clients")

    # Vérifier l'acceptation des termes
    if not current_user.terms_accepted:
        return redirect(url_for("terms.accept_terms_notice"))

    # Vérifier que c'est bien un client avec un compte
    if not hasattr(current_user, 'account_number'):
        abort(403, "Client sans compte bancaire")

    # Récupérer les informations du compte
    account = Epargne.query.filter_by(employe_id=current_user.id).first()
    transactions = Transaction.query.filter_by(employe_id=current_user.id) \
        .order_by(Transaction.date_created.desc()) \
        .limit(10).all()

    # Récupérer les prêts
    from models import     Pret
    loans = Pret.query.filter_by(employe_id=current_user.id).all()

    return render_template('client_portal.html',
                           account=account,
                           transactions=transactions,
                           loans=loans,
                           user=current_user)




@clients_bp.route('/profile', methods=['GET', 'PUT'])
@login_required
def profile():
    if request.method == 'PUT':
        data = request.json
        user = User.query.get(current_user.id)

        if data.get('phone'):
            user.phone = data['phone']
        if data.get('email'):
            user.email = data['email']
        if data.get('address'):
            user.address = data['address']

        session.commit()
        return jsonify({'status': 'success', 'message': 'Profil mis à jour'})

    return jsonify({
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'phone': current_user.phone,
        'email': current_user.email,
        'address': current_user.address,
        'account_number': current_user.account_number
    })


@clients_bp.route('/transactions')
@login_required
def transactions():
    page = request.args.get('page', 1, type=int)
    per_page = 20

    transactions = Transaction.query.filter_by(employe_id=current_user.id) \
        .order_by(Transaction.date_created.desc()) \
        .paginate(page=page, per_page=per_page)

    return jsonify({
        'transactions': [{
            'id': t.id,
            'type': t.type,
            'amount': t.amount,
            'method': t.method,
            'status': t.status,
            'date_created': t.date_created.isoformat()
        } for t in transactions.items],
        'total_pages': transactions.pages,
        'current_page': page
    })