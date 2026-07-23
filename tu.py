from app import app, db
from sqlalchemy import text

with app.app_context():

    try:
        print("🔧 Correction table competences...")

        # Désactiver les clés étrangères temporairement
        db.session.execute(text("PRAGMA foreign_keys=OFF;"))

        # Supprimer l'ancienne table
        db.session.execute(text("""
            DROP TABLE IF EXISTS competences;
        """))

        # Recréer la table avec la bonne relation
        db.session.execute(text("""
            CREATE TABLE competences (
                id INTEGER PRIMARY KEY,
                client_id INTEGER NOT NULL,
                employe_id INTEGER,
                nom VARCHAR(100) NOT NULL,
                niveau VARCHAR(50),
                description TEXT,
                date_creation DATETIME,

                FOREIGN KEY(client_id)
                REFERENCES clients(id),

                FOREIGN KEY(employe_id)
                REFERENCES users(id)
            );
        """))

        db.session.commit()

        print("✅ Table competences corrigée.")

    except Exception as e:
        db.session.rollback()
        print("❌ Erreur :", e)