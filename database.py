import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///gmes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Créer toutes les tables si elles n'existent pas
    with app.app_context():
        db.create_all()
        print("✅ Tables créées avec succès")


