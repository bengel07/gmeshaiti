from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            db.session.execute(text("""
                ALTER TABLE prets
                ADD COLUMN IF NOT EXISTS prochaine_echeance DATE;
            """))
            db.session.commit()
            print("✅ Colonne prochaine_echeance vérifiée")
        except Exception as e:
            db.session.rollback()
            print("❌ Erreur migration prochaine_echeance :", e)