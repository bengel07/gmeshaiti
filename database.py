from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)


def migration_prochaine_echeance():
    try:
        db.session.execute(text("""
            ALTER TABLE prets
            ADD COLUMN IF NOT EXISTS prochaine_echeance DATE;
        """))

        db.session.commit()
        print("✅ Colonne prochaine_echeance ajoutée")

    except Exception as e:
        db.session.rollback()
        print("❌ Erreur migration prochaine_echeance :", e)