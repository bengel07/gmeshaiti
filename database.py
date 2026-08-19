from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            # Vérifier si la colonne existe
            result = db.session.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'transactions'
                AND column_name = 'type_transaction'
            """))

            colonne_existe = result.fetchone()

            if not colonne_existe:
                print("⚠️ Colonne type_transaction absente.")
                print("🔧 Ajout de la colonne type_transaction...")

                db.session.execute(text("""
                    ALTER TABLE transactions
                    ADD COLUMN type_transaction VARCHAR(50)
                    DEFAULT 'depot'
                """))

                db.session.commit()

                print("✅ Colonne type_transaction ajoutée.")

            else:
                print("✅ Colonne type_transaction déjà présente.")

        except Exception as e:
            db.session.rollback()
            print("❌ Erreur ajout type_transaction :", e)