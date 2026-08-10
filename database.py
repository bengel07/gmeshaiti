from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()

        try:
            # Corriger la longueur de clients.statut sur PostgreSQL
            if db.engine.url.drivername.startswith("postgresql"):
                db.session.execute(text("""
                    ALTER TABLE clients
                    ALTER COLUMN statut TYPE VARCHAR(500)
                """))
                db.session.commit()
                print("✅ clients.statut mis à VARCHAR(500)")

        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Migration clients.statut : {e}")

        print("✅ Tables GMES vérifiées/créées")