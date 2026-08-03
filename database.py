from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

def corriger_colonnes_prets():
    """Corrige les colonnes VARCHAR(255) qui doivent être en TEXT."""
    try:
        print("🔧 Vérification des colonnes de la table prets...")

        requetes = [
            "ALTER TABLE prets ALTER COLUMN signature TYPE TEXT;",
            "ALTER TABLE prets ALTER COLUMN reference1 TYPE TEXT;",
            "ALTER TABLE prets ALTER COLUMN reference2 TYPE TEXT;",
            "ALTER TABLE prets ALTER COLUMN info_garant TYPE TEXT;",
            "ALTER TABLE prets ALTER COLUMN motif TYPE TEXT;",
            "ALTER TABLE prets ALTER COLUMN motif_refus TYPE TEXT;",
            "ALTER TABLE prets ALTER COLUMN signature_responsable TYPE TEXT;",
            "ALTER TABLE prets ALTER COLUMN autre_type_pret TYPE TEXT;",
            "ALTER TABLE prets ALTER COLUMN numero_dossier TYPE TEXT;",
            "ALTER TABLE prets ALTER COLUMN code_pret TYPE TEXT;"
        ]

        for req in requetes:
            try:
                db.session.execute(text(req))
                print(f"✅ {req}")
            except Exception as e:
                print(f"⚠️ {e}")

        db.session.commit()
        print("🎉 Correction terminée.")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur : {e}")


def init_db(app):
    db.init_app(app)

    with app.app_context():
        corriger_colonnes_prets()