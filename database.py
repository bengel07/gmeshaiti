from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():

        # Créer les tables si elles n'existent pas
        db.create_all()
        print("✅ Tables vérifiées/créées")

        # =========================================================
        # CORRECTION POSTGRESQL POUR LES EMPLOYÉS
        # =========================================================
        try:
            db.session.execute(text("""
                ALTER TABLE users
                ALTER COLUMN client_id DROP NOT NULL
            """))

            db.session.execute(text("""
                ALTER TABLE users
                ALTER COLUMN succursale_id DROP NOT NULL
            """))

            db.session.commit()

            print("✅ users.client_id = NULL autorisé")
            print("✅ users.succursale_id = NULL autorisé")

        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Correction structure users : {e}")