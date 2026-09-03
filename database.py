from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            # Ajouter la colonne manquante si nécessaire
            db.session.execute(text("""
                ALTER TABLE transactions_caisse
                ADD COLUMN IF NOT EXISTS succursale_id INTEGER;
            """))

            db.session.commit()

            print("✅ Colonne succursale_id vérifiée")

        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Migration succursale_id : {e}")