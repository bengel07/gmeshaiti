# routes/functions.py
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from database import db
from models import Employe, Client, Pret, Remboursement, Groupe

functions_bp = Blueprint('functions', __name__)


# Route dynamique principale
@functions_bp.route('/dashboard/<fonction>')
@login_required
def fonction_dashboard(fonction):
    # Vérifier si l'utilisateur a cette fonction
    if current_user.fonction != fonction:
        flash(f"Accès réservé aux {fonction.replace('_', ' ')}s", 'danger')
        return redirect(url_for('dashboard'))

    # Logique spécifique à chaque fonction
    context = {}
    template = f'functions/{fonction}.html'

    try:
        if fonction == 'caissier':
            # Logique caissier
            context['transactions'] = []  # À remplacer par votre logique
            context['solde_caisse'] = 0

        elif fonction == 'agent_credit':
            # Logique agent crédit
            context['prets_en_attente'] = Pret.query.filter_by(statut='en_attente').all()

        elif fonction == 'analyste_credit':
            # Logique analyste crédit
            context['dossiers_analyse'] = Pret.query.filter_by(statut='en_analyse').all()

        elif fonction == 'conseiller_client':
            # Logique conseiller client
            context['clients'] = Client.query.filter_by(conseiller_id=current_user.id).all()

        elif fonction == 'gestionnaire_groupe':
            # Logique gestionnaire de groupes
            context['groupes'] = Groupe.query.filter_by(gestionnaire_id=current_user.id).all()

        elif fonction == 'agent_remboursement':
            # Logique agent remboursement
            context['echeances'] = Remboursement.query.filter_by(
                statut='en_attente'
            ).all()

        elif fonction == 'agent_conformite':
            # Logique agent conformité
            context['verifications_pending'] = Client.query.filter_by(
                photo_id_verified=False
            ).all()

        elif fonction == 'chef_agence':
            # Logique chef d'agence
            context['employes'] = Employe.query.filter_by(
                succursale_id=current_user.succursale_id
            ).all()
            context['stats'] = {
                'total_clients': Client.query.filter_by(
                    succursale_id=current_user.succursale_id
                ).count(),
                'total_prets': Pret.query.filter_by(
                    succursale_id=current_user.succursale_id
                ).count(),
            }

        # Ajoutez d'autres fonctions ici...

        else:
            # Template par défaut pour les fonctions non encore implémentées
            template = 'functions/default.html'
            context['fonction'] = fonction


    except Exception as e:

        flash(f"Erreur dans la fonction {fonction}: {str(e)}", 'danger')

        return redirect(url_for('dashboard'))  # ← REDIRIGEZ VERS LE DASHBOARD AU LIEU

    # Vérifiez si le template existe avant de le rendre

    try:
        return render_template(template, **context)

    except Exception as e:
        flash(f"Interface {fonction} en développement", 'info')
        return redirect(url_for('caissier_dashboard'))


# Routes spécifiques pour certaines fonctions (optionnel)
@functions_bp.route('/caissier/transaction')
@login_required
def caissier_transaction():
    if current_user.fonction != 'caissier':
        flash("Accès réservé aux caissiers", 'danger')
        return redirect(url_for('dashboard'))
    return render_template('functions/caissier_transaction.html')


@functions_bp.route('/agent_credit/nouveau_pret')
@login_required
def agent_credit_nouveau_pret():
    if current_user.fonction != 'agent_credit':
        flash("Accès réservé aux agents de crédit", 'danger')
        return redirect(url_for('dashboard'))
    return render_template('functions/nouveau_pret.html')