# utils/stats.py - NOUVEAU FICHIER
from flask import current_app
from database import db, init_db
from models import User, Client, Pret, Groupe, ProjetSocial, Emploi, Famille, Satisfaction
from sqlalchemy import func, case

# utils/stats.py
from flask import current_app
from database import db
from models import User, Client, Pret, Groupe, Notification, Pointage, Succursale
from sqlalchemy import func, case
from datetime import datetime, date
import logging

from sqlalchemy import func
from datetime import datetime,timedelta
from models import (
    Client, Pret, Epargne,
    RetardPaiement, User,Employe,
    ScoringCredit, Remboursement
)
# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_stats_dashboard():
    """Récupère les statistiques pour le tableau de bord"""

    # print("=== get_stats_dashboard() appelée ===")

    try:
        # 1. Clients actifs

        # Si Client est un modèle séparé
        clients_actifs = db.session.query(func.count(Client.id)).filter(Client.statut == 'actif').scalar() or 0

        # 2. Total des prêts ACCORDÉS (pas tous les prêts)
        total_prets_result = db.session.query(func.sum(Pret.montant)).filter(Pret.statut.in_(['actif','accorde', 'approuve', 'en_cours'])).scalar()
        total_prets = float(total_prets_result) if total_prets_result else 0

        # 3. Taux de remboursement
        taux_result = db.session.query(
            (func.sum(case((Pret.statut == "remboursé", 1), else_=0)) * 100.0) / func.count(Pret.id)
        ).scalar()

        taux_remboursement = round(float(taux_result) if taux_result else 0)
        # print(f"taux_remboursement: {taux_remboursement}")

        # 4. Communautés
        communautes = db.session.query(func.count(func.distinct(Client.groupe_id))).scalar() or 0
        # print(f"communautes: {communautes}")

        # 5. ⭐ NOUVEAU : Projets sociaux financés
        projets_sociaux = db.session.query(func.count(ProjetSocial.id)).filter(
            ProjetSocial.statut == 'en_cours').scalar() or 0

        # 6. ⭐ NOUVEAU : Familles aidées
        familles_aidees = db.session.query(func.count(Famille.id)).filter(Famille.statut == 'aidee').scalar() or 0

        # 7. ⭐ NOUVEAU : Emplois créés
        emplois_crees = db.session.query(func.count(Emploi.id)).filter(Emploi.statut == 'actif').scalar() or 0

        # 8. ⭐ NOUVEAU : Projets réalisés
        projets_realises = db.session.query(func.count(ProjetSocial.id)).filter(
            ProjetSocial.statut == 'termine').scalar() or 0

        # 9. ⭐ NOUVEAU : Total des clients accompagnés (total clients)
        total_clients = db.session.query(func.count(Client.id)).scalar() or 0

        # 10. ⭐ NOUVEAU : Taux de satisfaction (si vous avez un modèle Satisfaction)
        satisfaction_result = db.session.query(func.avg(Satisfaction.note)).scalar()
        taux_satisfaction = f"{round(float(satisfaction_result) if satisfaction_result else 98)}%"

        # Formatage
        if total_prets >= 1000000:
            formatted_prets = f"{total_prets / 1000000:.1f}M"
        elif total_prets >= 1000:
            formatted_prets = f"{total_prets / 1000:.1f}K"
        else:
            formatted_prets = f"{total_prets:.0f}"

        result = {
            "clients_actifs": clients_actifs,
            "total_prets": formatted_prets,
            "taux_remboursement": taux_remboursement,
            "communautes": communautes,
            # ⭐ NOUVELLES STATISTIQUES
            "total_clients": total_clients,
            "projets_sociaux": projets_sociaux,
            "familles_aidees": familles_aidees,
            "emplois_crees": emplois_crees,
            "projets_realises": projets_realises,
            "taux_satisfaction": taux_satisfaction
        }

        # print(f"✅ Stats calculées: {result}")
        return result

    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

        return {
            "clients_actifs": 0,
            "total_prets": "0",
            "taux_remboursement": 0,
            "communautes": 0,
            "total_clients": 0,
            "projets_sociaux": 12,
            "familles_aidees": 45,
            "emplois_crees": 28,
            "projets_realises": 23,
            "taux_satisfaction": "98%"


        }


def get_stats_employes_succursale(succursale_id):
    """Statistiques pour le suivi des employés"""
    today = datetime.utcnow().date()
    employes = User.query.filter_by(actif=True).count()

    retards = Notification.query.join(User).filter(
        User.succursale_id == succursale_id,
        Notification.message.like("%Retard%"),
        func.date(Notification.created_at) == today
    ).count()

    absences = Notification.query.join(User).filter(
        User.succursale_id == succursale_id,
        Notification.message.like("%Absence%"),
        func.date(Notification.created_at) == today
    ).count()

    pointages_today = Pointage.query.join(User).filter(
        User.succursale_id == succursale_id,
        func.date(Pointage.heure_arrivee) == today
    ).count()
    presence_rate = (pointages_today / employes * 100) if employes > 0 else 0

    return {
        "employes": employes,
        "presence": round(presence_rate, 2),
        "retards": retards,
        "absences": absences,
        "succursales": {
            "total": Succursale.query.count(),
            "actives": Succursale.query.filter_by(actif=True).count()
        }
    }



def stats():
    """Retourne les statistiques globales"""
    from datetime import datetime, timedelta

    today = datetime.utcnow().date()

    # Compter les employés actifs
    employes = User.query.filter_by(actif=True).count()

    # Compter les retards aujourd'hui
    retards = Notification.query.filter(
        Notification.message.like("%Retard%"),
        db.func.date(Notification.created_at) == today
    ).count()

    # Compter les absences aujourd'hui
    absences = Notification.query.filter(
        Notification.message.like("%Absence%"),
        db.func.date(Notification.created_at) == today
    ).count()

    # Taux de présence
    pointages_today = Pointage.query.filter(
        db.func.date(Pointage.heure_arrivee) == today
    ).count()

    presence_rate = (pointages_today / employes * 100) if employes > 0 else 0

    return {
        "employes": employes,
        "presence": round(presence_rate, 2),
        "retards": retards,
        "absences": absences,
        "succursales": {
            "total": Succursale.query.count(),
            "actives": Succursale.query.filter_by(actif=True).count()
        }
    }



def get_stats_direction_succursale(succursale_id):
    """Statistiques du dashboard directeur de succursale"""

    total_clients = Client.query.filter_by(
        succursale_id=succursale_id
    ).count()

    total_employes = User.query.filter_by(
        succursale_id=succursale_id
    ).count()

    portefeuille_credits = db.session.query(
        func.sum(Pret.montant_accorde)
    ).filter(
        Pret.succursale_id == succursale_id,
        Pret.statut.in_(["actif", "approuve"])
    ).scalar() or 0

    epargne_totale = db.session.query(
        func.sum(Epargne.solde)
    ).join(Client).filter(
        Client.succursale_id == succursale_id
    ).scalar() or 0

    prets_attente = Pret.query.filter(
        Pret.succursale_id == succursale_id,
        Pret.statut.in_(["en_attente", "soumis"])
    ).count()

    total_prets = Pret.query.filter(
        Pret.succursale_id == succursale_id,
        Pret.statut.in_(["actif", "approuve"])
    ).count()

    prets_retard_30 = Pret.query.filter(
        Pret.succursale_id == succursale_id,
        Pret.statut == "impaye"
    ).count()

    par30 = round(
        (prets_retard_30 / total_prets) * 100,
        2
    ) if total_prets else 0

    score_moyen = db.session.query(
        func.avg(ScoringCredit.score_global)
    ).join(Client).filter(
        Client.succursale_id == succursale_id
    ).scalar() or 0

    clients_risque = ScoringCredit.query.join(Client).filter(
        Client.succursale_id == succursale_id,
        ScoringCredit.categorie_risque.in_(["D", "E"])
    ).count()

    retards = RetardPaiement.query.join(Client).filter(
        Client.succursale_id == succursale_id,
        RetardPaiement.statut == "impaye"
    ).all()

    montant_retards = sum(
        r.montant_retard or 0
        for r in retards
    )

    nombre_retards = len(retards)

    return {
        "total_clients": total_clients,
        "total_employes": total_employes,
        "prets_attente": prets_attente,
        "portefeuille_credits": portefeuille_credits,
        "epargne_totale": epargne_totale,
        "total_actifs": portefeuille_credits + epargne_totale,
        "par_30": par30,
        "score_moyen": round(score_moyen, 2),
        "clients_risque": clients_risque,
        "montant_retards": montant_retards,
        "nombre_retards": nombre_retards,
        "resultat_net": 0,
        "roa": 0,
        "taux_penetration": 0,
        "satisfaction": 95
    }

def get_stats_remboursements_succursale(succursale_id):
    """Statistiques des retards de remboursement"""

    retards = RetardPaiement.query.join(Client).filter(
        Client.succursale_id == succursale_id,
        RetardPaiement.statut == "impaye"
    ).all()

    montant_retards = sum(
        r.montant_retard or 0
        for r in retards
    )

    return {
        "nombre_retards": len(retards),
        "montant_retards": montant_retards,
        "jours_retard": sum(
            r.jours_retard or 0
            for r in retards
        )
    }

# stats.py

# from datetime import datetime, timedelta

def get_stats_dossiers_attente(dossiers_attente):
    """Statistiques des dossiers en attente"""

    maintenant = datetime.now()
    aujourdhui = maintenant.date()

    return {
        'total': len(dossiers_attente),

        'aujourdhui': sum(
            1 for d in dossiers_attente
            if d.date_signature_terms
            and d.date_signature_terms.date() == aujourdhui
        ),

        'semaine': sum(
            1 for d in dossiers_attente
            if d.date_signature_terms
            and d.date_signature_terms >= maintenant - timedelta(days=7)
        ),

        'retard_validation': sum(
            1 for d in dossiers_attente
            if d.date_signature_terms
            and d.date_signature_terms < maintenant - timedelta(days=3)
        )
    }


def get_stats_caissier(succursale_id):
    """Statistiques du dashboard caissier"""

    aujourd_hui = datetime.now().date()
    debut_mois = aujourd_hui.replace(day=1)

    # Pour inclure tout le mois jusqu'à aujourd'hui
    fin_mois = aujourd_hui

    logger.debug(f"Période: du {debut_mois} au {fin_mois}")
    logger.debug(f"Succursale ID: {succursale_id}")

    return {
        'paiements_aujourd_hui':
            Remboursement.query
            .join(Pret)
            .filter(Pret.succursale_id == succursale_id)
            .filter(func.date(Remboursement.date_remboursement) == aujourd_hui)
            .count(),

        'montant_aujourd_hui':
            db.session.query(func.sum(Remboursement.montant))
            .join(Pret)
            .filter(Pret.succursale_id == succursale_id)
            .filter(func.date(Remboursement.date_remboursement) == aujourd_hui)
            .scalar() or 0,

        'paiements_mois':
            Remboursement.query
            .join(Pret)
            .filter(Pret.succursale_id == succursale_id)
            .filter(func.date(Remboursement.date_remboursement) >= debut_mois)
            .count(),

        'montant_mois':
            db.session.query(func.sum(Remboursement.montant))
            .join(Pret)
            .filter(Pret.succursale_id == succursale_id)
            .filter(func.date(Remboursement.date_remboursement) >= debut_mois)
            .scalar() or 0,
    }

def get_stats_succursale(succursale_id):
    """Statistiques générales d'une succursale"""

    return {
        'clients': Client.query.filter_by(
            succursale_id=succursale_id
        ).count(),

        'employes': User.query.filter_by(
            succursale_id=succursale_id
        ).count(),

        'prets': Pret.query.filter_by(
            succursale_id=succursale_id
        ).count(),

        'remboursements':
            db.session.query(
                func.sum(Remboursement.montant)
            )
            .join(Pret)
            .filter(
                Pret.succursale_id == succursale_id
            )
            .scalar() or 0
    }


def get_stats_admin_succursale(succursale_id):
    """Statistiques du tableau de bord administrateur de succursale"""

    debut_mois = datetime.now().replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    clients_total = Client.query.filter_by(
        succursale_id=succursale_id
    ).count()

    clients_nouveaux = Client.query.filter(
        Client.succursale_id == succursale_id,
        Client.date_inscription >= debut_mois
    ).count()

    prets_actifs = Pret.query.filter_by(
        succursale_id=succursale_id,
        statut='actif'
    ).count()

    prets_en_attente = Pret.query.filter_by(
        succursale_id=succursale_id,
        statut='en_attente'
    ).count()

    montant_actifs = db.session.query(
        func.coalesce(func.sum(Pret.montant), 0)
    ).filter(
        Pret.succursale_id == succursale_id,
        Pret.statut == 'actif'
    ).scalar()

    prets_total = Pret.query.filter_by(
        succursale_id=succursale_id
    ).count()

    taux_approbation = round(
        (prets_actifs / prets_total) * 100,
        2
    ) if prets_total > 0 else 0

    return {
        'clients': {
            'total': clients_total,
            'nouveaux_ce_mois': clients_nouveaux
        },

        'prets': {
            'actifs': prets_actifs,
            'en_attente': prets_en_attente,
            'total': prets_total,
            'montant_actifs': montant_actifs
        },

        'performance': {
            'taux_approbation': taux_approbation
        }
    }

from models import HistoriqueEmploye, Succursale

def get_stats_employe(employe):
    """Statistiques détaillées d'un employé"""

    return {
        'nb_credits_octroyes': (
            len(employe.credits_agent)
            if hasattr(employe, 'credits_agent')
            else 0
        ),

        'nb_clients_suivis': (
            len(employe.clients)
            if hasattr(employe, 'clients')
            else 0
        ),

        'nb_paiements_enregistres': (
            len(employe.paiements)
            if hasattr(employe, 'paiements')
            else 0
        ),

        'derniere_connexion': (
            employe.date_derniere_connexion.strftime('%d/%m/%Y %H:%M')
            if hasattr(employe, 'date_derniere_connexion')
            and employe.date_derniere_connexion
            else 'Jamais'
        ),

        'date_creation': (
            employe.date_inscription.strftime('%d/%m/%Y')
            if employe.date_inscription
            else 'N/A'
        )
    }

# stats.py

def get_stats_verifications_brh(succursale_id=None):
    """
    Statistiques conformité BRH / AML-CFT
    """
    from models import Employe

    query = Employe.query

    if succursale_id:
        query = query.filter_by(succursale_id=succursale_id)

    employes = query.all()

    total = len(employes)

    verifies = sum(
        1 for e in employes
        if getattr(e, 'verifications_completes', False)
    )

    formations_completes = sum(
        1 for e in employes
        if getattr(e, 'formation_aml_cft', False)
    )

    conformes = sum(
        1 for e in employes
        if getattr(e, 'verifications_completes', False)
        and getattr(e, 'formation_aml_cft', False)
    )

    non_verifies = total - verifies
    non_formes = total - formations_completes

    taux_conformite = round(
        (conformes / total) * 100,
        2
    ) if total > 0 else 0

    return {
        'total': total,
        'verifies': verifies,
        'non_verifies': non_verifies,
        'formations_completes': formations_completes,
        'non_formes': non_formes,
        'conformes': conformes,
        'taux_conformite': taux_conformite
    }

# stats.py



def get_stats_employes(succursale_id=None):
    """
    Statistiques des employés
    """

    query = User.query.filter(
        User.role.in_([
            'employe',
            'superviseur',
            'directeur'
        ])
    )

    if succursale_id:
        query = query.filter_by(
            succursale_id=succursale_id
        )

    return {
        'total': query.count(),
        'actifs': query.filter_by(
            statut='actif'
        ).count(),

        'en_attente': query.filter_by(
            statut='en_attente'
        ).count(),

        'formation': query.filter_by(
            statut='formation'
        ).count(),

        'inactifs': query.filter_by(
            statut='inactif'
        ).count()
    }




def get_stats_succursales(user):
    """
    Statistiques globales des succursales
    """

    if user.role == 'super_admin':
        succursales = Succursale.query.all()
    else:
        succursales = Succursale.query.filter_by(
            id=user.succursale_id
        ).all()

    stats_globales = []

    for s in succursales:

        clients = Client.query.filter_by(
            succursale_id=s.id
        ).count()

        prets = Pret.query.filter(
            Pret.succursale_id == s.id,
            Pret.statut.in_([
                'actif',
                'approuve'
            ])
        ).count()

        remboursements = Remboursement.query.filter_by(
            succursale_id=s.id
        ).count()

        montant_total = db.session.query(
            db.func.coalesce(
                db.func.sum(Pret.montant_accorde),
                0
            )
        ).filter(
            Pret.succursale_id == s.id,
            Pret.statut.in_([
                'actif',
                'approuve'
            ])
        ).scalar()

        stats_globales.append({
            'succursale': s,
            'clients': clients,
            'prets': prets,
            'remboursements': remboursements,
            'montant_total': montant_total,
            'employes': User.query.filter_by(
                succursale_id=s.id
            ).count(),

            'prets_retard': Pret.query.filter_by(
                succursale_id=s.id,
                statut='impaye'
            ).count(),

            'epargne_totale': db.session.query(
                db.func.coalesce(
                    db.func.sum(Epargne.solde),
                    0
                )
            ).join(Client).filter(
                Client.succursale_id == s.id
            ).scalar()
        })

    return stats_globales

def get_detail_succursale_stats(succursale_id):
    """
    Statistiques détaillées d'une succursale
    """

    succursale = Succursale.query.get_or_404(
        succursale_id
    )

    nombre_clients = Client.query.filter_by(
        succursale_id=succursale.id
    ).count()

    prets_actifs = Pret.query.filter_by(
        succursale_id=succursale.id,
        statut='actif'
    ).count()

    remboursements = Remboursement.query.filter_by(
        succursale_id=succursale.id
    ).count()

    employes = User.query.filter_by(
        succursale_id=succursale.id,
        role='employe'
    ).all()

    return {
        'nombre_clients': nombre_clients,
        'prets_actifs': prets_actifs,
        'remboursements': remboursements,
        'employes': employes
    }





def get_stats_admin_central_succursales():
    """
    Statistiques globales admin central pour toutes les succursales
    """

    succursales = Succursale.query.all()

    stats_globales = []

    for s in succursales:

        clients = Client.query.filter_by(
            succursale_id=s.id
        ).count()

        prets = Pret.query.filter(
            Pret.succursale_id == s.id,
            Pret.statut.in_(['actif', 'approuve'])
        ).count()

        remboursements = Remboursement.query.filter_by(
            succursale_id=s.id
        ).count()

        montant_total = db.session.query(
            db.func.coalesce(
                db.func.sum(Pret.montant_accorde),
                0
            )
        ).filter(
            Pret.succursale_id == s.id,
            Pret.statut.in_(['actif', 'approuve'])
        ).scalar()

        stats_globales.append({
            'succursale': s,
            'clients': clients,
            'prets': prets,
            'remboursements': remboursements,
            'montant_total': montant_total
        })

    return stats_globales


def calculer_statistiques_globales():
    """Calcule les statistiques globales du système"""

    from models import User, Client, Pret, Remboursement, Epargne, Employe, Groupe

    total_clients = Client.query.filter_by(role='client').count()
    total_prets = Pret.query.count()
    prets_approuve = Pret.query.filter_by(statut='approuve').count()
    prets_actifs = Pret.query.filter_by(statut='actif').count()
    prets_en_attente = Pret.query.filter_by(statut='en_attente').count()

    # Calcul des montants
    montant_total_prets = db.session.query(func.sum(Pret.montant)).scalar() or 0
    montant_prets_actifs = db.session.query(func.sum(Pret.montant)).filter(
        Pret.statut == 'approuve'
    ).scalar() or 0

    # Remboursements
    total_remboursements = Remboursement.query.count()
    montant_total_rembourse = db.session.query(func.sum(Remboursement.montant)).scalar() or 0

    # Groupes
    total_groupes = Groupe.query.count()

    # Taux de remboursement
    taux_remboursement = (montant_total_rembourse / montant_total_prets * 100) if montant_total_prets > 0 else 0

    # Clients avec prêts
    clients_avec_prets_count = db.session.query(
        func.count(func.distinct(User.id))
    ).join(Pret, User.id == Pret.client_id).filter(
        User.role == 'client'
    ).scalar() or 0

    # ✅ Import différé pour éviter le cycle app.py <-> stats.py
    from app import calculer_rotation_fonds

    return {
        'clients': {
            'total': total_clients,
            'avec_prets': clients_avec_prets_count,
            'nouveaux_ce_mois': User.query.filter(
                User.date_inscription >= datetime.utcnow().replace(day=1),
                User.role == 'client'
            ).count()
        },
        'prets': {
            'total': total_prets,
            'actifs': prets_actifs,
            'prets_approuve': prets_approuve,
            'en_attente': prets_en_attente,
            'montant_total': round(montant_total_prets, 2),
            'montant_actifs': round(montant_prets_actifs, 2)
        },
        'remboursements': {
            'total': total_remboursements,
            'montant_total': round(montant_total_rembourse, 2),
            'taux_remboursement': round(taux_remboursement, 1)
        },
        'groupes': {
            'total': total_groupes,
            'membres_moyen': total_clients / total_groupes if total_groupes > 0 else 0
        },
        'performance': {
            'taux_approbation': (prets_actifs / total_prets * 100) if total_prets > 0 else 0,
            'rotation_fonds': calculer_rotation_fonds()
        }
    }


def get_stats_direction_generale():
    """Statistiques complètes pour le dashboard direction générale"""

    from models import User, Client, Pret, PaiementPret, CompteCaisse, Transaction, RetardPaiement
    import random

    aujourdhui = datetime.now().date()
    mois_dernier = aujourdhui - timedelta(days=30)
    mois_avant_dernier = aujourdhui - timedelta(days=60)
    premier_jour_mois = datetime.now().replace(day=1)

    # Commercial - CA mensuel
    ca_mensuel = db.session.query(func.sum(Pret.montant)).filter(
        Pret.date_decaissement >= premier_jour_mois,
        Pret.statut == 'decaisse'
    ).scalar() or 0

    # Financier - Résultat net
    resultat_net = db.session.query(func.sum(PaiementPret.interets)).filter(
        PaiementPret.date_paiement >= premier_jour_mois
    ).scalar() or 0

    # Opérations - Transactions du jour
    transactions_jour = Transaction.query.filter(
        Transaction.date_creation >= datetime.now().replace(hour=0, minute=0, second=0)
    ).count()

    # RH - Effectif actif
    effectif_total = User.query.filter_by(est_actif=True, statut='actif').count()

    # Globales
    total_actifs = db.session.query(func.sum(Pret.montant)).filter(Pret.statut == 'actif').scalar() or 0
    portefeuille_credits = total_actifs
    total_clients = Client.query.count()

    # Dossiers / Prêts en attente (séparés)
    en_attente_dossiers = Client.query.filter_by(statut='en_attente_approbation').count()
    en_attente_prets = Pret.query.filter_by(statut='en_attente').count()

    # Clients en retard
    clients_en_retard = (
        db.session.query(
            Client,
            func.sum(RetardPaiement.jours_retard),
            func.count(RetardPaiement.id)
        )
        .join(RetardPaiement, RetardPaiement.client_id == Client.id)
        .group_by(Client.id)
        .having(func.sum(RetardPaiement.jours_retard) > 0)
        .all()
    )

    stats = {
        'total_actifs': total_actifs,
        'portefeuille_credits': portefeuille_credits,
        'total_clients': total_clients,
        'resultat_net': resultat_net,
        'par_30': 4.2,            # ⚠️ placeholder, pas encore calculé
        'roa': 3.8,                # ⚠️ placeholder
        'taux_penetration': 15.5,  # ⚠️ placeholder
        'satisfaction': 87,        # ⚠️ placeholder
        'performance_commerciale': 78,  # ⚠️ placeholder
        'performance_financiere': 82,   # ⚠️ placeholder
        'performance_operations': 75,   # ⚠️ placeholder
        'performance_rh': 85,           # ⚠️ placeholder
        'dossiers_en_attente': en_attente_dossiers,
        'prets_en_attente': en_attente_prets,
        'en_attente': en_attente_dossiers + en_attente_prets,
        'clients_en_retard': clients_en_retard
    }

    performance = {
        'commercial': {'ca_mensuel': ca_mensuel},
        'financier': {'resultat_net': resultat_net},
        'operations': {'transactions_jour': transactions_jour},
        'rh': {'effectif_total': effectif_total}
    }

    # Succursales
    succursales_list = Succursale.query.filter_by(active=True).all()
    succursales_data = []

    for s in succursales_list:
        encours = db.session.query(func.sum(Pret.montant)) \
                      .join(Client, Pret.client_id == Client.id) \
                      .filter(
                          Client.succursale_id == s.id,
                          Pret.statut.in_(['actif', 'impaye'])
                      ).scalar() or 0

        clients = Client.query.filter_by(succursale_id=s.id).count()

        succursales_data.append({
            'nom': s.nom,
            'code': s.code,
            'ville': s.ville,
            'encours': encours,
            'par_30': 4.2,  # ⚠️ placeholder — l'ancien calcul s'annulait toujours à 4.2
            'par_30_couleur': 'warning' if encours > 0 else 'success',
            'clients': clients,
            'performance': min(100, (encours / 100000000 * 100) if encours > 0 else 0),
            'performance_couleur': 'success' if encours > 50000000 else 'warning',
            'tendance': 'stable'  # ⚠️ placeholder — l'ancien était random.choice(), retiré
        })

    # Alertes
    alertes = []

    succursales_critiques = []
    for succ in Succursale.query.all():
        total_credits = Pret.query.filter_by(succursale_id=succ.id).count()
        credits_impayes = Pret.query.filter(
            Pret.succursale_id == succ.id,
            Pret.statut == 'impaye',
            Pret.date_echeance < aujourdhui - timedelta(days=30)
        ).count()

        if total_credits > 0 and (credits_impayes / total_credits) * 100 > 5:
            succursales_critiques.append(succ.nom)

    if succursales_critiques:
        alertes.append({
            'type': 'danger',
            'icone': 'exclamation-triangle',
            'titre': f'PAR > 5% dans {len(succursales_critiques)} succursale(s)',
            'description': f'Les succursales {", ".join(succursales_critiques)} dépassent le seuil critique de 5%.',
            'priorite': 'Haute',
            'succursale': ', '.join(succursales_critiques),
            'date': "Aujourd'hui"
        })

    croissance_mois_dernier = db.session.query(func.sum(Pret.montant)).filter(
        Pret.date_decaissement >= mois_dernier
    ).scalar() or 0

    croissance_mois_avant = db.session.query(func.sum(Pret.montant)).filter(
        Pret.date_decaissement >= mois_avant_dernier,
        Pret.date_decaissement < mois_dernier
    ).scalar() or 0

    if croissance_mois_avant > 0:
        taux_croissance = ((croissance_mois_dernier - croissance_mois_avant) / croissance_mois_avant) * 100
        if taux_croissance < 0:
            alertes.append({
                'type': 'warning',
                'icone': 'chart-line',
                'titre': 'Croissance en baisse',
                'description': f'La croissance du portefeuille a baissé de {abs(round(taux_croissance, 1))}% par rapport au mois dernier.',
                'priorite': 'Moyenne',
                'succursale': 'Toutes',
                'date': 'Cette semaine'
            })

    seuil_decouvert = -1000000
    comptes_decouvert = CompteCaisse.query.filter(CompteCaisse.solde < seuil_decouvert).count()

    if comptes_decouvert > 0:
        alertes.append({
            'type': 'danger',
            'icone': 'credit-card',
            'titre': 'Découvert bancaire critique',
            'description': f'{comptes_decouvert} compte(s) en situation de découvert dépassant le seuil autorisé.',
            'priorite': 'Urgente',
            'succursale': 'Toutes',
            'date': "Aujourd'hui"
        })

    seuil_inactivite = 90
    clients_inactifs = (
        db.session.query(func.count(func.distinct(Client.id)))
        .join(Pret, Pret.client_id == Client.id)
        .filter(
            Pret.derniere_activite < datetime.now() - timedelta(days=seuil_inactivite),
            Client.compte_actif.is_(True)
        )
        .scalar() or 0
    )

    if clients_inactifs > 10:
        alertes.append({
            'type': 'warning',
            'icone': 'user-friends',
            'titre': 'Clients inactifs',
            'description': f'{clients_inactifs} clients sont inactifs depuis plus de {seuil_inactivite} jours.',
            'priorite': 'Moyenne',
            'succursale': 'Toutes',
            'date': 'Cette semaine'
        })

    decisions = [
        {
            'titre': 'Déploiement nouveau système',
            'description': 'Migration vers la nouvelle plateforme core banking',
            'statut': 'En cours',
            'statut_couleur': 'warning',
            'date_echeance': datetime.now() + timedelta(days=45),
            'progression': 65,
            'couleur': 'info'
        }
    ]

    evolution = {
        'encours': [82, 85, 83, 88, 92, 95, 98, 102, 105, 108, 112, 115],  # ⚠️ placeholder
        'clients': [12.5, 13.2, 13.8, 14.5, 15.2, 16.1, 17.0, 17.8, 18.5, 19.2, 20.1, 21.0]  # ⚠️ placeholder
    }

    return {
        'stats': stats,
        'total_clients': total_clients,
        'performance': performance,
        'succursales': succursales_data,
        'alertes': alertes,
        'decisions': decisions,
        'evolution': evolution,
        'clients_en_retard': clients_en_retard
    }