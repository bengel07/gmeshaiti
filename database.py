from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def ajouter_colonnes_clients():
    """Ajoute les nouvelles colonnes de la table clients si elles n'existent pas."""
    try:
        with db.engine.begin() as conn:

            # Colonne ville
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='clients'
                AND column_name='ville'
            """))

            if result.fetchone() is None:
                print("➕ Ajout de la colonne ville...")
                conn.execute(text("""
                    ALTER TABLE clients
                    ADD COLUMN ville VARCHAR(100)
                """))

            # Colonne code_postal
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='clients'
                AND column_name='code_postal'
            """))

            if result.fetchone() is None:
                print("➕ Ajout de la colonne code_postal...")
                conn.execute(text("""
                    ALTER TABLE clients
                    ADD COLUMN code_postal VARCHAR(100)
                """))

        print("✅ Vérification des colonnes clients terminée.")

    except Exception as e:
        print(f"❌ Erreur migration clients : {e}")


def init_db(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()

        # ✅ Exécuter une seule fois au démarrage
        ajouter_colonnes_clients()