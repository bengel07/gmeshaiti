# super_admin_bp.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from views import PAGES, super_admin_required

# Création du blueprint
super_admin_bp = Blueprint('super_admin', __name__, url_prefix='/super_admin')


# =============================================
# ROUTE : PAGE SUPER ADMIN SWITCHER
# =============================================
@super_admin_bp.route('')
@super_admin_required
def switcher():
    """Page principale Super Admin"""
    return render_template('super_admin_switcher.html',
                           pages=PAGES,
                           total_pages=len(PAGES),
                           username=session.get('user'),
                           role=session.get('role'))


# =============================================
# ROUTE : REDIRECTION VERS LA PAGE CHOISIE
# =============================================
@super_admin_bp.route('/go', methods=['GET', 'POST'])
@super_admin_required
def go():
    """Redirige vers la page sélectionnée"""
    # 🔥 Correction : Récupérer depuis args pour GET et form pour POST
    if request.method == 'GET':
        page_key = request.args.get('page_key')
    else:
        page_key = request.form.get('page_key')

    # Alternative plus simple (mais moins claire)
    # page_key = request.values.get('page_key')  # Récupère des deux

    print(f"🔍 Méthode: {request.method}")  # Debug
    print(f"🔍 Page key: {page_key}")  # Debug

    if not page_key:
        flash('❌ Aucune page sélectionnée.', 'warning')
        return redirect(url_for('super_admin.switcher'))

    if page_key not in PAGES:
        flash('❌ Page inconnue.', 'danger')
        return redirect(url_for('super_admin.switcher'))

    endpoint = PAGES[page_key]['endpoint']
    page_name = PAGES[page_key]['name']
    print(f"🔍 Endpoint: {endpoint}")  # Debug

    try:
        # Vérifier si l'endpoint existe
        from flask import current_app
        if endpoint not in current_app.view_functions:
            # Rediriger vers la page de construction
            flash(f'🚧 La page "{page_name}" est en construction.', 'info')
            return redirect(url_for('page_en_construction', page_name=page_name))
        if endpoint == "voir_client":
            flash("⚠️ Veuillez d'abord sélectionner un client.", "warning")
            return redirect(url_for("liste_clients"))

        if endpoint == "voir_dossiers":
            return redirect(url_for("liste_dossiers"))

        return redirect(url_for(endpoint))
    except Exception as e:
        flash(f'🚧 La page "{page_name}" est en cours de développement.', 'info')
        return redirect(url_for('page_en_construction', page_name=page_name))


# =============================================
# ROUTE : ACCÈS DIRECT (raccourci)
# =============================================
@super_admin_bp.route('/go/<page_key>')
@super_admin_required
def quick_access(page_key):
    """Accès direct via URL : /super_admin/go/dashboard"""
    if page_key not in PAGES:
        flash('❌ Page inconnue.', 'danger')
        return redirect(url_for('super_admin.switcher'))

    endpoint = PAGES[page_key]['endpoint']
    page_name = PAGES[page_key]['name']

    try:
        from flask import current_app
        if endpoint not in current_app.view_functions:
            flash(f'🚧 La page "{page_name}" est en construction.', 'info')
            return redirect(url_for('page_en_construction', page_name=page_name))

        if endpoint == "voir_client":
            flash("⚠️ Veuillez d'abord sélectionner un client.", "warning")
            return redirect(url_for("liste_clients"))

        if endpoint == "voir_dossiers":
            return redirect(url_for("liste_dossiers"))

        return redirect(url_for(endpoint))
    except Exception:
        flash(f'🚧 La page "{page_name}" est en cours de développement.', 'info')
        return redirect(url_for('page_en_construction', page_name=page_name))


# =============================================
# ROUTE : LISTE DES PAGES EN JSON
# =============================================
@super_admin_bp.route('/pages.json')
@super_admin_required
def pages_json():
    """Retourne la liste de toutes les pages en JSON"""
    return jsonify(PAGES)



