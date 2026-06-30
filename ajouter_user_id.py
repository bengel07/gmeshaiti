# fichier: ajouter_employe_id.py
import sqlite3

print("🔧 Ajout de employe_id à la base de données...")

# Connexion à la base
connexion = sqlite3.connect('gmes.db')
curseur = connexion.cursor()

# Étape 1: Vérifier ce qu'il y a dans la base
print("\n📊 Tables dans la base:")
curseur.execute("SELECT name FROM sqlite_master WHERE type='table'")
for table in curseur.fetchall():
    print(f"  - {table[0]}")

# Étape 2: Regarder la table face_data
print("\n🔍 Structure de face_data:")
curseur.execute("PRAGMA table_info(face_data)")
colonnes = curseur.fetchall()

if not colonnes:
    print("❌ La table face_data n'existe pas!")
else:
    print("Colonnes actuelles:")
    for col in colonnes:
        print(f"  {col[0]}. {col[1]} ({col[2]})")

    # Étape 3: Vérifier si employe_id existe déjà
    noms_colonnes = [col[1] for col in colonnes]

    if 'employe_id' in noms_colonnes:
        print("\n✅ employe_id existe déjà!")
    else:
        print("\n➕ Ajout de la colonne employe_id...")
        curseur.execute("ALTER TABLE face_data ADD COLUMN employe_id INTEGER")
        connexion.commit()
        print("✅ employe_id ajouté avec succès!")

        # Étape 4: Vérifier l'ajout
        curseur.execute("PRAGMA table_info(face_data)")
        print("\n📋 Nouvelle structure:")
        for col in curseur.fetchall():
            print(f"  {col[0]}. {col[1]} ({col[2]})")

# Fermer la connexion
connexion.close()
print("\n✅ Opération terminée!")
