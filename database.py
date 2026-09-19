from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()

            # Mise à jour automatique des colonnes ajoutées au modèle Pret
            db.session.execute(text("""
                ALTER TABLE prets
                ADD COLUMN IF NOT EXISTS solde_restant FLOAT DEFAULT 0
            """))

            db.session.execute(text("""
                ALTER TABLE prets
                ADD COLUMN IF NOT EXISTS solde_restant_cache FLOAT DEFAULT 0
            """))

            db.session.commit()

            print("✅ Base de données synchronisée avec les nouveaux champs")

        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Erreur synchronisation DB : {e}")