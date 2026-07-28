from app import app, db
from models import User

with app.app_context():
    # Compter les users en attente
    count = User.query.filter_by(role='client', statut='en_attente_approbation').count()
    print(f"📊 Nombre d'utilisateurs en attente : {count}")

    # Lister les users en attente
    users = User.query.filter_by(role='client', statut='en_attente_approbation').all()
    for user in users:
        print(f"  - {user.id} | {user.nom} {user.prenom} | {user.email}")