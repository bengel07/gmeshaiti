from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):

    db.init_app(app)

    with app.app_context():

        try:
            migrations = [

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

            for sql in migrations:
                db.session.execute(text(sql))

            db.session.commit()

            print("✅ Migration signature prêt terminée")

        except Exception as e:
            db.session.rollback()
            print("⚠️ Erreur migration signature prêt :", e)