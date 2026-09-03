from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            # Ajouter la colonne si elle n'existe pas
            db.session.execute(text("""
                ALTER TABLE transactions_caisse
                ADD COLUMN IF NOT EXISTS succursale_id INTEGER;
            """))

            db.session.commit()

            print("✅ Colonne succursale_id vérifiée/ajoutée dans transactions_caisse")

        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Erreur ajout succursale_id : {e}")