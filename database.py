from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():

        # Création normale des tables manquantes
        db.create_all()

        try:
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS system_migrations (
                    id SERIAL PRIMARY KEY,
                    migration_name VARCHAR(200) UNIQUE NOT NULL,
                    date_execution TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))

            db.session.commit()

            migration = db.session.execute(text("""
                SELECT id
                FROM system_migrations
                WHERE migration_name = 'documents_v1'
            """)).fetchone()

            if not migration:

                print("🔧 Exécution migration documents_v1...")

                db.session.execute(text("""
                    ALTER TABLE documents
                    ADD COLUMN IF NOT EXISTS statut VARCHAR(20)
                    DEFAULT 'reçu'
                    NOT NULL
                """))

                db.session.execute(text("""
                    ALTER TABLE documents
                    ADD COLUMN IF NOT EXISTS demande_item_id INTEGER
                """))

                db.session.execute(text("""
                    CREATE TABLE IF NOT EXISTS demande_documents (
                        id SERIAL PRIMARY KEY,
                        client_id INTEGER NOT NULL,
                        employe_id INTEGER NOT NULL,
                        token VARCHAR(100) UNIQUE NOT NULL,
                        message TEXT,
                        statut VARCHAR(30) NOT NULL DEFAULT 'en attente',
                        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        date_envoi TIMESTAMP NULL,
                        date_completion TIMESTAMP NULL
                    )
                """))

                db.session.execute(text("""
                    CREATE TABLE IF NOT EXISTS demande_documents_items (
                        id SERIAL PRIMARY KEY,
                        demande_id INTEGER NOT NULL,
                        type_document VARCHAR(50) NOT NULL,
                        categorie VARCHAR(30) DEFAULT 'identite',
                        description VARCHAR(255),
                        statut VARCHAR(30) NOT NULL DEFAULT 'en attente',
                        date_reception TIMESTAMP NULL,
                        date_verification TIMESTAMP NULL,
                        commentaire TEXT
                    )
                """))

                db.session.execute(text("""
                    INSERT INTO system_migrations (migration_name)
                    VALUES ('documents_v1')
                """))

                db.session.commit()

                print("✅ Migration documents_v1 terminée.")

            else:
                print("ℹ️ Migration documents_v1 déjà exécutée.")

        except Exception as e:
            db.session.rollback()
            print("❌ Erreur init_db :", e)