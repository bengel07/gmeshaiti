
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            # Ajouter user_id à la table clients si la colonne n'existe pas
            db.session.execute(text("""
                ALTER TABLE clients
                ADD COLUMN IF NOT EXISTS user_id INTEGER;
            """))

            # Ajouter la clé étrangère vers users.id si elle n'existe pas
            db.session.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conname = 'fk_clients_user_id_users'
                    ) THEN
                        ALTER TABLE clients
                        ADD CONSTRAINT fk_clients_user_id_users
                        FOREIGN KEY (user_id)
                        REFERENCES users(id);
                    END IF;
                END $$;
            """))

            # Un employé ne peut être lié qu'à un seul profil client
            db.session.execute(text("""
                CREATE UNIQUE INDEX IF NOT EXISTS ix_clients_user_id_unique
                ON clients(user_id)
                WHERE user_id IS NOT NULL;
            """))

            db.session.commit()

            print("✅ Colonne clients.user_id vérifiée/ajoutée")

        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Erreur ajout clients.user_id : {e}")

