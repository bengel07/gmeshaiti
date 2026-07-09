# find_clients_refs.py
import os
import re


def find_clients_refs():
    """Trouve toutes les références à 'clients.id' dans les fichiers .py"""

    print("🔍 Recherche de 'clients.id' dans le projet...")
    print("=" * 50)

    found = []

    for root, dirs, files in os.walk('.'):
        # Ignorer les dossiers
        if 'venv' in root or '__pycache__' in root or 'instance' in root:
            continue

        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'clients.id' in content:
                            found.append(path)
                            print(f"\n📁 {path}")
                            # Afficher les lignes concernées
                            lines = content.split('\n')
                            for i, line in enumerate(lines):
                                if 'clients.id' in line:
                                    print(f"   Ligne {i + 1}: {line.strip()}")
                except:
                    pass

    if not found:
        print("\n✅ Aucune référence à 'clients.id' trouvée")
    else:
        print(f"\n⚠️ {len(found)} fichier(s) avec 'clients.id'")
        print("\n💡 Remplacez 'clients.id' par 'client.id' dans ces fichiers")


if __name__ == '__main__':
    find_clients_refs()