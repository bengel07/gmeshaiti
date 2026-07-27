# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import text
#
# db = SQLAlchemy()
#
#
# def init_db(app):
#     db.init_app(app)
#
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():

        def ajouter_colonne_client_dossier():

            inspector = inspect(db.engine)

            colonnes = [
                col["name"]
                for col in inspector.get_columns("dossiers")
            ]

            if "client_id" not in colonnes:
                print("🔧 Ajout colonne client_id dans dossiers...")

                db.session.execute(text("""
                    ALTER TABLE dossiers
                    ADD COLUMN client_id INTEGER
                """))

                db.session.execute(text("""
                    ALTER TABLE dossiers
                    ADD CONSTRAINT fk_dossiers_client
                    FOREIGN KEY (client_id)
                    REFERENCES clients(id)
                """))

                db.session.commit()

                print("✅ client_id ajouté avec succès")

            else:
                print("ℹ️ client_id existe déjà")


        # IMPORTANT : exécuter la migration
        ajouter_colonne_client_dossier()
