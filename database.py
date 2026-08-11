from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            # Augmenter la taille des statuts
            db.session.execute(text("""
                ALTER TABLE clients
                ALTER COLUMN statut TYPE VARCHAR(100)
            """))

            db.session.execute(text("""
                ALTER TABLE users
                ALTER COLUMN statut TYPE VARCHAR(100)
            """))

            db.session.commit()

            print("✅ Colonnes statut mises à jour : VARCHAR(100)")

        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Migration statut : {e}")