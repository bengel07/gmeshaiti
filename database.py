from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            # Vérifier que la connexion PostgreSQL fonctionne
            db.session.execute(text("SELECT 1"))

            # Ajouter succursale_id si la colonne n'existe pas
            db.session.execute(text("""
                ALTER TABLE retraits_attente
                ADD COLUMN IF NOT EXISTS succursale_id INTEGER
            """))

            # Ajouter la clé étrangère si elle n'existe pas
            db.session.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conname = 'fk_retraits_attente_succursale'
                    ) THEN
                        ALTER TABLE retraits_attente
                        ADD CONSTRAINT fk_retraits_attente_succursale
                        FOREIGN KEY (succursale_id)
                        REFERENCES succursale(id);
                    END IF;
                END
                $$;
            """))

            db.session.commit()

            print("✅ Connexion PostgreSQL réussie")
            print("✅ Colonne succursale_id vérifiée/ajoutée")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur initialisation DB : {e}")