from sqlalchemy import text
from database import db

def update_table_prets_signature():
    """Ajoute les colonnes nécessaires à la signature des prêts."""

    try:
        print("🔄 Mise à jour de la table prets...")

        requetes = [

            # Le client a accepté les conditions
            """
            ALTER TABLE prets
            ADD COLUMN IF NOT EXISTS conditions_acceptees BOOLEAN DEFAULT FALSE;
            """,

            # Date de signature
            """
            ALTER TABLE prets
            ADD COLUMN IF NOT EXISTS date_signature_conditions TIMESTAMP;
            """,

            # Token utilisé (optionnel mais pratique)
            """
            ALTER TABLE prets
            ADD COLUMN IF NOT EXISTS token_signature TEXT;
            """,

            # Adresse IP
            """
            ALTER TABLE prets
            ADD COLUMN IF NOT EXISTS ip_signature VARCHAR(100);
            """,

            # Navigateur
            """
            ALTER TABLE prets
            ADD COLUMN IF NOT EXISTS user_agent_signature TEXT;
            """,

            # Signature du client
            """
            ALTER TABLE prets
            ALTER COLUMN signature TYPE TEXT;
            """,

            # Références
            """
            ALTER TABLE prets
            ALTER COLUMN reference1 TYPE TEXT;
            """,

            """
            ALTER TABLE prets
            ALTER COLUMN reference2 TYPE TEXT;
            """,

            """
            ALTER TABLE prets
            ALTER COLUMN info_garant TYPE TEXT;
            """,

            """
            ALTER TABLE prets
            ALTER COLUMN motif TYPE TEXT;
            """,

            """
            ALTER TABLE prets
            ALTER COLUMN autre_type_pret TYPE TEXT;
            """,

            """
            ALTER TABLE prets
            ALTER COLUMN numero_dossier TYPE TEXT;
            """,

            """
            ALTER TABLE prets
            ALTER COLUMN code_pret TYPE TEXT;
            """,

            """
            ALTER TABLE prets
            ALTER COLUMN signature_responsable TYPE TEXT;
            """,

            """
            ALTER TABLE prets
            ALTER COLUMN motif_refus TYPE TEXT;
            """
        ]

        for sql in requetes:
            try:
                db.session.execute(text(sql))
                print("✅ OK")
            except Exception as e:
                print("⚠️", e)

        db.session.commit()
        print("🎉 Table prets mise à jour avec succès.")

    except Exception as e:
        db.session.rollback()
        print("❌ Erreur :", e)