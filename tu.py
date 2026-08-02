#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de diagnostic pour Render
Exécution: python diagnostic.py
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Client, Pret, User


def diagnostic_complet():
    """Diagnostic complet du système"""

    with app.app_context():
        print("=" * 60)
        print("🔍 DIAGNOSTIC COMPLET GMES")
        print("=" * 60)

        # 1. Vérifier les clients
        print("\n📋 1. LISTE DES CLIENTS")
        clients = Client.query.all()
        print(f"Total clients: {len(clients)}")

        for client in clients:
            print(f"\n   Client ID: {client.id}")
            print(f"   Nom: {client.nom} {client.prenom}")
            print(f"   Email: {client.email}")
            print(f"   Téléphone: {client.telephone}")
            print(f"   Compte: {client.numero_compte}")
            print(
                f"   terms_accepted: {client.terms_accepted} ✅" if client.terms_accepted else f"   terms_accepted: {client.terms_accepted} ❌")
            print(f"   Statut: {client.statut}")
            print(f"   Succursale ID: {client.succursale_id}")
            print("-" * 40)

        # 2. Vérifier les utilisateurs
        print("\n👤 2. LISTE DES UTILISATEURS")
        users = User.query.all()
        print(f"Total utilisateurs: {len(users)}")

        for user in users:
            print(f"\n   User ID: {user.id}")
            print(f"   Nom: {user.prenom} {user.nom}")
            print(f"   Email: {user.email}")
            print(f"   Rôle: {user.role}")
            print(f"   Succursale ID: {user.succursale_id}")
            print(f"   Statut: {user.statut}")
            print("-" * 40)

        # 3. Vérifier les prêts récents
        print("\n💰 3. DERNIERS PRÊTS")
        prets = Pret.query.order_by(Pret.id.desc()).limit(5).all()
        print(f"Derniers {len(prets)} prêts:")

        for pret in prets:
            print(f"\n   Prêt ID: {pret.id}")
            print(f"   Client ID: {pret.client_id}")
            print(f"   Montant: {pret.montant:,.0f} Gdes")
            print(f"   Durée: {pret.duree_mois} mois")
            print(f"   Statut: {pret.statut}")
            print(f"   Numéro dossier: {pret.numero_dossier}")
            if pret.client:
                print(f"   Client: {pret.client.nom} {pret.client.prenom}")
            print("-" * 40)

        # 4. Vérifier la configuration
        print("\n⚙️ 4. CONFIGURATION")
        print(f"APP_URL: {os.getenv('APP_URL', 'Non défini')}")
        print(f"BREVO_API_KEY: {'✅ Définie' if os.getenv('BREVO_API_KEY') else '❌ Manquante'}")
        print(f"MAIL_USERNAME: {os.getenv('MAIL_USERNAME', 'Non défini')}")
        print(f"SECRET_KEY: {'✅ Définie' if os.getenv('SECRET_KEY') else '❌ Manquante'}")

        # 5. Recherche d'un client spécifique
        print("\n🔎 5. RECHERCHE CLIENT SPÉCIFIQUE")
        email_test = input("Entrez l'email du client à vérifier (ou Entrée pour passer): ").strip()

        if email_test:
            client = Client.query.filter_by(email=email_test).first()
            if client:
                print(f"✅ Client trouvé:")
                print(f"   ID: {client.id}")
                print(f"   Nom: {client.nom} {client.prenom}")
                print(f"   Email: {client.email}")
                print(f"   terms_accepted: {client.terms_accepted}")
                print(f"   Statut: {client.statut}")

                # Vérifier les prêts du client
                prets_client = Pret.query.filter_by(client_id=client.id).all()
                print(f"   Nombre de prêts: {len(prets_client)}")
                for p in prets_client:
                    print(f"   - Prêt #{p.id}: {p.montant:,.0f} Gdes, {p.statut}")
            else:
                print(f"❌ Aucun client trouvé avec l'email: {email_test}")

        # 6. Réparer terms_accepted si nécessaire
        print("\n🛠️ 6. RÉPARATION TERMS_ACCEPTED")
        reponse = input("Voulez-vous forcer terms_accepted=True pour un client ? (oui/non): ").strip().lower()

        if reponse == 'oui':
            email_force = input("Entrez l'email du client: ").strip()
            client = Client.query.filter_by(email=email_force).first()
            if client:
                client.terms_accepted = True
                db.session.commit()
                print(f"✅ terms_accepted forcé à True pour {client.email}")
            else:
                print(f"❌ Client non trouvé")

        print("\n" + "=" * 60)
        print("✅ DIAGNOSTIC TERMINÉ")
        print("=" * 60)


def tester_creation_pret():
    """Test de création de prêt"""

    with app.app_context():
        print("\n" + "=" * 60)
        print("🧪 TEST DE CRÉATION DE PRÊT")
        print("=" * 60)

        try:
            # 1. Prendre un client
            client = Client.query.first()
            if not client:
                print("❌ Aucun client trouvé!")
                return

            print(f"✅ Client choisi: {client.nom} {client.prenom} (ID: {client.id})")
            print(f"   terms_accepted: {client.terms_accepted}")

            if not client.terms_accepted:
                print("❌ Client n'a pas accepté les conditions!")
                reponse = input("Voulez-vous forcer l'acceptation ? (oui/non): ").strip().lower()
                if reponse == 'oui':
                    client.terms_accepted = True
                    db.session.commit()
                    print("✅ terms_accepted forcé à True")

            # 2. Créer un prêt de test
            if client.terms_accepted:
                print("\n📝 Création d'un prêt de test...")

                from app import generer_numero_pret
                numero_pret = generer_numero_pret()

                nouveau_pret = Pret(
                    numero_pret=numero_pret,
                    client_id=client.id,
                    agent_id=1,  # Admin
                    montant=100000,
                    duree_mois=12,
                    motif="Test automatique",
                    type_pret="personnel",
                    statut='en_attente',
                    taux_interet=12,
                    mensualite=8884.88,
                    numero_dossier=f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                )

                db.session.add(nouveau_pret)
                db.session.commit()

                print(f"✅ Prêt créé avec succès!")
                print(f"   ID: {nouveau_pret.id}")
                print(f"   Numéro: {nouveau_pret.numero_pret}")
                print(f"   Dossier: {nouveau_pret.numero_dossier}")
                print(f"   Statut: {nouveau_pret.statut}")
            else:
                print("❌ Impossible de créer le prêt: terms_accepted = False")

        except Exception as e:
            db.session.rollback()
            print(f"❌ ERREUR: {str(e)}")
            import traceback
            traceback.print_exc()


def tester_email():
    """Test d'envoi d'email"""

    with app.app_context():
        print("\n" + "=" * 60)
        print("📧 TEST D'ENVOI D'EMAIL")
        print("=" * 60)

        try:
            from app import send_email_brevo

            client = Client.query.first()
            if not client:
                print("❌ Aucun client trouvé!")
                return

            print(f"✅ Client: {client.email}")

            sujet = "GMES - Test d'email"
            html = f"""
            <div style="font-family: Arial, sans-serif;">
                <h2>Bonjour {client.prenom} {client.nom},</h2>
                <p>Ceci est un test d'envoi d'email depuis Render.</p>
                <p>Si vous recevez cet email, la configuration fonctionne !</p>
                <hr>
                <p style="color: #999; font-size: 12px;">GMES Microcrédit</p>
            </div>
            """

            result = send_email_brevo(
                to_email=client.email,
                to_name=f"{client.prenom} {client.nom}",
                subject=sujet,
                html_content=html
            )

            if result:
                print(f"✅ Email envoyé à {client.email}")
            else:
                print(f"❌ Échec d'envoi à {client.email}")

        except Exception as e:
            print(f"❌ ERREUR: {str(e)}")


if __name__ == "__main__":
    from datetime import datetime

    print("\n" + "=" * 60)
    print("🔧 SCRIPT DE DIAGNOSTIC GMES")
    print("=" * 60)

    # Menu
    print("\nChoisissez une option:")
    print("1. Diagnostic complet")
    print("2. Tester création de prêt")
    print("3. Tester envoi d'email")
    print("4. Tout exécuter")

    choix = input("\nVotre choix (1-4): ").strip()

    if choix == '1':
        diagnostic_complet()
    elif choix == '2':
        tester_creation_pret()
    elif choix == '3':
        tester_email()
    elif choix == '4':
        diagnostic_complet()
        tester_creation_pret()
        tester_email()
    else:
        print("Choix invalide")