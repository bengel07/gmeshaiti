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

            db.session.commit()

            print("✅ client_signature vérifiée/ajoutée dans retraits_attente")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur ajout client_signature : {e}")