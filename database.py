from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()

        try:
            db.session.execute(text("""
                ALTER TABLE retraits_attente
                ADD COLUMN IF NOT EXISTS client_signature TEXT
            """))

            db.session.execute(text("""
                ALTER TABLE retraits_attente
                ADD COLUMN IF NOT EXISTS transaction_id INTEGER
            """))

            db.session.commit()

            print("✅ Colonnes client_signature et transaction_id vérifiées")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur modification retraits_attente : {e}")