# create_tables.py
# Script pour créer les tables manquantes

import os
import sys
from app import app, db
from sqlalchemy import text, inspect


def create_missing_tables():
    """Crée uniquement les tables manquantes"""
    with app.app_context():
        print("=" * 50)
        print("🔍 Vérification des tables manquantes...")
        print("=" * 50)

        try:
            # Vérifier les tables existantes
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            print(f"📋 Tables existantes : {existing_tables}")

            # Désactiver les contraintes FK
            db.session.execute(text('PRAGMA foreign_keys=OFF;'))

            # Créer les tables manquantes
            db.create_all()

            # Réactiver les contraintes FK
            db.session.execute(text('PRAGMA foreign_keys=ON;'))
            db.session.commit()

            # Vérifier après création
            inspector = inspect(db.engine)
            new_tables = inspector.get_table_names()
            print(f"\n📋 Tables après création : {new_tables}")

            # Trouver les nouvelles tables
            created = [t for t in new_tables if t not in existing_tables]
            if created:
                print(f"\n✅ Tables créées : {created}")
            else:
                print("\n✅ Aucune nouvelle table à créer")

            return True

        except Exception as e:
            print(f"❌ Erreur : {e}")
            db.session.rollback()

            # Tentative de récupération
            try:
                print("\n🔄 Tentative de récupération...")
                db.session.execute(text('PRAGMA foreign_keys=OFF;'))
                db.create_all()
                db.session.execute(text('PRAGMA foreign_keys=ON;'))
                db.session.commit()
                print("✅ Tables créées avec succès (mode récupération)")
                return True
            except Exception as e2:
                print(f"❌ Échec : {e2}")
                return False


if __name__ == '__main__':
    create_missing_tables()
    print("\n" + "=" * 50)
    print("✅ Script terminé.")