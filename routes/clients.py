import secrets
from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, jsonify, session, abort, redirect, url_for, flash
from flask_login import login_required, current_user, login_user
from werkzeug.security import generate_password_hash

from models import User, Transaction, Epargne, TransactionEpargne, Pret
from database import db
from models import Client, Succursale
from utils.security import filtrer_par_role


clients_bp = Blueprint('clients', __name__, url_prefix='/clients')





@clients_bp.route('/dashboard')
@login_required
def client_dashboard():

    # Vérifier que c'est bien un client
    if current_user.role != 'client':
        if current_user.role in [
            'employee',
            'admin_succursale',
            'admin_principal'
        ]:
            return redirect(url_for('employees.employee_dashboard'))

        abort(403, "Accès réservé aux clients")

    # Récupérer le profil Client lié au User
    client = Client.query.filter_by(
        id=current_user.client_id
    ).first()

    if not client:
        abort(403, "Profil client introuvable")

    # Vérifier l'acceptation des termes
    if not current_user.terms_accepted:
        return redirect(url_for("terms.accept_terms_notice"))

    # Récupérer les comptes d'épargne du client
    accounts = Epargne.query.filter_by(
        client_id=client.id
    ).all()

    # Premier compte pour compatibilité avec ton template actuel
    account = accounts[0] if accounts else None

    # Transactions d'épargne du client
    from models import TransactionEpargne, Pret

    transactions = TransactionEpargne.query.join(
        Epargne,
        TransactionEpargne.compte_id == Epargne.id
    ).filter(
        Epargne.client_id == client.id
    ).order_by(
        TransactionEpargne.date_transaction.desc()
    ).limit(10).all()

    # Prêts du client
    loans = Pret.query.filter_by(
        client_id=client.id
    ).all()

    return render_template(
        'client_portal.html',
        account=account,
        accounts=accounts,
        transactions=transactions,
        loans=loans,
        client=client,
        user=current_user
    )




@clients_bp.route('/profile', methods=['GET', 'PUT'])
@login_required
def profile():

    client = Client.query.filter_by(
        id=current_user.client_id
    ).first()

    if not client:
        return jsonify({
            'status': 'error',
            'message': 'Profil client introuvable'
        }), 404

    if request.method == 'PUT':

        data = request.get_json() or {}

        if data.get('telephone'):
            current_user.telephone = data['telephone']

        if data.get('email'):
            current_user.email = data['email']
            client.email = data['email']

        if data.get('adresse'):
            current_user.adresse = data['adresse']
            client.adresse = data['adresse']

        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Profil mis à jour'
        })

    return jsonify({
        'id_client': client.id_client,
        'first_name': current_user.prenom,
        'last_name': current_user.nom,
        'phone': current_user.telephone,
        'email': current_user.email,
        'address': current_user.adresse,
        'account_number': client.numero_compte
    })

@clients_bp.route('/transactions')
@login_required
def transactions():

    if current_user.role != 'client':
        abort(403)

    client = Client.query.filter_by(
        id=current_user.client_id
    ).first()

    if not client:
        abort(403, "Profil client introuvable")

    from models import TransactionEpargne

    page = request.args.get('page', 1, type=int)
    per_page = 20

    transactions = TransactionEpargne.query.join(
        Epargne,
        TransactionEpargne.compte_id == Epargne.id
    ).filter(
        Epargne.client_id == client.id
    ).order_by(
        TransactionEpargne.date_transaction.desc()
    ).paginate(
        page=page,
        per_page=per_page
    )

    return jsonify({
        'transactions': [{
            'id': t.id,
            'type': t.type_transaction,
            'amount': float(t.montant),
            'status': 'effectue',
            'date_created': t.date_transaction.isoformat()
            if t.date_transaction else None
        } for t in transactions.items],
        'total_pages': transactions.pages,
        'current_page': page
    })


@clients_bp.route('/activation/<token>', methods=['GET', 'POST'])
def activation_client(token):

    user = User.query.filter_by(
        activation_token=token,
        role='client'
    ).first()

    if not user:
        flash(
            "❌ Le lien d'activation est invalide ou n'existe plus.",
            "danger"
        )
        return redirect(url_for('index'))

    # Vérifier expiration
    if (
        not user.activation_expiration
        or datetime.utcnow() > user.activation_expiration
    ):
        flash(
            "⏰ Ce lien d'activation a expiré. "
            "Veuillez demander un nouveau lien.",
            "danger"
        )
        return render_template(
            'client_activation.html',
            user=user,
            expired=True
        )

    client = Client.query.filter_by(
        id=user.client_id
    ).first()

    if not client:
        flash(
            "❌ Profil client introuvable.",
            "danger"
        )
        return redirect(url_for('index'))

    # Si le compte est déjà activé
    if user.statut == 'actif' and user.actif:
        flash(
            "ℹ️ Votre compte est déjà activé. "
            "Vous pouvez vous connecter.",
            "info"
        )
        return redirect(url_for('login'))

    if request.method == 'POST':

        password = request.form.get('password', '').strip()
        password_confirm = request.form.get(
            'password_confirm',
            ''
        ).strip()

        # Vérification
        if not password:
            flash(
                "❌ Veuillez créer un mot de passe.",
                "danger"
            )
            return render_template(
                'client_activation.html',
                user=user,
                client=client,
                token=token
            )

        if len(password) < 8:
            flash(
                "❌ Le mot de passe doit contenir au moins 8 caractères.",
                "danger"
            )
            return render_template(
                'client_activation.html',
                user=user,
                client=client,
                token=token
            )

        if password != password_confirm:
            flash(
                "❌ Les deux mots de passe ne correspondent pas.",
                "danger"
            )
            return render_template(
                'client_activation.html',
                user=user,
                client=client,
                token=token
            )

        try:

            # Créer le mot de passe
            user.password_hash = generate_password_hash(password)

            # Activer le compte
            user.statut = 'actif'
            user.actif = True
            user.est_actif = True

            # Confirmer l'email
            user.email = client.email
            client.email_confirme = True
            client.date_confirmation_email = datetime.utcnow()

            # Supprimer le token
            user.activation_token = None
            user.activation_expiration = None

            db.session.commit()

            # Connecter automatiquement le client
            login_user(user)

            flash(
                "✅ Votre compte a été activé avec succès.",
                "success"
            )

            # Ton dashboard existant
            return redirect(
                url_for('clients.client_dashboard')
            )

        except Exception as e:

            db.session.rollback()

            print(
                f"❌ ERREUR ACTIVATION CLIENT : {str(e)}"
            )

            flash(
                "❌ Une erreur est survenue lors de l'activation.",
                "danger"
            )

    return render_template(
        'client_activation.html',
        user=user,
        client=client,
        token=token
    )

def creer_acces_client(client):

    # Vérifier email
    if not client.email:
        raise ValueError(
            "Le client doit avoir une adresse email."
        )

    # Vérifier si User existe déjà
    user = User.query.filter_by(
        client_id=client.id
    ).first()

    # Si aucun User, créer
    if not user:

        user = User(
            username=client.email,
            email=client.email,
            nom=client.nom,
            prenom=client.prenom,
            nom_complet=client.nom_complet,
            telephone=client.telephone,
            role='client',
            statut='en_attente',
            actif=False,
            est_actif=False,
            terms_accepted=False,
            client_id=client.id
        )

        db.session.add(user)
        db.session.flush()

    else:

        user.email = client.email
        user.username = client.email
        user.role = 'client'
        user.client_id = client.id
        user.statut = 'en_attente'
        user.actif = False
        user.est_actif = False

    # ==============================
    # Générer le token
    # ==============================

    token = secrets.token_urlsafe(48)

    user.activation_token = token

    user.activation_expiration = (
        datetime.utcnow() + timedelta(hours=24)
    )

    db.session.commit()

    # ==============================
    # Créer le lien
    # ==============================

    activation_link = url_for(
        'clients.activation_client',
        token=token,
        _external=True
    )

    return activation_link