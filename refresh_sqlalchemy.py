# refresh_sqlalchemy.py
import sys
import os

# Ajouter le répertoire courant
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Forçage du rafraîchissement SQLAlchemy...")

try:
    from app import app, db

    with app.app_context():
        print("1. Nettoyage du cache des métadonnées...")

        # Méthode radicale : supprimer et recréer toutes les métadonnées
        db.metadata.clear()

        # Réfléchir à nouveau la structure
        db.metadata.reflect(bind=db.engine)

        print("2. Vérification de la table succursales...")

        # Vérifier via l'inspecteur
        from sqlalchemy import inspect

        inspector = inspect(db.engine)

        if 'succursales' in inspector.get_table_names():
            print("   ✅ Table succursales trouvée")

            # Lister les colonnes
            columns = inspector.get_columns('succursales')
            column_names = [col['name'] for col in columns]

            print(f"   Colonnes: {column_names}")

            if 'code' in column_names:
                print("   ✅ Colonne 'code' présente")
            else:
                print("   ❌ Colonne 'code' MANQUANTE")
        else:
            print("   ❌ Table succursales introuvable")

        print("\n3. Test d'une requête SQLAlchemy...")

        try:
            # Essayer d'exécuter une requête simple
            from sqlalchemy import text

            result = session.execute(text("SELECT id, code, nom FROM succursales LIMIT 1")).fetchone()
            if result:
                print(f"   ✅ Requête réussie: ID={result[0]}, Code='{result[1]}', Nom='{result[2]}'")
            else:
                print("   ⚠ Requête réussie mais aucun résultat")
        except Exception as e:
            print(f"   ❌ Erreur requête: {e}")

        print("\n✅ Cache SQLAlchemy rafraîchi!")

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback

    traceback.print_exc()