# utils/stats.py - NOUVEAU FICHIER
from flask import current_app
from database import db, init_db
from models import  User, Client, Pret, Groupe
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
            "communautes": communautes
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