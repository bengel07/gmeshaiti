from sqlalchemy import text
from app import app
from database import db


def update_prets_signature():

    with app.app_context():

        try:
            requetes = [

                """
                ALTER TABLE prets
                ADD COLUMN IF NOT EXISTS conditions_acceptees BOOLEAN DEFAULT FALSE;
                """,

                """
                ALTER TABLE prets
                ADD COLUMN IF NOT EXISTS date_signature TIMESTAMP;
                """,

                """
                ALTER TABLE prets
                ADD COLUMN IF NOT EXISTS signature_client TEXT;
                """,

                """
                ALTER TABLE prets
                ADD COLUMN IF NOT EXISTS ip_signature VARCHAR(100);
                """
            ]

            for req in requetes:
                db.session.execute(text(req))
                print("✅ OK")

            db.session.commit()

            print("🎉 Migration signature prêt terminée")

        except Exception as e:
            db.session.rollback()
            print("❌ Erreur :", e)


update_prets_signature()