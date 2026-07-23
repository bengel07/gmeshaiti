# views.py
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
from flask import current_app as app

# =============================================
# DÉCORATEUR POUR VÉRIFIER SUPER_ADMIN
# =============================================
def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'super_admin':
            flash('⛔ Accès réservé aux super administrateurs', 'danger')
            return redirect(url_for('admin_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# views.py - Ajoutez cette fonction après PAGES





def get_pages_by_category(category=None):
    """Retourne les pages filtrées par catégorie"""
    if category is None:
        return PAGES
    return {k: v for k, v in PAGES.items() if v.get('category') == category}

def get_pages_by_roles(roles):
    """Retourne les pages accessibles par les rôles donnés"""
    # À adapter selon vos besoins
    accessible_pages = {}
    for role in roles:
        if role == 'super_admin':
            accessible_pages.update(PAGES)
        elif role == 'direction':
            # Pages pour la direction
            accessible_pages.update({k: v for k, v in PAGES.items() if v.get('category') in ['Direction', 'Administration']})
        elif role == 'superviseur':
            # Pages pour les superviseurs
            accessible_pages.update({k: v for k, v in PAGES.items() if v.get('category') in ['Superviseurs', 'Employés']})
        elif role == 'employe':
            # Pages pour les employés
            accessible_pages.update({k: v for k, v in PAGES.items() if v.get('category') == 'Employés'})
    return accessible_pages





# =============================================
# DICTIONNAIRE DE TOUTES TES PAGES - VERSION CORRIGÉE
# =============================================
PAGES = {
    # =============================================
    # ADMINISTRATION (Super Admin)
    # =============================================
    "admin_dashboard": {
        "name": "Tableau de bord",
        "icon": "📊",
        "function": "Vue globale",
        "endpoint": "admin_dashboard",  # ✅ EXISTE: /admin/dashboard
        "category": "Administration"
    },
    "gestion_utilisateurs": {
        "name": "Gestion utilisateurs",
        "icon": "👥",
        "function": "CRUD utilisateurs",
        "endpoint": "gestion_utilisateurs",  # ✅ EXISTE: /admin/utilisateurs
        "category": "Administration"
    },
    "liste_users": {
        "name": "Gestion des Employés",
        "icon": "⚙️",
        "function": "Gestion des employés",
        "endpoint": "liste_users",  # ✅ EXISTE: /liste_users
        "category": "Administration"
    },
    "liste_succursales": {
        "name": "Gestion des succursales",
        "icon": "🏢",
        "function": "CRUD succursales",
        "endpoint": "liste_succursales",  # ✅ EXISTE: /admin/succursales
        "category": "Administration"
    },
    "admin_rapports": {
        "name": "Rapports",
        "icon": "📊",
        "function": "Génération de rapports",
        "endpoint": "admin_rapports",  # ✅ EXISTE: /admin/rapports
        "category": "Administration"
    },
    "statistiques_groupes": {
        "name": "Statistiques",
        "icon": "📈",
        "function": "Analyses",
        "endpoint": "statistiques_groupes",  # ✅ EXISTE: /api/statistiques-groupes
        "category": "Administration"
    },
    "admin_approbations": {
        "name": "Approbations",
        "icon": "⏳",
        "function": "Validation",
        "endpoint": "admin_approbations",  # ✅ EXISTE: /admin_central/approbations
        "category": "Administration"
    },
    "parametres": {
        "name": "Paramètres",
        "icon": "⚙️",
        "function": "Configuration",
        "endpoint": "parametres",  # ✅ EXISTE: /parametres
        "category": "Administration"
    },
    "liste_cartes": {
        "name": "Cartes des Employés",
        "icon": "💼",
        "function": "Gestion des cartes",
        "endpoint": "liste_cartes",  # ✅ EXISTE: /admin/cartes
        "category": "Administration"
    },
    "create_succursale": {
        "name": "Nouvelle Succursale",
        "icon": "🏢",
        "function": "Création",
        "endpoint": "create_succursale",  # ✅ EXISTE: /admin/create_succursale
        "category": "Administration"
    },
    "ajouter_admin": {
        "name": "Nouvel Admin",
        "icon": "👑",
        "function": "Création admin",
        "endpoint": "ajouter_admin",  # ✅ EXISTE: /admin/ajouter-admin
        "category": "Administration"
    },
    "ajouter_employe": {
        "name": "Nouvel Agent",
        "icon": "👨‍💼",
        "function": "Création employé",
        "endpoint": "ajouter_employe",  # ✅ EXISTE: /admin/ajouter-employe
        "category": "Administration"
    },
    "liste_employes": {
        "name": "Employés par succursale",
        "icon": "👥",
        "function": "Liste",
        "endpoint": "liste_employes",  # ✅ EXISTE: /admin/employes
        "category": "Administration"
    },
    "admin_employes": {
        "name": "Gestion des Employés",
        "icon": "👥",
        "function": "Gestion",
        "endpoint": "admin_employes",  # ✅ EXISTE: /admin/employes
        "category": "Administration"
    },
    "gerer_employes": {
        "name": "Gérer employés",
        "icon": "⚙️",
        "function": "Gestion avancée",
        "endpoint": "gerer_employes",  # ✅ EXISTE: /admin/gerer-employes
        "category": "Administration"
    },
    "historique_global": {
        "name": "Historique global",
        "icon": "📜",
        "function": "Audit des actions",
        "endpoint": "historique_global",  # ✅ EXISTE: /admin/historique
        "category": "Administration"
    },
    "gestion_retards": {
        "name": "Gestion des retards",
        "icon": "⏰",
        "function": "Suivi des retards",
        "endpoint": "gestion_retards",  # ✅ EXISTE: /admin/retards
        "category": "Administration"
    },
    "admin_remboursements": {
        "name": "Remboursements",
        "icon": "💵",
        "function": "Suivi des remboursements",
        "endpoint": "admin_remboursements",  # ✅ EXISTE: /admin/remboursements
        "category": "Administration"
    },

    # =============================================
    # EMPLOYÉS (Fonctions opérationnelles)
    # =============================================
    "caissier": {
        "name": "Caissier",
        "icon": "🏦",
        "function": "Gestion des remboursements",
        "endpoint": "caissier_dashboard",  # ✅ EXISTE: /<succursale_code>/caissier/dashboard
        "category": "Employés"
    },
    "analyste_credit": {
        "name": "Analyste crédit",
        "icon": "📊",
        "function": "Analyse des prêts",
        "endpoint": "analyste_dashboard",  # ✅ EXISTE: /employe/analyste
        "category": "Employés"
    },
    "conseiller": {
        "name": "Conseiller clientèle",
        "icon": "👥",
        "function": "Gestion clients",
        "endpoint": "conseiller_dashboard",  # ✅ EXISTE: /employe/conseiller
        "category": "Employés"
    },
    "gestionnaire_groupe": {
        "name": "Gestionnaire de groupes",
        "icon": "🎯",
        "function": "Gestion des groupes",
        "endpoint": "gestionnaire_dashboard",  # ✅ EXISTE: /employe/gestionnaire
        "category": "Employés"
    },
    "rapports": {
        "name": "Génération de rapports",
        "icon": "📈",
        "function": "Génération de rapports",
        "endpoint": "rapports_dashboard",  # ✅ EXISTE: /employe/rapports
        "category": "Employés"
    },
    "agent_credit": {
        "name": "Agent de crédit",
        "icon": "💰",
        "function": "Analyse et octroi de prêts",
        "endpoint": "agent_credit_dashboard",  # ✅ EXISTE: /<succursale_code>/agent-credit/dashboard
        "category": "Employés"
    },
    "superviseur_credit": {
        "name": "Superviseur crédit",
        "icon": "👨‍💼",
        "function": "Validation des prêts",
        "endpoint": "superviseur_credit_dashboard",  # ❌ N'EXISTE PAS - Utiliser chef_credit_dashboard
        "category": "Employés"
    },
    "gestionnaire_portefeuille": {
        "name": "Gestionnaire portefeuille",
        "icon": "📋",
        "function": "Suivi des prêts",
        "endpoint": "gestionnaire_portefeuille_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "conseiller_client": {
        "name": "Conseiller client",
        "icon": "👥",
        "function": "Accueil et orientation clients",
        "endpoint": "conseiller_dashboard",  # Gardez celui-ci
        "url": "/employe/conseiller",  # Ajoutez l'URL directe
        "category": "Employés"
    },
    "relation_client": {
        "name": "Relation client",
        "icon": "🤝",
        "function": "Fidélisation clients",
        "endpoint": "relation_client_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "animateur_groupe": {
        "name": "Animateur de groupe",
        "icon": "🎯",
        "function": "Formation clients",
        "endpoint": "animateur_groupe_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "caissier_principal": {
        "name": "Caissier principal",
        "icon": "💼",
        "function": "Supervision caisse",
        "endpoint": "caissier_principal_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "agent_remboursement": {
        "name": "Agent remboursement",
        "icon": "💵",
        "function": "Suivi échéances",
        "endpoint": "agent_remboursement_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "agent_saisie": {
        "name": "Agent saisie",
        "icon": "⌨️",
        "function": "Saisie données",
        "endpoint": "agent_saisie_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "agent_conformite": {
        "name": "Agent conformité",
        "icon": "🛡️",
        "function": "Vérifications AML/CFT",
        "endpoint": "agent_conformite_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "agent_risque": {
        "name": "Agent risque",
        "icon": "⚠️",
        "function": "Évaluation risques",
        "endpoint": "agent_risque_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "controlleur_interne": {
        "name": "Contrôleur interne",
        "icon": "🔍",
        "function": "Audit interne",
        "endpoint": "controlleur_interne_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "secretaire": {
        "name": "Secrétaire",
        "icon": "📋",
        "function": "Support administratif",
        "endpoint": "secretaire_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "archiviste": {
        "name": "Archiviste",
        "icon": "🗂️",
        "function": "Gestion dossiers",
        "endpoint": "archiviste_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "charge_rh": {
        "name": "Chargé RH",
        "icon": "👥",
        "function": "Gestion du personnel",
        "endpoint": "charge_rh_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "informaticien": {
        "name": "Informaticien",
        "icon": "💻",
        "function": "Support IT",
        "endpoint": "informaticien_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "agent_terrain": {
        "name": "Agent terrain",
        "icon": "🚗",
        "function": "Visites clients",
        "endpoint": "agent_terrain_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "collecteur": {
        "name": "Collecteur",
        "icon": "📦",
        "function": "Recouvrement terrain",
        "endpoint": "collecteur_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },
    "formateur": {
        "name": "Formateur",
        "icon": "🎓",
        "function": "Formation clients",
        "endpoint": "formateur_dashboard",  # ❌ N'EXISTE PAS
        "category": "Employés"
    },

    # =============================================
    # SUPERVISEURS (Gestion et supervision)
    # =============================================
    "chef_agence": {
        "name": "Chef d'agence",
        "icon": "🏢",
        "function": "Direction succursale",
        "endpoint": "chef_agence_dashboard",  # ✅ EXISTE: /superviseur/chef_agence/dashboard
        "category": "Superviseurs"
    },
    "superviseur_operations": {
        "name": "Superviseur opérations",
        "icon": "👨‍💼",
        "function": "Supervision équipe",
        "endpoint": "superviseur_operations_dashboard",  # ✅ EXISTE: /superviseur/operations/dashboard
        "category": "Superviseurs"
    },
    "chef_credit": {
        "name": "Chef crédit",
        "icon": "💰",
        "function": "Direction département crédit",
        "endpoint": "chef_credit_dashboard",  # ✅ EXISTE: /superviseurs/chef_credit/dashboard
        "category": "Superviseurs"
    },
    "responsable_conformite": {
        "name": "Responsable conformité",
        "icon": "🛡️",
        "function": "Direction conformité",
        "endpoint": "responsable_conformite_dashboard",  # ✅ EXISTE: /superviseurs/responsable_conformite/dashboard
        "category": "Superviseurs"
    },
    "coordinateur_terrain": {
        "name": "Coordinateur terrain",
        "icon": "🗺️",
        "function": "Supervision agents terrain",
        "endpoint": "coordinateur_terrain_dashboard",  # ✅ EXISTE: /direction/coordinateur_terrain/dashboard
        "category": "Superviseurs"
    },
    "directeur_regional": {
        "name": "Directeur régional",
        "icon": "🌍",
        "function": "Supervision multi-agences",
        "endpoint": "directeur_regional_dashboard",  # ✅ EXISTE: /direction/regional/dashboard
        "category": "Superviseurs"
    },

    # =============================================
    # DIRECTION (Haut management)
    # =============================================
    "directeur_general": {
        "name": "Directeur général",
        "icon": "👑",
        "function": "Direction générale",
        "endpoint": "directeur_general_dashboard",  # ✅ EXISTE: /direction/general/dashboard
        "category": "Direction"
    },
    "directeur_financier": {
        "name": "Directeur financier",
        "icon": "💼",
        "function": "Direction financière",
        "endpoint": "directeur_financier_dashboard",  # ✅ EXISTE: /direction/financier/dashboard
        "category": "Direction"
    },
    "directeur_operations": {
        "name": "Directeur opérations",
        "icon": "⚙️",
        "function": "Direction opérations",
        "endpoint": "directeur_operations_dashboard",  # ✅ EXISTE: /direction/operations/dashboard
        "category": "Direction"
    },
    "directeur_commercial": {
        "name": "Directeur commercial",
        "icon": "📈",
        "function": "Développement commercial",
        "endpoint": "directeur_commercial_dashboard",  # ✅ EXISTE: /direction/commercial/dashboard
        "category": "Direction"
    },
    "directeur_rh": {
        "name": "Directeur RH",
        "icon": "👥",
        "function": "Ressources humaines",
        "endpoint": "directeur_rh_dashboard",  # ✅ EXISTE: /direction/rh/dashboard
        "category": "Direction"
    },
    "directeur_conformite": {
        "name": "Directeur conformité",
        "icon": "🛡️",
        "function": "Conformité BRH",
        "endpoint": "directeur_conformite_dashboard",  # ✅ EXISTE: /direction/conformite/dashboard
        "category": "Direction"
    },

    # =============================================
    # SUPER ADMIN (Spécifique)
    # =============================================
    "super_admin_switcher": {
        "name": "Super Admin - Interface",
        "icon": "🔓",
        "function": "Accès total au système",
        "endpoint": "super_admin.switcher",  # ✅ EXISTE: /super_admin
        "category": "Super Admin"
    },
    "audit_logs": {
        "name": "Audit Logs",
        "icon": "📝",
        "function": "Journal des accès",
        "endpoint": "audit_logs",  # ✅ EXISTE: /super-admin/audit-logs
        "category": "Super Admin"
    },

    # =============================================
    # FONCTIONS GÉNÉRIQUES (Pages communes)
    # =============================================
    "creer_dossier": {
        "name": "Créer un dossier",
        "icon": "📁",
        "function": "Ouverture de compte",
        "endpoint": "creer_dossier",  # ✅ EXISTE: /conseiller/creer-dossier
        "category": "Général"
    },
    "mes_dossiers": {
        "name": "Mes dossiers",
        "icon": "📋",
        "function": "Gestion des dossiers",
        "endpoint": "conseiller_mes_dossiers",  # ✅ EXISTE: /conseiller/mes-dossiers
        "category": "Général"
    },
    "liste_groupes": {
        "name": "Liste des groupes",
        "icon": "👥",
        "function": "Gestion des groupes",
        "endpoint": "liste_groupes",  # ✅ EXISTE: /liste_groupes
        "category": "Général"
    },
    "mes_groupes": {
        "name": "Mon groupe",
        "icon": "🤝",
        "function": "Gestion du groupe",
        "endpoint": "mes_groupes",  # ✅ EXISTE: /mes-groupes
        "category": "Général"
    },
    "demande_pret": {
        "name": "Nouveau prêt",
        "icon": "💰",
        "function": "Demande de prêt",
        "endpoint": "demande_pret",  # ✅ EXISTE: /prets/demande-pret
        "category": "Général"
    },
    "rechercher_client": {
        "name": "Rechercher client",
        "icon": "🔍",
        "function": "Recherche et transactions",
        "endpoint": "rechercher_client",  # ✅ EXISTE: /rechercher-client
        "category": "Général"
    },
    "effectuer_retrait": {
        "name": "Effectuer retrait",
        "icon": "🏧",
        "function": "Opérations de retrait",
        "endpoint": "effectuer_retrait",  # ✅ EXISTE: /effectuer-retrait
        "category": "Général"
    },
    "effectuer_transfert": {
        "name": "Effectuer transfert",
        "icon": "💸",
        "function": "Transferts d'argent",
        "endpoint": "effectuer_transfert",  # ✅ EXISTE: /effectuer-transfert
        "category": "Général"
    },
    "effectuer_depot": {
        "name": "Effectuer dépôt",
        "icon": "🏦",
        "function": "Opérations de dépôt",
        "endpoint": "effectuer_depot",  # ✅ EXISTE: /effectuer-depot
        "category": "Général"
    },
    "prets_en_attente": {
        "name": "Prêts en attente",
        "icon": "⏳",
        "function": "Validation des prêts",
        "endpoint": "prets_en_attente",  # ✅ EXISTE: /prets-en-attente
        "category": "Général"
    },
    "remboursements_retards": {
        "name": "Remboursements en retard",
        "icon": "⚠️",
        "function": "Suivi des retards",
        "endpoint": "remboursements_retards",  # ✅ EXISTE: /<succursale_code>/remboursements/retards
        "category": "Général"
    },
    "mes_remboursements": {
        "name": "Mes remboursements",
        "icon": "💳",
        "function": "Suivi des remboursements",
        "endpoint": "mes_remboursements",  # ✅ EXISTE: /mes-remboursements
        "category": "Général"
    },
    "notifications": {
        "name": "Notifications",
        "icon": "🔔",
        "function": "Voir les notifications",
        "endpoint": "notifications",  # ✅ EXISTE: /notifications
        "category": "Général"
    },
    "profil": {
        "name": "Mon profil",
        "icon": "👤",
        "function": "Gestion du profil",
        "endpoint": "profil",  # ✅ EXISTE: /profil
        "category": "Général"
    },
    "tableau_de_bord": {
        "name": "Tableau de bord",
        "icon": "📊",
        "function": "Tableau de bord général",
        "endpoint": "tableau_de_bord",  # ✅ EXISTE: /tableau-de-bord
        "category": "Général"
    },
    "simulateur_credit": {
        "name": "Simulateur crédit",
        "icon": "🧮",
        "function": "Simulation de prêt",
        "endpoint": "simulateur_credit",  # ✅ EXISTE: /simulateur-credit
        "category": "Général"
    },
    "conseiller_mes_dossiers": {
        "name": "Mes dossiers",
        "icon": "📋",
        "function": "Gestion des dossiers",
        "endpoint": "conseiller_mes_dossiers",  # ✅ EXISTE: /conseiller/mes-dossiers
        "category": "Général"
    },
    "conseiller_dossier_en_attente": {
        "name": "Dossiers en attente",
        "icon": "⏳",
        "function": "Dossiers à traiter",
        "endpoint": "conseiller_dossier_en_attente",  # ✅ EXISTE: /conseiller/dossiers-en-attente
        "category": "Général"
    },
    "conseiller_voir_dossier": {
        "name": "Voir dossier",
        "icon": "👁️",
        "function": "Détails du dossier",
        "endpoint": "conseiller_voir_dossier",  # ✅ EXISTE: /conseiller/dossier/<int:dossier_id>
        "category": "Général"
    },
    "modifier_client": {
        "name": "Modifier client",
        "icon": "✏️",
        "function": "Édition client",
        "endpoint": "modifier_client",  # ✅ EXISTE: /agent/client/<int:client_id>/modifier
        "category": "Général"
    },
    "voir_client": {
        "name": "Voir client",
        "icon": "👤",
        "function": "Détails client",
        "endpoint": "voir_client",  # ✅ EXISTE: /agent/client/<int:client_id>
        "category": "Général"
    }
}

# =============================================
# LISTE DES ENDPOINTS QUI N'EXISTENT PAS
# =============================================
ENDPOINTS_MANQUANTS = {
    "superviseur_credit_dashboard": "❌ Utiliser 'chef_credit_dashboard' à la place",
    "gestionnaire_portefeuille_dashboard": "❌ Pas d'équivalent direct",
    "relation_client_dashboard": "❌ Pas d'équivalent direct",
    "animateur_groupe_dashboard": "❌ Pas d'équivalent direct",
    "caissier_principal_dashboard": "❌ Pas d'équivalent direct",
    "agent_remboursement_dashboard": "❌ Pas d'équivalent direct",
    "agent_saisie_dashboard": "❌ Pas d'équivalent direct",
    "agent_conformite_dashboard": "❌ Pas d'équivalent direct",
    "agent_risque_dashboard": "❌ Pas d'équivalent direct",
    "controlleur_interne_dashboard": "❌ Pas d'équivalent direct",
    "secretaire_dashboard": "❌ Pas d'équivalent direct",
    "archiviste_dashboard": "❌ Pas d'équivalent direct",
    "charge_rh_dashboard": "❌ Pas d'équivalent direct",
    "informaticien_dashboard": "❌ Pas d'équivalent direct",
    "agent_terrain_dashboard": "❌ Pas d'équivalent direct",
    "collecteur_dashboard": "❌ Pas d'équivalent direct",
    "formateur_dashboard": "❌ Pas d'équivalent direct",
}
print(f"📊 TOTAL PAGES: {len(PAGES)}")
# =============================================
# SUPPRIMEZ ICI TOUTES LES ROUTES @app.route
# =============================================
# Les routes seront déplacées dans super_admin_bp.py


