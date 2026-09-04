from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()
logger = logging.getLogger(__name__)


def init_db(app):
    db.init_app(app)

    with app.app_context():
        from sqlalchemy import inspect

        try:
            logger.info("🔍 Vérification de la base de données...")

            # Vérifier si la table produits_epargne existe
            if not inspect(db.engine).has_table('produits_epargne'):
                logger.warning("⚠️ Création des tables...")

                # Créer TOUTES les tables
                db.create_all()
                logger.info("✅ Toutes les tables créées")

                # Créer le produit d'épargne par défaut
                try:
                    from models import ProduitEpargne
                    from datetime import date

                    if not ProduitEpargne.query.filter_by(code='EP-DEFAULT').first():
                        produit = ProduitEpargne(
                            code='EP-DEFAULT',
                            nom='Épargne Standard',
                            description='Compte d\'épargne standard',
                            type_produit='classique',
                            taux_interet_annuel=2.5,
                            date_lancement=date.today()
                        )
                        db.session.add(produit)
                        db.session.commit()
                        logger.info("✅ Produit d'épargne par défaut créé")
                except Exception as e:
                    logger.warning(f"⚠️ Produit non créé: {e}")
            else:
                logger.info("✅ Tables déjà existantes")

        except Exception as e:
            logger.error(f"❌ Erreur: {e}")
            raise