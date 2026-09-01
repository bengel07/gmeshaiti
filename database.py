from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            with db.engine.begin() as conn:

                # Ajouter la colonne si elle n'existe pas
                conn.execute(text("""
                    ALTER TABLE transactions_caisse
                    ADD COLUMN IF NOT EXISTS succursale_id INTEGER
                """))

                # Ajouter la clé étrangère vers la vraie table : succursale
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

            print("✅ transactions_caisse.succursale_id vérifié avec succès")

        except Exception as e:
            print(f"❌ Erreur migration succursale_id : {e}")