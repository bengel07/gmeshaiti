
# Ajouter cette fonction au début du fichier (hors de la route)
def generer_numero_pret():
    from datetime import datetime
    import random

    date_actuelle = datetime.now().strftime("%Y%m%d")
    chiffres_aleatoires = str(random.randint(000, 99999))
    return f"GMES_Pret-{date_actuelle}-{chiffres_aleatoires}"



def notifier_directeurs_demande_pret(pret, type_action="nouvelle_demande"):
    """
    Notifie tous les directeurs et administrateurs d'une action sur une demande de prêt

    Args:
        pret: Objet Pret (la demande de prêt)
        type_action: Type d'action ("nouvelle_demande", "approbation", "refus", "modification")
    """
    from models import User, Notification, Action  # ← AJOUTÉ Action
    from datetime import datetime, timedelta
    from flask import url_for
    from flask_login import current_user

    print("=" * 70)
    print(f"📢 NOTIFICATION DIRECTEURS - Action: {type_action}")
    print("=" * 70)

    try:
        # Récupérer les informations nécessaires
        client = pret.client
        agent = pret.agent if pret.agent_id else None

        if not client:
            print("❌ Client non trouvé pour ce prêt")
            return False

        # Déterminer la succursale concernée
        succursale_id = client.succursale_id

        # Configuration des messages selon l'action
        config_messages = {
            "attente_signature": {
                "titre": f"📨 Conditions envoyées au client - Prêt #{pret.id}",
                "type": "info",
                "icone": "📨",
                "couleur": "gray"
            },
            "annulation": {
                "titre": f"🚫 Demande de prêt #{pret.id} annulée",
                "type": "warning",
                "icone": "🚫",
                "couleur": "orange"
            },
            "nouvelle_demande": {
                "titre": f"💰 Nouvelle demande de prêt #{pret.id}",
                "type": "info",
                "icone": "💰",
                "couleur": "blue"
            },
            "approbation": {
                "titre": f"✅ Prêt #{pret.id} approuvé",
                "type": "success",
                "icone": "✅",
                "couleur": "green"
            },
            "refus": {
                "titre": f"❌ Prêt #{pret.id} refusé",
                "type": "danger",
                "icone": "❌",
                "couleur": "red"
            },
            "modification": {
                "titre": f"✏️ Prêt #{pret.id} modifié",
                "type": "warning",
                "icone": "✏️",
                "couleur": "orange"
            }
        }

        config = config_messages.get(type_action, config_messages["nouvelle_demande"])

        # Formater le montant
        montant_formate = f"{pret.montant:,.0f} HTG".replace(',', ' ')

        # Construire le message détaillé
        message = (
            f"Client: {client.prenom} {client.nom}\n"
            f"Montant: {montant_formate}\n"
            f"Durée: {pret.duree_mois} mois\n"
            f"Taux: {pret.taux_interet}%\n"
        )

        if agent:
            message += f"Agent: {agent.prenom} {agent.nom}\n"

        if pret.date_demande:
            message += f"Date: {pret.date_demande.strftime('%d/%m/%Y %H:%M')}"

        # Construire le lien vers le prêt
        lien_pret = url_for('voir_pret', pret_id=pret.id, _external=True)

        # Liste des rôles à notifier
        roles_cibles = ['direction', 'directeur', 'admin', 'super_admin', 'admin_succursale']

        # Construire la requête de base
        query = User.query.filter(
            User.role.in_(roles_cibles),
            User.actif == True
        )

        # Filtrer par succursale si spécifiée
        if succursale_id:
            directeurs_succursale = query.filter(
                (User.succursale_id == succursale_id) |
                (User.role.in_(['admin', 'direction', 'directeur', 'super_admin']))
            ).all()
        else:
            directeurs_succursale = query.all()

        # Éliminer les doublons
        destinataires = directeurs_succursale

        if not destinataires:
            print("⚠️ Aucun destinataire trouvé")
            return False

        print(f"📨 Notification à {len(destinataires)} destinataire(s)")
        directeur = destinataires[0]
        titre_action = f"Nouvelle demande de prêt #{pret.id}"
        date_creation = datetime.now()

        # 🔥 CRÉER UNE ACTION UNIQUE POUR CETTE NOTIFICATION
        nouvelle_action = Action(
            pret_id=pret.id,
            titre=titre_action,
            assignee_a_id=directeur.id,  # ✅ AJOUTER CETTE LIGNE
            creee_par_id=pret.agent_id,  # ✅ Correction
            type_action=type_action,
            date_creation=date_creation,
            date_action=datetime.now(),

            # ✅ Obligatoire dans la base de données
            date_echeance=date_creation + timedelta(days=7),

            description=f"{config['titre']} - {message[:1000]}",
            statut="a_faire",
            progression=0,
            notification_envoyee=False
        )
        db.session.add(nouvelle_action)
        db.session.flush()  # Pour obtenir nouvelle_action.id

        # Créer les notifications
        notifications_creees = 0
        for destinataire in destinataires:
            try:
                # Vérifier si une notification similaire existe déjà
                existing = Notification.query.filter_by(
                    employe_id=destinataire.id,
                    titre=config["titre"],
                    lue=False
                ).first()

                if existing and type_action == "nouvelle_demande":
                    print(f"   ⏭️ Notification déjà existante pour {destinataire.email}")
                    continue

                # Créer la notification avec le bon action_id
                notification = Notification(
                    employe_id=destinataire.id,
                    titre=config["titre"],
                    message=message,
                    type_notification=config["type"],
                    lien=lien_pret,
                    date_envoi=datetime.now(),
                    lue=False,
                    destinataire_id=destinataire.id,
                    action_id=nouvelle_action.id,  # ← CORRIGÉ : utilise l'ID de l'Action
                    date_creation=datetime.now(),
                    pret_id=pret.id
                )
                db.session.add(notification)
                notifications_creees += 1
                print(f"   ✅ Notification créée pour {destinataire.email} ({destinataire.role})")

            except Exception as e:
                print(f"   ❌ Erreur pour {destinataire.email}: {e}")

        # Commit en une seule fois
        if notifications_creees > 0:
            db.session.commit()
            print(f"✅ {notifications_creees} notifications créées avec succès")
            return True
        else:
            print("⚠️ Aucune nouvelle notification créée")
            return False

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur critique dans notifier_directeurs_demande_pret: {e}")
        import traceback
        traceback.print_exc()
        return False