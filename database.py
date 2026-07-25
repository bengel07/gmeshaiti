from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    from sqlalchemy import inspect, text

    def add_columns(app):
        """Ajoute les colonnes manquantes à la table clients"""
        with app.app_context():
            try:
                inspector = inspect(db.engine)
                columns = [col["name"] for col in inspector.get_columns("clients")]

                new_columns = {
                    "code_postal": "VARCHAR(100)",
                    "ville": "VARCHAR(200)"
                }

                for name, sql_type in new_columns.items():
                    if name not in columns:
                        try:
                            print(f"📌 Ajout de {name}...")
                            db.session.execute(
                                text(f"ALTER TABLE clients ADD COLUMN {name} {sql_type}")
                            )
                            db.session.commit()
                            print(f"✅ {name} ajouté")
                        except Exception as e:
                            db.session.rollback()
                            print(f"❌ Erreur pour {name}: {e}")
                    else:
                        print(f"✅ {name} existe déjà")

            except Exception as e:
                print(f"❌ Erreur générale : {e}")
                db.session.rollback()


