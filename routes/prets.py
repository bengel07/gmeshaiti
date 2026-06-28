# from flask import Blueprint, render_template, redirect, url_for, flash
# from flask_login import login_required, current_user
# from models import Succursale, Pret
#
# prets_bp = Blueprint('prets', __name__)
#
# # TOUTES les routes prêts ici
# @prets_bp.route('/<succursale_code>/prets')  # Déplacé de app.py
# def succursale_prets(succursale_code):
#     pass
#
#
#
#
# @prets_bp.route('/<succursale_code>/prets')
# @login_required
# def list_prets(succursale_code):
#     succursale = Succursale.query.filter_by(code=succursale_code).first_or_404()
#
#     if current_user.role != 'super_admin' and current_user.succursale_id != succursale.id:
#         flash("⛔ Accès refusé", "danger")
#         return redirect(url_for('admin_dashboard'))
#
#     prets = Pret.query.filter_by(succursale_id=succursale.id).all()
#
#     return render_template(
#         "prets/list.html",
#         succursale=succursale,
#         prets=prets
#     )
#
# @prets_bp.route('/<succursale_code>/prets/ajouter', methods=['GET', 'POST'])
# @login_required
# def ajouter_pret(succursale_code):
#
#     if current_user.role not in ['super_admin', 'directeur']:
#         flash("❌ Permission refusée", "danger")
#         return redirect(request.referrer)
#
#     succursale = Succursale.query.filter_by(code=succursale_code).first_or_404()
#     clients = Client.query.filter_by(succursale_id=succursale.id).all()
#
#     if request.method == 'POST':
#         pret = Pret(
#             client_id=request.form['client_id'],
#             montant=request.form['montant'],
#             duree_mois=request.form['duree'],
#             taux_interet=request.form['taux'],
#             succursale_id=succursale.id,
#             actif=True
#         )
#         db.session.add(pret)
#         db.session.commit()
#
#         flash("✅ Prêt créé avec succès", "success")
#         return redirect(url_for('prets.list_prets', succursale_code=succursale.code))
#
#     return render_template("prets/ajouter.html", succursale=succursale, clients=clients)
#
# # ... toutes les autres routes prêts

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Succursale, Pret, Client, db

prets_bp = Blueprint('prets', __name__, url_prefix='/prets')

# Route pour lister les prêts d'une succursale
@prets_bp.route('/<succursale_code>/prets')
@login_required
def list_prets(succursale_code):
    """Liste des prêts d'une succursale"""
    succursale = Succursale.query.filter_by(code=succursale_code).first_or_404()

    # Vérification des permissions
    if current_user.role != 'super_admin' and current_user.succursale_id != succursale.id:
        flash("⛔ Accès refusé", "danger")
        return redirect(url_for('admin_dashboard'))

    # Récupération des prêts
    prets = Pret.query.filter_by(succursale_id=succursale.id).all()

    return render_template(
        "prets/list.html",
        succursale=succursale,
        prets=prets
    )

# Route pour ajouter un nouveau prêt
@prets_bp.route('/<succursale_code>/prets/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_pret(succursale_code):
    """Ajouter un nouveau prêt"""
    # Vérification des permissions
    if current_user.role not in ['super_admin', 'directeur']:
        flash("❌ Permission refusée", "danger")
        return redirect(request.referrer or url_for('prets.list_prets', succursale_code=succursale_code))

    succursale = Succursale.query.filter_by(code=succursale_code).first_or_404()
    clients = Client.query.filter_by(succursale_id=succursale.id).all()

    if request.method == 'POST':
        # Création du prêt
        pret = Pret(
            client_id=request.form['client_id'],
            montant=request.form['montant'],
            duree_mois=request.form['duree'],
            taux_interet=request.form['taux'],
            succursale_id=succursale.id,
            actif=True
        )
        db.session.add(pret)
        db.session.commit()

        flash("✅ Prêt créé avec succès", "success")
        return redirect(url_for('prets.list_prets', succursale_code=succursale.code))

    return render_template("prets/ajouter.html", succursale=succursale, clients=clients)