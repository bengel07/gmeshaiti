from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            # Vérifier la connexion PostgreSQL Render
            db.session.execute(text("SELECT 1"))
            db.session.commit()
            print("✅ Connexion PostgreSQL réussie")

            # Créer les tables manquantes
            db.create_all()
            print("✅ Tables vérifiées/créées")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur connexion/création DB : {e}")
            raise