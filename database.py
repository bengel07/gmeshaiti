from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        # Créer les tables si elles n'existent pas
        db.create_all()

        # Ajouter client_signature si la colonne n'existe pas
        try:
            db.session.execute(text("""
                ALTER TABLE retrait_attente
                ADD COLUMN IF NOT EXISTS client_signature TEXT
            """))
            db.session.commit()

            print("✅ Colonne client_signature vérifiée/ajoutée")

        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Erreur ajout client_signature : {e}")