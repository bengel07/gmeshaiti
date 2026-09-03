from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            # Vérifier la connexion
            db.session.execute(text("SELECT 1"))

            # =====================================================
            # AJOUTER id_pret DANS LA TABLE prets SI ABSENT
            # =====================================================

            db.session.execute(text("""
                ALTER TABLE prets
                ADD COLUMN IF NOT EXISTS id_pret VARCHAR(20)
            """))

            # =====================================================
            # REMPLIR id_pret POUR LES ANCIENS PRÊTS
            # =====================================================

            db.session.execute(text("""
                UPDATE prets
                SET id_pret = 'PRET-' || LPAD(id::text, 6, '0')
                WHERE id_pret IS NULL
            """))

            # =====================================================
            # INDEX UNIQUE
            # =====================================================

            db.session.execute(text("""
                CREATE UNIQUE INDEX IF NOT EXISTS
                ix_prets_id_pret_unique
                ON prets (id_pret)
            """))

            db.session.commit()

            print("✅ Connexion PostgreSQL réussie")
            print("✅ Colonne prets.id_pret vérifiée/ajoutée")
            print("✅ Anciens prêts vérifiés")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur initialisation DB : {e}")