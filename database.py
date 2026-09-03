from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            db.session.commit()
            print("✅ Connexion PostgreSQL réussie")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur connexion PostgreSQL : {e}")