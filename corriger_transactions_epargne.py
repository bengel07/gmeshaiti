from app import app, db
from sqlalchemy import inspect, text

colonnes = {
    "groupe_id": "VARCHAR(32)",
    "reference": "VARCHAR(80)",
    "compte_interne_id": "INTEGER REFERENCES comptes_internes(id)",
    "type": "VARCHAR(30)",
    "sens": "VARCHAR(6)",
    "libelle": "VARCHAR(255)",
    "periode": "VARCHAR(7)",
    "created_by": "INTEGER REFERENCES users(id)",
    "created_at": "DATETIME",
}

with app.app_context():
    inspecteur = inspect(db.engine)

    if not inspecteur.has_table("transactions_epargne"):
        raise RuntimeError("Table transactions_epargne introuvable.")

    existantes = {
        c["name"]
        for c in inspecteur.get_columns("transactions_epargne")
    }

    with db.engine.begin() as conn:
        for nom, definition in colonnes.items():
            if nom not in existantes:
                conn.execute(text(
                    f'ALTER TABLE transactions_epargne '
                    f'ADD COLUMN "{nom}" {definition}'
                ))
                print(f"Colonne ajoutée : {nom}")

        conn.execute(text("""
            UPDATE transactions_epargne
            SET type = type_transaction
            WHERE type IS NULL
        """))

        conn.execute(text("""
            UPDATE transactions_epargne
            SET created_at = COALESCE(date_transaction, CURRENT_TIMESTAMP)
            WHERE created_at IS NULL
        """))

        conn.execute(text("""
            UPDATE transactions_epargne
            SET libelle = description
            WHERE libelle IS NULL
        """))

        conn.execute(text("""
            UPDATE transactions_epargne
            SET periode = strftime('%Y-%m', created_at)
            WHERE periode IS NULL
        """))

    print("Migration additive terminée.")
