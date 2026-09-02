
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

            db.create_all()

            # Ajouter client_id à users si elle n'existe pas
            db.session.execute(text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS client_id INTEGER
            """))
            db.session.commit()

            print("✅ Colonne users.client_id vérifiée/créée")
            print("✅ Tables vérifiées/créées")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur base de données : {e}")
            raise
