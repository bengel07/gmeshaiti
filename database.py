from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            with db.engine.connect() as connection:
                connection.execute(text("""
                    ALTER TABLE clients
                    ADD COLUMN IF NOT EXISTS date_signature_terms TIMESTAMP
                """))
                connection.commit()

            print("✅ Colonne date_signature_terms vérifiée/créée")

        except Exception as e:
            print(f"⚠️ Impossible de créer date_signature_terms : {e}")