#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test pour créer un prêt et envoyer les notifications via Brevo
Exécution: python tu.py
"""

import sys
import os

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Client, Pret, User, Notification, Journal
from datetime import datetime


def test_creer_pret_et_notifications():
    """Test complet: création d'un prêt + envoi des notifications"""

    # ✅ CRUCIAL: Utiliser le contexte d'application
    with app.app_context():
        print("=" * 50)
        print("🧪 TEST CRÉATION PRÊT + NOTIFICATIONS BREVO")
        print("=" * 50)

        try:
            # 1. Récupérer un client existant
            client = Client.query.first()
            if not client:
                print("❌ Aucun client trouvé!")
                return False
            print(f"✅ Client: {client.prenom} {client.nom} (ID: {client.id})")
            print(f"   Email: {client.email}")

            # 2. Récupérer un agent
            agent = User.query.filter(User.role.in_(['direction', 'admin', 'admin_succursale'])).first()
            if not agent:
                agent = User.query.first()

            if not agent:
                print("❌ Aucun agent trouvé!")
                return False
            print(f"✅ Agent: {agent.prenom} {agent.nom} (ID: {agent.id})")

            # 3. Créer le prêt
            montant = 100000
            duree = 12
            taux = 12

            montant_interet = montant * (taux / 100) * (duree / 12)
            montant_total = montant + montant_interet
            mensualite = montant_total / duree if duree > 0 else montant_total

            nouveau_pret = Pret(
                client_id=client.id,
                agent_id=agent.id,
                montant=montant,
                duree_mois=duree,
                motif="Test automatique",
                type_pret="personnel",
                statut='en_attente',
                taux_interet=taux,
                mensualite=round(mensualite, 2),
                montant_interet=round(montant_interet, 2),
                montant_total=round(montant_total, 2),
                numero_dossier=f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            )

            db.session.add(nouveau_pret)
            db.session.flush()
            print(f"✅ Prêt créé (ID: {nouveau_pret.id})")

            # 4. Journal
            journal = Journal(
                employe_id=agent.id,
                action='CREATION_PRET',
                details=f"Test prêt #{nouveau_pret.id}",
                client_id=client.id,
                pret_id=nouveau_pret.id
            )
            db.session.add(journal)
            db.session.commit()
            print("✅ Commit effectué")

            # 5. Envoyer notifications via Brevo
            print("\n📧 Envoi des notifications via Brevo...")

            from app import envoyer_notification_pret, notifier_directeurs_demande_pret

            # Notification au client
            email_result = envoyer_notification_pret(client, nouveau_pret)
            print(f"   Email client: {'✅ ENVOYÉ' if email_result else '❌ ÉCHEC'}")

            # Notification aux directeurs
            try:
                notifier_directeurs_demande_pret(nouveau_pret)
                print("   ✅ Notifications directeurs: ENVOYÉES")
            except Exception as e:
                print(f"   ❌ Erreur directeurs: {str(e)}")

            # 6. Résumé
            print("\n" + "=" * 50)
            print("📋 RÉSUMÉ")
            print(f"   Prêt ID: {nouveau_pret.id}")
            print(f"   Client: {client.prenom} {client.nom}")
            print(f"   Email: {client.email}")
            print(f"   Montant: {montant:,.0f} Gdes")
            print(f"   Statut: {nouveau_pret.statut}")
            print("=" * 50)

            return True

        except Exception as e:
            db.session.rollback()
            print(f"❌ ERREUR: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def test_email_brevo():
    """Test spécifique pour l'envoi d'email via Brevo"""

    with app.app_context():
        print("=" * 50)
        print("📧 TEST EMAIL BREVO")
        print("=" * 50)

        try:
            from emails import send_email

            client = Client.query.first()
            if not client:
                print("❌ Aucun client trouvé!")
                return False

            print(f"✅ Client: {client.email}")

            # Tester l'email
            sujet = "GMES - Test Brevo"
            html = f"""
            <div style="font-family: Arial, sans-serif;">
                <h2>Bonjour {client.prenom} {client.nom},</h2>
                <p>Ceci est un test d'envoi d'email via Brevo.</p>
                <p>Si vous recevez cet email, la configuration est correcte !</p>
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

            return result

        except Exception as e:
            print(f"❌ ERREUR: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    print("\n🔧 SCRIPT DE TEST GMES + BREVO")
    print("=" * 50)

    # Test 1: Email
    print("\n1️⃣ Test d'envoi d'email Brevo")
    test_email_brevo()

    # Test 2: Création de prêt
    print("\n" + "-" * 50)
    print("2️⃣ Test création de prêt + notifications")
    test_creer_pret_et_notifications()

    print("\n" + "=" * 50)
    print("✅ Tests terminés!")