from app import app, db
from sqlalchemy import inspect, text

with app.app_context():
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('clients')]

    try:
        if 'code_postal' not in columns:
            # ✅ Utilisation de db.session.execute() avec text()
            db.session.execute(text('ALTER TABLE clients ADD COLUMN code_postal VARCHAR(20)'))
            db.session.commit()
            print("✅ Colonne code_postal ajoutée")
        else:
            print("ℹ️ Colonne code_postal existe déjà")

        if 'ville' not in columns:
            # ✅ Utilisation de db.session.execute() avec text()
            db.session.execute(text('ALTER TABLE clients ADD COLUMN ville VARCHAR(100)'))
            db.session.commit()
            print("✅ Colonne ville ajoutée")
        else:
            print("ℹ️ Colonne ville existe déjà")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.session.rollback()