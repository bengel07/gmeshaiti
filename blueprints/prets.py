# from flask import Blueprint, render_template
# from flask_login import login_required
#
# prets_bp = Blueprint(
#     'prets',
#     __name__,
#     url_prefix='/succursales'
# )
#
# @prets_bp.route('/<succursale_code>/prets')
# @login_required
# def list_prets(succursale_code):
#     return render_template(
#         'prets/list.html',
#         succursale_code=succursale_code
#     )
