# run.py
import os
import sys

# Ajoutez le répertoire courant au chemin
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importer et lancer l'application
from app import app

if __name__ == '__main__':
    with app.app_context():
        from app import initialiser_donnees

        initialiser_donnees()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)