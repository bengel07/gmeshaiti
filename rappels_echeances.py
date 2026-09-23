# ============================================================
# rappels_echeances.py
#
# Commande Flask CLI qui envoie des rappels de remboursement
# au client à J-10, J-5, J-3 et J-1 avant chaque échéance.
#
# INSTALLATION :
#
# 1. Placez ce fichier à côté de votre app.py (ou dans un
#    dossier "scripts/" si vous préférez, en adaptant l'import
#    "from app import app" ci-dessous).
#
# 2. Dans app.py, après la création de `app` et l'import de
#    vos modèles, ajoutez simplement :
#
#       import rappels_echeances
#
#    (ça enregistre la commande CLI sans rien exécuter au
#    démarrage normal de l'app web)
#
# 3. Testez en local :
#
#       flask rappels-echeances
#
# 4. Sur Render : créez un nouveau service de type
#    "Cron Job" (pas "Web Service"), pointant sur le même
#    dépôt, avec comme commande de démarrage :
#
#       flask rappels-echeances
#
#    et programmez-le pour tourner une fois par jour
#    (par exemple à 08:00, heure locale d'Haïti).
# ============================================================

import click
from datetime import date, timedelta

from app import app
from models import db, Echeancier, NotificationClient
from services.notifier_client import notifier_client


JOURS_RAPPEL = [10, 5, 3, 1]


@app.cli.command("rappels-echeances")
def rappels_echeances():
    """
    Envoie des rappels de remboursement au client
    à J-10, J-5, J-3 et J-1 avant chaque échéance.
    """

    aujourdhui = date.today()
    total_envoyes = 0

    for jours in JOURS_RAPPEL:

        date_cible = aujourdhui + timedelta(days=jours)

        echeanciers = Echeancier.query.filter(
            Echeancier.date_echeance == date_cible,
            Echeancier.statut.in_(['en_attente', 'partiel'])
        ).all()

        for echeancier in echeanciers:

            pret = echeancier.pret

            if pret is None or pret.client_id is None:
                continue

            montant_restant = (
                echeancier.montant
                - (echeancier.montant_paye or 0)
            )

            titre = f"Remboursement dans {jours} jour(s)"

            # ============================================
            # ÉVITER LES DOUBLONS SI LA COMMANDE TOURNE
            # DEUX FOIS LE MÊME JOUR
            # ============================================

            deja_envoye = NotificationClient.query.filter(
                NotificationClient.client_id == pret.client_id,
                NotificationClient.titre == titre,
                db.func.date(
                    NotificationClient.date_creation
                ) == aujourdhui,
                NotificationClient.message.like(
                    f"%échéance n°{echeancier.numero_echeance}%"
                )
            ).first()

            if deja_envoye:
                continue

            notifier_client(
                client_id=pret.client_id,
                titre=titre,
                message=(
                    f"Votre échéance n°{echeancier.numero_echeance} "
                    f"de {montant_restant:,.2f} HTG est prévue le "
                    f"{echeancier.date_echeance.strftime('%d/%m/%Y')}."
                ),
                type="warning",
                lien=f"/mes-prets/{pret.id}"
            )

            total_envoyes += 1

    click.echo(f"✅ {total_envoyes} rappel(s) de remboursement envoyé(s).")