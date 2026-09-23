from datetime import datetime

from models import db, NotificationClient


def notifier_client(client_id, titre, message, type="info", lien=None):
    """
    Crée une notification destinée UNIQUEMENT au client
    (jamais au personnel / agents / direction).

    type : "info", "success", "warning" ou "danger"
    lien : lien optionnel vers un écran de l'app mobile
           (ex: "/mes-prets/12"), jamais un lien vers le
           panneau interne du personnel.
    """

    try:

        notif = NotificationClient(
            client_id=client_id,
            titre=titre,
            message=message,
            type=type,
            lien=lien,
            lue=False,
            date_creation=datetime.utcnow()
        )

        db.session.add(notif)
        db.session.commit()

        return notif

    except Exception as e:

        db.session.rollback()

        print("❌ Erreur notifier_client :", str(e))

        return None