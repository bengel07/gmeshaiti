"""Droits d'accès par rôle et par fonction (séparation des tâches).

Votre table des utilisateurs a deux colonnes : `role` ('super_admin', 'direction', 'employe') et,
pour un employé, `fonction`. Voici les CODES de fonction à enregistrer dans `User.fonction` :

    conseiller    Agent de crédit (conseiller)
    analyste      Analyste de crédit
    caissier      Caissier(ère)
    comptable     Comptable
    recouvrement  Agent de recouvrement
    conformite    Responsable conformité / contrôle interne
    accueil       Réception / service client

Principe : un employé n'a que les droits de SA fonction. Les tâches incompatibles sont réparties :
le conseiller crée le dossier, le caissier manipule l'argent, le comptable contrôle sans toucher à la
caisse, la direction approuve et clôture.

Pour changer un droit, modifiez uniquement la table PERMISSIONS ci-dessous.
Ce module est du Python pur : aucune dépendance à Flask ni à la base de données.
"""

import re
import unicodedata

FONCTIONS = {
    "conseiller": "Agent de crédit (conseiller)",
    "analyste": "Analyste de crédit",
    "caissier": "Caissier(ère)",
    "comptable": "Comptable",
    "recouvrement": "Agent de recouvrement",
    "conformite": "Responsable conformité / contrôle interne",
    "accueil": "Réception / service client",
}

ROLES = {
    "super_admin": "Administrateur général",
    "direction": "Direction",
    "employe": "Employé (voir sa fonction)",
}

# permission -> ensemble de « clés » autorisées. Clé = rôle, ou "employe:<fonction>" pour un employé.
PERMISSIONS = {
    # Configuration des produits d'épargne
    "produit.configurer": {"super_admin"},
    # Création d'un dossier client (votre route creer_dossier : conseiller ou super_admin)
    "dossier.creer": {"super_admin", "employe:conseiller"},
    # Consulter un compte et son relevé (lecture seule)
    "compte.consulter": {"super_admin", "direction", "employe:conseiller", "employe:analyste",
                         "employe:caissier", "employe:comptable", "employe:conformite"},
    # Opérations d'argent : le caissier, et la direction en secours
    # (retirez "direction" pour une séparation stricte : seul le caissier touche à la caisse)
    "compte.activer": {"super_admin", "direction", "employe:caissier"},
    "compte.deposer": {"super_admin", "direction", "employe:caissier"},
    "compte.retirer": {"super_admin", "direction", "employe:caissier"},
    # Clôture : décision de la direction
    "compte.cloturer": {"super_admin", "direction"},
    # Rapports financiers et contrôle d'intégrité
    "rapport.consulter": {"super_admin", "direction", "employe:comptable", "employe:conformite"},
}

# opération de l'API -> permission requise
PERMISSION_OPERATION = {
    "activation": "compte.activer",
    "depot": "compte.deposer",
    "retrait": "compte.retirer",
    "cloture": "compte.cloturer",
}


# Noms de fonction déjà présents dans votre application -> code utilisé dans PERMISSIONS.
# Une fonction absente de FONCTIONS et de cette table n'a AUCUN droit sur l'épargne.
ALIAS_FONCTIONS = {
    "agent_remboursement": "recouvrement",
    "agent_conformite": "conformite",
    "responsable_conformite": "conformite",
    "controlleur_interne": "conformite",
    "controleur_interne": "conformite",
    "secretaire": "accueil",
    "relation_client": "accueil",
}


def normaliser_fonction(valeur):
    """'Agent-Remboursement ' -> 'agent_remboursement' (minuscules, sans accents, '_' comme séparateur)."""
    brut = unicodedata.normalize("NFKD", str(valeur or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", brut.lower()).strip("_")


def cle(utilisateur):
    """'super_admin', 'direction' ou 'employe:<fonction>' ; None si l'utilisateur est inconnu."""
    role = getattr(utilisateur, "role", None)
    if role == "employe":
        fonction = normaliser_fonction(getattr(utilisateur, "fonction", None))
        fonction = ALIAS_FONCTIONS.get(fonction, fonction)
        return f"employe:{fonction}" if fonction else None
    return role


def a_permission(utilisateur, permission):
    if permission not in PERMISSIONS:
        raise KeyError(f"Permission inconnue : {permission}")
    return cle(utilisateur) in PERMISSIONS[permission]


def permissions_de(utilisateur):
    return {p for p, autorises in PERMISSIONS.items() if cle(utilisateur) in autorises}


def fonction_valide(code):
    return code in FONCTIONS