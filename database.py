from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            # Supprimer l'ancienne colonne id_pret si elle existe
            # La colonne n'est plus utilisée par le modèle Pret.
            db.session.execute(text("""
                ALTER TABLE prets
                DROP COLUMN IF EXISTS id_pret;
            """))

            db.session.commit()

            print("✅ Migration DB : colonne id_pret supprimée si elle existait.")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur migration id_pret : {e}")
            raise