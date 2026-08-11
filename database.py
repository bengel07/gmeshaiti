from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()

        # ==============================
        # MIGRATION POSTGRESQL RENDER
        # ==============================
        if db.engine.url.drivername.startswith("postgresql"):
            try:
                db.session.execute(text("""
                    ALTER TABLE clients
                    ALTER COLUMN statut TYPE VARCHAR(500)
                """))

                db.session.execute(text("""
                    ALTER TABLE users
                    ALTER COLUMN statut TYPE VARCHAR(500)
                """))

                db.session.commit()

                print("✅ Migration PostgreSQL réussie")
                print("   clients.statut = VARCHAR(500)")
                print("   users.statut   = VARCHAR(500)")

            except Exception as e:
                db.session.rollback()
                print(f"⚠️ Migration PostgreSQL : {e}")

        print("✅ Tables GMES vérifiées/créées")