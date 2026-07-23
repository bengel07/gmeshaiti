from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():

        def corriger_colonnes_postgresql():
            """Corrige automatiquement les colonnes trop petites sur PostgreSQL."""

            if db.engine.dialect.name != "postgresql":
                print("ℹ️ Base SQLite détectée, correction ignorée.")
                return

            try:
                db.session.execute(text("""
                       ALTER TABLE clients
                       ALTER COLUMN statut TYPE VARCHAR(100);
                   """))

                db.session.execute(text("""
                       ALTER TABLE users
                       ALTER COLUMN statut TYPE VARCHAR(100);
                   """))

                db.session.commit()
                print("✅ Colonnes 'statut' corrigées.")

            except Exception as e:
                db.session.rollback()
                print(f"ℹ️ Correction ignorée : {e}")

        # Exécuter la correction
        corriger_colonnes_postgresql()
