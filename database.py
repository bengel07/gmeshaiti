from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            with db.engine.connect() as conn:
                conn.execute(text("""
                    ALTER TABLE transactions_caisse
                    ADD COLUMN IF NOT EXISTS succursale_id INTEGER
                    REFERENCES succursales(id)
                """))
                conn.commit()

            print("✅ Vérification de la colonne succursale_id terminée")

        except Exception as e:
            print(f"⚠️ Erreur lors de l'ajout de succursale_id : {e}")