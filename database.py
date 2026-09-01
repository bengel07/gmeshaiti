from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            with db.engine.begin() as conn:

                # succursale_id
                conn.execute(text("""
                    ALTER TABLE transactions_caisse
                    ADD COLUMN IF NOT EXISTS succursale_id INTEGER
                """))

                # Clé étrangère succursale
                conn.execute(text("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1
                            FROM pg_constraint
                            WHERE conname = 'fk_transactions_caisse_succursale'
                        ) THEN
                            ALTER TABLE transactions_caisse
                            ADD CONSTRAINT fk_transactions_caisse_succursale
                            FOREIGN KEY (succursale_id)
                            REFERENCES succursale(id);
                        END IF;
                    END
                    $$;
                """))

                # employe_id
                conn.execute(text("""
                    ALTER TABLE transactions_caisse
                    ADD COLUMN IF NOT EXISTS employe_id INTEGER
                """))

                # Clé étrangère employe
                conn.execute(text("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1
                            FROM pg_constraint
                            WHERE conname = 'fk_transactions_caisse_employe'
                        ) THEN
                            ALTER TABLE transactions_caisse
                            ADD CONSTRAINT fk_transactions_caisse_employe
                            FOREIGN KEY (employe_id)
                            REFERENCES users(id);
                        END IF;
                    END
                    $$;
                """))

            print("✅ Colonnes succursale_id et employe_id vérifiées avec succès")

        except Exception as e:
            print(f"❌ Erreur migration transactions_caisse : {e}")