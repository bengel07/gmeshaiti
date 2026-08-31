from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            # Mettre à jour la clé étrangère de retraits
            db.session.execute(text("""
                ALTER TABLE retraits
                DROP CONSTRAINT IF EXISTS retraits_transaction_id_fkey;
            """))

            db.session.execute(text("""
                ALTER TABLE retraits
                ADD CONSTRAINT retraits_transaction_id_fkey
                FOREIGN KEY (transaction_id)
                REFERENCES transactions_epargne(id);
            """))

            db.session.commit()

            print("✅ BASE DE DONNÉES MISE À JOUR :")
            print("   retraits.transaction_id → transactions_epargne.id")

        except Exception as e:
            db.session.rollback()
            print(f"❌ ERREUR MISE À JOUR BASE DE DONNÉES : {e}")