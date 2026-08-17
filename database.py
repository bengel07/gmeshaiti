from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            # Ajouter la colonne si elle n'existe pas
            db.session.execute(text("""
                ALTER TABLE groupes
                ADD COLUMN IF NOT EXISTS succursale_id INTEGER
            """))

            # Ajouter la clé étrangère si elle n'existe pas
            db.session.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conname = 'fk_groupes_succursale'
                    ) THEN
                        ALTER TABLE groupes
                        ADD CONSTRAINT fk_groupes_succursale
                        FOREIGN KEY (succursale_id)
                        REFERENCES succursale(id);
                    END IF;
                END
                $$;
            """))

            db.session.commit()

            print("✅ Migration groupes.succursale_id effectuée")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur migration groupes : {e}")

