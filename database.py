def init_db(app):
    db.init_app(app)

    with app.app_context():
        try:
            with db.engine.begin() as conn:

                # ==========================================
                # 1. transactions_caisse.succursale_id
                # ==========================================
                conn.execute(text("""
                    ALTER TABLE transactions_caisse
                    ADD COLUMN IF NOT EXISTS succursale_id INTEGER
                """))

                conn.execute(text("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1
                            FROM pg_constraint
                            WHERE conname = 'fk_transactions_caisse_succursale'
                        ) THEN
                            ALTER TABLE transactions_caisse
                            ADD CONSTRAINT fk_transactions_caisse_succursale
                            FOREIGN KEY (succursale_id)
                            REFERENCES succursale(id);
                        END IF;
                    END
                    $$;
                """))

                # ==========================================
                # 2. transactions_caisse.employe_id
                # ==========================================
                conn.execute(text("""
                    ALTER TABLE transactions_caisse
                    ADD COLUMN IF NOT EXISTS employe_id INTEGER
                """))

                conn.execute(text("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1
                            FROM pg_constraint
                            WHERE conname = 'fk_transactions_caisse_employe'
                        ) THEN
                            ALTER TABLE transactions_caisse
                            ADD CONSTRAINT fk_transactions_caisse_employe
                            FOREIGN KEY (employe_id)
                            REFERENCES users(id);
                        END IF;
                    END
                    $$;
                """))

                # ==========================================
                # 3. retraits.succursale_id
                # ==========================================
                conn.execute(text("""
                    ALTER TABLE retraits
                    ADD COLUMN IF NOT EXISTS succursale_id INTEGER
                """))

                conn.execute(text("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1
                            FROM pg_constraint
                            WHERE conname = 'fk_retraits_succursale'
                        ) THEN
                            ALTER TABLE retraits
                            ADD CONSTRAINT fk_retraits_succursale
                            FOREIGN KEY (succursale_id)
                            REFERENCES succursale(id);
                        END IF;
                    END
                    $$;
                """))

            print("✅ Migration des colonnes succursale/employe terminée")

        except Exception as e:
            print(f"❌ Erreur migration : {e}")