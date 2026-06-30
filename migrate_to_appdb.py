# migrate_to_appdb.py
import os
import sqlite3
import pickle

print("🚀 Migration vers gmes.db...")

# 1. Supprimer gmes.db existant s'il y a conflit
if os.path.exists('gmes.db'):
    # Sauvegarder d'abord
    backup = 'gmes.db.backup'
    if os.path.exists(backup):
        os.remove(backup)
    os.rename('gmes.db', backup)
    print(f"📦 Ancien gmes.db sauvegardé: {backup}")

# 2. Créer gmes.db avec toutes les tables
print("🗃️ Création de gmes.db...")

# Créer la connexion
conn = sqlite3.connect('gmes.db')
cursor = conn.cursor()

# Créer la table face_data
cursor.execute("""
               CREATE TABLE IF NOT EXISTS face_data
               (
                   id
                   INTEGER
                   PRIMARY
                   KEY
                   AUTOINCREMENT,
                   client_id
                   INTEGER
                   NOT
                   NULL,
                   nom
                   TEXT
                   NOT
                   NULL,
                   fonction
                   TEXT,
                   face_encoding
                   BLOB
                   NOT
                   NULL,
                   selfie_path
                   TEXT,
                   photo_id_path
                   TEXT,
                   date_enregistrement
                   DATETIME
                   DEFAULT
                   CURRENT_TIMESTAMP
               )
               """)

# Créer les autres tables si elles existent dans app.db
if os.path.exists('app.db'):
    print("📦 Transfert des données depuis app.db...")

    # Se connecter à app.db
    conn_app = sqlite3.connect('app.db')
    cursor_app = conn_app.cursor()

    # Copier la table face_data
    cursor_app.execute("SELECT * FROM face_data")
    face_data = cursor_app.fetchall()

    for row in face_data:
        cursor.execute("""
                       INSERT INTO face_data (client_id, nom, fonction, face_encoding, selfie_path, photo_id_path,
                                              date_enregistrement)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       """, row[1:])  # Sauter l'ID

    print(f"✅ {len(face_data)} visages transférés")
    conn_app.close()

conn.commit()
conn.close()

print("✅ gmes.db créé avec succès!")

print("\n📁 Vérification:")
print(f"  gmes.db: {os.path.getsize('gmes.db')} octets")

# CORRECTION: Éviter le backslash dans le f-string
app_exists = 'Existe' if os.path.exists('app.db') else "N'existe pas"
faces_exists = 'Existe' if os.path.exists('faces.db') else "N'existe pas"

print(f"  app.db: {app_exists}")
print(f"  faces.db: {faces_exists}")

print("\n🔧 Maintenant modifiez app.py pour utiliser:")
print("   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gmes.db'")