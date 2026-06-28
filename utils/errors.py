from sqlalchemy.exc import IntegrityError

def humanize_unique_error(error):
    """
    Transforme une erreur UNIQUE en message clair et universel
    """
    message = str(error.orig)

    if "UNIQUE constraint failed:" not in message:
        return "Une erreur est survenue lors de l’enregistrement."

    # Exemple: UNIQUE constraint failed: admins.email
    field = message.split(":")[-1].strip()

    column = field.split(".")[-1]

    labels = {
        "email": "cet email",
        "telephone": "ce numéro de téléphone",
        "phone": "ce numéro de téléphone",
        "nom_utilisateur": "ce nom d’utilisateur",
        "username": "ce nom d’utilisateur",
        "cin": "ce numéro d’identification",
        "nif": "ce NIF",
        "id": "cet identifiant",
        "code": "ce code",
    }

    readable = labels.get(column, f"cette information ({column})")

    return f"❌ {readable.capitalize()} est déjà utilisé par une autre personne."
