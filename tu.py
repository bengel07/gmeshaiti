from app import app, db
from sqlalchemy import text


def fix_competence_fk():

    with app.app_context():

        engine = db.engine
        db_type = engine.name

        print(f"🗄 Base détectée : {db_type}")

        if db_type == "postgresql":

            print("🔍 Vérification PostgreSQL...")

            result = db.session.execute(text("""
                SELECT
                    ccu.table_name AS foreign_table
                FROM information_schema.table_constraints tc
                JOIN information_schema.constraint_column_usage ccu
                ON tc.constraint_name = ccu.constraint_name
                WHERE tc.table_name='competences'
                AND tc.constraint_name='competences_client_id_fkey';
            """))

            row = result.fetchone()

            if row:
                print("➡️ Référence actuelle :", row.foreign_table)

                if row.foreign_table == "users":

                    print("🗑 Suppression ancienne FK...")

                    db.session.execute(text("""
                        ALTER TABLE competences
                        DROP CONSTRAINT competences_client_id_fkey;
                    """))

                    db.session.commit()

                    print("🔧 Création nouvelle FK...")

                    db.session.execute(text("""
                        ALTER TABLE competences
                        ADD CONSTRAINT competences_client_id_fkey
                        FOREIGN KEY (client_id)
                        REFERENCES clients(id);
                    """))

                    db.session.commit()

                    print("✅ Correction PostgreSQL terminée")

                else:
                    print("✅ Déjà correct")

            else:
                print("⚠️ Contrainte inexistante")


        elif db_type == "sqlite":

            print("🔍 Vérification SQLite...")

            result = db.session.execute(
                text("PRAGMA foreign_key_list(competences);")
            )

            rows = result.fetchall()

            for row in rows:
                print(row)

            print("""
⚠️ SQLite ne permet pas de modifier directement une FK.
Il faut recréer la table.
""")

        else:
            print("❌ Base inconnue")


if __name__ == "__main__":
    fix_competence_fk()