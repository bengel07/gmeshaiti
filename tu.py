# fix_terms.py
from app import app
from database import db
from models import TermsAcceptance  # Adapte selon ton modèle

with app.app_context():
    print("⚠️ Recréation de la table terms_acceptance...")

    # Supprimer la table
    TermsAcceptance.__table__.drop(db.engine)
    print("✅ Ancienne table supprimée")

    # Recréer avec nullable=True
    TermsAcceptance.__table__.create(db.engine)
    print("✅ Nouvelle table créée")

    print("🎯 Problème résolu !")