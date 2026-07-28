from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    from models import User

    with app.app_context():
        # Voir les utilisateurs en attente
        users = User.query.filter_by(role='client', statut='en_attente_approbation').all()

        print(f"🔴 {len(users)} utilisateur(s) en attente trouvé(s)")

        for user in users:
            print(f"  - {user.nom} {user.prenom} (ID: {user.id}) - {user.email}")
            # Corriger le statut
            user.statut = 'actif'
            print(f"    ✅ Statut changé en 'actif'")

        # Sauvegarder
        db.session.commit()

        # Vérifier
        restant = User.query.filter_by(role='client', statut='en_attente_approbation').count()
        print(f"\n✅ Après correction : {restant} utilisateur(s) en attente")


