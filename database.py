from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    def corriger_fk_terms_acceptance():
        """Corrige la clé étrangère terms_acceptance.client_id -> clients.id"""

        if db.engine.dialect.name != "postgresql":
            print("ℹ️ SQLite détecté, correction FK ignorée.")
            return

        try:
            db.session.execute(text("""
                ALTER TABLE terms_acceptance
                DROP CONSTRAINT IF EXISTS terms_acceptance_client_id_fkey;
            """))

            db.session.execute(text("""
                ALTER TABLE terms_acceptance
                ADD CONSTRAINT terms_acceptance_client_id_fkey
                FOREIGN KEY (client_id)
                REFERENCES clients(id)
                ON DELETE CASCADE;
            """))

            db.session.commit()
            print("✅ FK terms_acceptance corrigée vers clients.id")

        except Exception as e:
            db.session.rollback()
            print(f"ℹ️ FK terms_acceptance déjà correcte ou erreur : {e}")

    with app.app_context():
        db.create_all()


        # IMPORTANT
        corriger_fk_terms_acceptance()

        print("✅ Tables vérifiées/créées")

