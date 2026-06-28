# routes/accueil.py - CORRIGÉ
from flask import Blueprint, render_template

accueil_bp = Blueprint("main", __name__, url_prefix='/accueil')

@accueil_bp.route("/")
def accueil():
    # Déplacer l'import ICI - à l'intérieur de la fonction
    from utils.stats import get_stats_dashboard
    stats = get_stats_dashboard()
    return render_template("accueil.html", stats=stats)