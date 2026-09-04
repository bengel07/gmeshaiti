# fix.py - Script de correction automatique
import re
import os


def fix_models_file():
    file_path = 'models.py'

    if not os.path.exists(file_path):
        print(f"❌ Fichier {file_path} non trouvé !")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Compter les occurrences
    count = content.count("'succursales.id'") + content.count('"succursales.id"')
    print(f"📊 {count} occurrences trouvées")

    # Correction
    content = content.replace("'succursales.id'", "'succursale.id'")
    content = content.replace('"succursales.id"', '"succursale.id"')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Corrections appliquées !")


if __name__ == "__main__":
    fix_models_file()