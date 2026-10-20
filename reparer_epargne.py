"""
Repare la base PostgreSQL pour correspondre aux modeles (models.py) :
  1. ajoute toutes les colonnes manquantes (jamais de suppression, jamais de NOT NULL)
  2. recopie l'historique de transactions_epargne dans les nouvelles colonnes :
        type        <- type_transaction
        created_at  <- date_transaction
        sens        <- credit (depot, transfert_entrant) / debit (retrait, transfert_sortant)

A lancer dans ~/gmeshaiti avec le venv actif :   python reparer_epargne.py
Il montre le plan, demande de taper OUI, puis applique tout en une seule transaction
(si une instruction echoue, rien n'est modifie).
"""
import os
import sys

from sqlalchemy import inspect, text


def type_sql(engine, col):
    """Type SQL de la colonne ; un Enum devient VARCHAR (evite CREATE TYPE)."""
    enums = getattr(col.type, "enums", None)
    if enums:
        return f"VARCHAR({max(50, max(len(e) for e in enums))})"
    return col.type.compile(dialect=engine.dialect)


def main():
    sys.path.insert(0, os.getcwd())
    from app import app
    from database import db

    with app.app_context():
        engine = db.engine
        q = engine.dialect.identifier_preparer.quote
        insp = inspect(engine)
        existantes = set(insp.get_table_names())

        instructions = []          # (description, sql)
        colonnes_apres = {}        # table -> set(colonnes apres ajout)

        for table in db.metadata.sorted_tables:
            if table.name not in existantes:
                print(f"[info] table absente (db.create_all la creera) : {table.name}")
                continue
            en_base = {c["name"] for c in insp.get_columns(table.name)}
            colonnes_apres[table.name] = set(en_base)
            for col in table.columns:
                if col.name not in en_base:
                    sql = f"ALTER TABLE {q(table.name)} ADD COLUMN {q(col.name)} {type_sql(engine, col)}"
                    instructions.append((f"ajouter {table.name}.{col.name}", sql))
                    colonnes_apres[table.name].add(col.name)

        t = "transactions_epargne"
        cols = colonnes_apres.get(t, set())
        tq = q(t)
        if {"type", "type_transaction"} <= cols:
            instructions.append(("copier type_transaction -> type",
                f"UPDATE {tq} SET {q('type')} = type_transaction WHERE {q('type')} IS NULL AND type_transaction IS NOT NULL"))
        if {"created_at", "date_transaction"} <= cols:
            instructions.append(("copier date_transaction -> created_at (sinon maintenant)",
                f"UPDATE {tq} SET created_at = COALESCE(date_transaction, CURRENT_TIMESTAMP) WHERE created_at IS NULL"))
        if "groupe_id" in cols:
            instructions.append(("groupe_id des anciennes lignes (un groupe par ligne : HIST<id>)",
                f"UPDATE {tq} SET groupe_id = 'HIST' || CAST(id AS VARCHAR) WHERE groupe_id IS NULL"))
        if {"periode", "date_transaction"} <= cols:
            if engine.dialect.name == "postgresql":
                expr = "to_char(date_transaction, 'YYYY-MM')"
            else:
                expr = "strftime('%Y-%m', date_transaction)"
            instructions.append(("periode (AAAA-MM) depuis date_transaction",
                f"UPDATE {tq} SET periode = {expr} WHERE periode IS NULL AND date_transaction IS NOT NULL"))
        if {"libelle", "description"} <= cols:
            instructions.append(("libelle <- description",
                f"UPDATE {tq} SET libelle = SUBSTR(description, 1, 255) WHERE libelle IS NULL AND description IS NOT NULL"))
        if {"sens", "type_transaction"} <= cols:
            instructions.append(("deduire sens (credit/debit)",
                f"UPDATE {tq} SET sens = CASE "
                f"WHEN type_transaction IN ('depot','transfert_entrant') THEN 'credit' "
                f"WHEN type_transaction IN ('retrait','transfert_sortant') THEN 'debit' END "
                f"WHERE sens IS NULL"))

        if not instructions:
            print("Rien a faire : la base correspond deja aux modeles.")
            return

        print(f"\nBase : {engine.url.get_backend_name()} / {engine.url.database}")
        print(f"{len(instructions)} operation(s) prevue(s) :\n")
        for desc, sql in instructions:
            print(f"  - {desc}\n      {sql}")

        if input("\nTapez OUI pour appliquer (une sauvegarde pg_dump est recommandee) : ").strip() != "OUI":
            print("Annule. Rien n'a ete modifie.")
            return

        with engine.begin() as conn:
            for desc, sql in instructions:
                res = conn.execute(text(sql))
                n = f" ({res.rowcount} ligne(s))" if sql.startswith("UPDATE") else ""
                print(f"  OK  {desc}{n}")
        print("\nTermine. Redemarrez : sudo systemctl restart gmes.service")


if __name__ == "__main__":
    main()
    os._exit(0)