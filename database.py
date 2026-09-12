from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

        try:
            db.session.execute(text("""
                ALTER TABLE remboursements
                DROP CONSTRAINT IF EXISTS remboursements_client_id_fkey
            """))

            db.session.execute(text("""
                ALTER TABLE remboursements
                ADD CONSTRAINT remboursements_client_id_fkey
                FOREIGN KEY (client_id) REFERENCES clients(id)
            """))

            db.session.commit()
            print("✅ FK remboursements.client_id corrigée vers clients.id")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur correction FK remboursements : {e}")
