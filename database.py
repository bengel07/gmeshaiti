from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()

            # Mise à jour automatique des colonnes ajoutées au modèle User
            db.session.execute(text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS activation_token VARCHAR(200)
            """))

            db.session.execute(text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS activation_expiration TIMESTAMP
            """))

            # Contrainte UNIQUE ajoutée séparément, seulement si elle n'existe pas déjà
            db.session.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint WHERE conname = 'users_activation_token_key'
                    ) THEN
                        ALTER TABLE users ADD CONSTRAINT users_activation_token_key UNIQUE (activation_token);
                    END IF;
                END $$;
            """))

            db.session.commit()

            print("✅ Base de données synchronisée avec les nouveaux champs")

        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Erreur synchronisation DB : {e}")