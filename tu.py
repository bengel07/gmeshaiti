from sqlalchemy import create_engine, text

DATABASE_URL = "COLLE_ICI_LA_DATABASE_URL_DE_RENDER"

# Certaines URL Render commencent par postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE clients
        ALTER COLUMN statut TYPE VARCHAR(100);
    """))

print("✅ Colonne 'statut' modifiée avec succès.")