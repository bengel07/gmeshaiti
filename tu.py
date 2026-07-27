from app import app
from models import User

with app.app_context():

    admin = User.query.filter_by(role="admin_succursale").first()

    if not admin:
        print("❌ Aucun admin_succursale trouvé.")
    else:
        print("=" * 60)
        print("ID          :", admin.id)
        print("Nom         :", admin.nom, admin.prenom)
        print("Email       :", admin.email)
        print("Role        :", admin.role)
        print("Fonction    :", admin.fonction)
        print("Statut      :", admin.statut)
        print("Succursale  :", admin.succursale_id)

        if admin.succursale:
            print("Code        :", admin.succursale.code)
            print("Dashboard   :", f"/{admin.succursale.code}/dashboard")
        else:
            print("❌ Aucune succursale assignée.")

        print("=" * 60)