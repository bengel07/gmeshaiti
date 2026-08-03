from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):

    db.init_app(app)

    def corriger_colonnes_prets():

        try:
            print("🔧 Vérification colonnes prêts")

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

            with app.app_context():

                for req in requetes:
                    try:
                        db.session.execute(text(req))
                        print("✅ Migration OK")
                    except Exception as e:
                        print("⚠️ Déjà existant :", e)

                db.session.commit()

        except Exception as e:
            db.session.rollback()
            print("❌ Migration erreur :", e)


    # si tu veux lancer automatiquement
    # corriger_colonnes_prets()