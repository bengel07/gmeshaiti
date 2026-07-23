from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    with app.app_context():
        try:
            with db.engine.begin() as conn:

                conn.execute(text("""
                       ALTER TABLE competences
                       DROP CONSTRAINT IF EXISTS competences_client_id_fkey;
                   """))

                conn.execute(text("""
                       ALTER TABLE competences
                       ADD CONSTRAINT competences_client_id_fkey
                       FOREIGN KEY (client_id)
                       REFERENCES clients(id);
                   """))

                print("✅ Correction FK competences.client_id terminée")

        except Exception as e:
            print("⚠️ Migration FK:", e)
