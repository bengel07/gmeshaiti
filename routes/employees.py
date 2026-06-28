
from flask import Blueprint, render_template
from flask_login import login_required
from models import Employe, Succursale, User
from utils.security import filtrer_par_role

employees_bp = Blueprint(
    'employees',
    __name__,
    url_prefix='/employees'
)


@employees_bp.route('/<succursale_code>')
@login_required
def list(succursale_code):
    succursale = Succursale.query.filter_by(
        code=succursale_code
    ).first_or_404()

    # CORRECTION : Filtre d'abord par succursale, puis par rôle
    employes = Employe.query.filter_by(
        succursale_id=succursale.id
    ).all()

    # Ensuite filtre par rôle
    employes = filtrer_par_role(employes, 'employe')

    return render_template(
        'employees/list.html',
        succursale=succursale,
        employes=employes
    )