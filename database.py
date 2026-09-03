from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    # 👇 AJOUTEZ CE BLOC POUR EXÉCUTER LA CRÉATION UNE SEULE FOIS
    with app.app_context():
        from sqlalchemy import inspect

        # Vérifier si la table produits_epargne existe
        if not inspect(db.engine).has_table('produits_epargne'):
            print("⚠️ Table produits_epargne inexistante - Création en cours...")

            # Créer TOUTES les tables manquantes
            db.create_all()
            print("✅ Toutes les tables créées avec succès")

            # Créer le produit d'épargne par défaut
            try:
                from models import ProduitEpargne
                from datetime import date

                # Vérifier si le produit existe déjà
                produit = ProduitEpargne.query.filter_by(code='EP-DEFAULT').first()
                if not produit:
                    print("📝 Création du produit d'épargne par défaut...")
                    produit = ProduitEpargne(
                        code='EP-DEFAULT',
                        nom='Épargne Standard',
                        description='Compte d\'épargne standard pour les clients',
                        type_produit='classique',
                        taux_interet_annuel=2.5,
                        date_lancement=date.today()
                    )
                    db.session.add(produit)
                    db.session.commit()
                    print("✅ Produit d'épargne par défaut créé")
                else:
                    print("✅ Produit d'épargne par défaut déjà existant")
            except Exception as e:
                print(f"⚠️ Erreur lors de la création du produit: {e}")
        else:
            print("✅ Table produits_epargne déjà existante")

        # Optionnel : Afficher toutes les tables existantes
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📋 Tables existantes: {tables}")