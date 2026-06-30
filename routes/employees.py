
from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user

from database import db
from models import Employe, Succursale, User
from sqlalchemy import or_
# from app import db

from utils.security import filtrer_par_role

employees_bp = Blueprint(
    'employees',
    __name__,
    url_prefix='/employees'
)



@employees_bp.route('/<succursale_code>')
@login_required
def list(succursale_code):

    # =========================
    # SUCCURSALE
    # =========================

    succursale = Succursale.query.filter_by(
        code=succursale_code
    ).first_or_404()

    # =========================
    # FILTRES
    # =========================

    statut = request.args.get('statut', '').strip()
    habilitation = request.args.get('habilitation', '').strip()
    search = request.args.get('search', '').strip()

    # =========================
    # QUERY USERS
    # =========================

    users_query = User.query.filter(
        User.succursale_id == succursale.id
    ).filter(
        User.role != 'client'
    )

    # ---------- FILTRE STATUT ----------
    if statut:
        users_query = users_query.filter(
            User.statut == statut
        )

    # ---------- FILTRE HABILITATION ----------
    if habilitation:
        users_query = users_query.filter(
            User.niveau_habilitation == int(habilitation)
        )

    # ---------- RECHERCHE ----------
    if search:

        search_term = f"%{search}%"

        users_query = users_query.filter(
            or_(

                # Nom
                User.nom.ilike(search_term),

                # Prénom
                User.prenom.ilike(search_term),

                # Nom complet
                (
                    db.func.coalesce(User.prenom, '') +
                    ' ' +
                    db.func.coalesce(User.nom, '')
                ).ilike(search_term),

                # Email
                User.email.ilike(search_term),

                # Téléphone
                User.telephone.ilike(search_term),

                # Username
                User.username.ilike(search_term),

                # Matricule
                User.matricule.ilike(search_term)
            )
        )

    # EXÉCUTION QUERY USERS
    users_employes = users_query.all()

    # =========================
    # QUERY EMPLOYES
    # =========================

    employes_query = Employe.query.filter_by(
        succursale_id=succursale.id
    )

    # ---------- FILTRE STATUT ----------
    if statut:
        employes_query = employes_query.filter(
            Employe.statut == statut
        )

    # ---------- FILTRE HABILITATION ----------
    if habilitation and hasattr(Employe, 'niveau_habilitation'):

        employes_query = employes_query.filter(
            Employe.niveau_habilitation == int(habilitation)
        )

    # ---------- RECHERCHE ----------
    if search:

        search_term = f"%{search}%"

        employes_query = employes_query.filter(
            or_(

                # Nom
                Employe.nom.ilike(search_term),

                # Prénom
                Employe.prenom.ilike(search_term),

                # Email
                Employe.email.ilike(search_term),

                # Téléphone
                Employe.telephone.ilike(search_term),

                # Matricule
                Employe.matricule.ilike(search_term)
            )
        )

    # EXÉCUTION QUERY EMPLOYES
    employes_table = employes_query.all()

    # =========================
    # FUSION
    # =========================

    employes = users_employes + employes_table

    # =========================
    # POSTES AUTORISÉS
    # =========================

    postes_autorises = len(set([
        getattr(emp, 'role', 'employe')
        for emp in employes
        if getattr(emp, 'role', None)
    ]))

    # =========================
    # TEMPLATE
    # =========================

    return render_template(
        'employees/list.html',
        succursale=succursale,
        employees=employes,
        postes_autorises=postes_autorises
    )





# Dans ton blueprint pour les succursales ou employés
@employees_bp.route('/<branch_code>/dashboard')
@login_required
def branch_dashboard(branch_code):
    # Vérifier que l'utilisateur est un admin_succursale
    if not hasattr(current_user, 'role') or current_user.role != 'admin_succursale':
        # Rediriger les autres rôles vers leurs dashboards respectifs
        if current_user.role == 'super_admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'client':
            return redirect(url_for('clients.client_dashboard'))
        elif current_user.role == 'employee':
            return redirect(url_for('employees.employee_dashboard'))
        else:
            abort(403)

    # Vérifier que l'admin a accès à cette succursale spécifique
    if not hasattr(current_user, 'branch_code'):
        abort(403, "Admin sans succursale affectée")

    if current_user.branch_code != branch_code:
        abort(403, f"Accès non autorisé à la succursale {branch_code}")

    # DEBUG
    print(f"=== DEBUG BRANCH DASHBOARD ===")
    print(f"Admin: {current_user.username}")
    print(f"Succursale demandée: {branch_code}")
    print(f"Succursale admin: {current_user.branch_code}")

    # Récupérer les statistiques de LA SUCCURSALE SPÉCIFIQUE
    from models import User, Pret, Transaction

    # Compter seulement les clients de cette succursale
    total_clients = Client.query.filter_by(branch_code=branch_code, role='client').count()

    # Prêts en attente de cette succursale
    pending_loans = Pret.query.join(User).filter(
        User.branch_code == branch_code,
        Pret.status == 'pending'
    ).count()

    # Transactions en attente de cette succursale
    pending_transactions = Transaction.query.join(User).filter(
        User.branch_code == branch_code,
        Transaction.status == 'pending'
    ).count()

    return render_template('branch_dashboard.html',
                           branch_code=branch_code,
                           total_clients=total_clients,
                           pending_loans=pending_loans,
                           pending_transactions=pending_transactions,
                           user=current_user)


