import hashlib
import re
from flask import current_app


def hash_password(password):
    """Hash un mot de passe avec SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def validate_password(password):
    """Valide la force du mot de passe"""
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"

    if not re.search(r"[A-Z]", password):
        return False, "Le mot de passe doit contenir au moins une majuscule"

    if not re.search(r"[a-z]", password):
        return False, "Le mot de passe doit contenir au moins une minuscule"

    if not re.search(r"\d", password):
        return False, "Le mot de passe doit contenir au moins un chiffre"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Le mot de passe doit contenir au moins un caractère spécial"

    return True, "Mot de passe valide"


def validate_phone(phone):
    """Valide le format du numéro de téléphone"""
    # Format international ou local
    pattern = r'^(\+?\d{1,4}?[-.\s]?)?(\(?\d{1,4}?\)?[-.\s]?)?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
    return re.match(pattern, phone) is not None


def validate_email(email):
    """Valide le format de l'email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# utils/security.py

def filtrer_par_role(users, role):
    """
    Filtre une liste d'utilisateurs par rôle.

    Args:
        users: Liste d'objets User ou Employe
        role: Le rôle à filtrer (ex: 'admin', 'employe', 'client')

    Returns:
        Liste filtrée des utilisateurs avec ce rôle
    """
    if not users:
        return []

    # Si c'est une liste d'objets User
    if hasattr(users[0], 'role'):
        return [u for u in users if u.role == role]

    # Si c'est une liste d'objets Employe
    elif hasattr(users[0], 'poste'):
        return [u for u in users if u.poste == role]

    # Si c'est une liste d'objets avec un attribut 'role' différent
    else:
        return [u for u in users if getattr(u, 'role', None) == role]


#
# # Dans utils/security.py, ajoute :
# def filtrer_par_role(users, role):
#     """
#     Filtre une liste d'utilisateurs par rôle
#     """
#     if not users:
#         return []
#     return [user for user in users if getattr(user, 'role', None) == role]
#
#
# # OU une version plus complète :
# def filtrer_par_role(users, role):
#     """Filtre les utilisateurs par rôle."""
#     if not users:
#         return []
#
#     filtered_users = []
#     for user in users:
#         user_role = getattr(user, 'role', None) or getattr(user, 'type', None)
#         if user_role == role:
#             filtered_users.append(user)
#
#     return filtered_users

# Dans utils/security.py
def filtrer_par_role(users, role=None):
    """
    Filtre une liste d'utilisateurs par rôle
    Si role est None, retourne tous les utilisateurs
    """
    if not users:
        return []

    if role is None:
        return users

    return [user for user in users if getattr(user, 'role', None) == role]