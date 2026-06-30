# create_succursale.py
import sys
import os
from app import app, db
from models import Succursale


def create_succursale():
    """Crée une nouvelle succursale"""
    with app.app_context():
        print("🏢 CRÉATION D'UNE SUCCURSALE")
        print("=" * 40)

        # Données de la succursale
        code = input("Code de la succursale (ex: CAS001) : ").strip() or "CAS001"
        nom = input("Nom de la succursale : ").strip() or "Succursale Principale"
        ville = input("Ville : ").strip() or "Casablanca"
        adresse = input("Adresse : ").strip() or "123 Avenue Hassan II"
        telephone = input("Téléphone : ").strip() or "0522-123456"
        email = input("Email : ").strip() or f"contact@{code.lower()}.gmes.ma"

        # Vérifier si le code existe déjà
        existing = Succursale.query.filter_by(code=code).first()
        if existing:
            print(f"❌ La succursale avec le code '{code}' existe déjà!")
            print(f"   Nom: {existing.nom}")
            print(f"   Ville: {existing.ville}")
            return

        # Créer la succursale
        succursale = Succursale(
            code=code,
            nom=nom,
            adresse=adresse,
            ville=ville,
            telephone=telephone,
            email=email,
            statut="active"
        )

        db.session.add(succursale)
        db.session.commit()

        print("\n✅ SUCCURSALE CRÉÉE AVEC SUCCÈS!")
        print(f"   Code: {code}")
        print(f"   Nom: {nom}")
        print(f"   Ville: {ville}")
        print(f"   Adresse: {adresse}")
        print(f"   Téléphone: {telephone}")
        print(f"   Email: {email}")

        # Option: créer un admin pour cette succursale
        create_admin = input("\nCréer un administrateur pour cette succursale ? (o/N) : ").lower()
        if create_admin in ['o', 'oui', 'y', 'yes']:
            create_admin_for_succursale(succursale.id)


def create_admin_for_succursale(succursale_id):
    """Crée un admin pour une succursale"""
    from models import User
    from werkzeug.security import generate_password_hash

    succursale = Succursale.query.get(succursale_id)
    if not succursale:
        print("❌ Succursale non trouvée")
        return

    print(f"\n👑 CRÉATION ADMIN POUR {succursale.code}")
    print("-" * 30)

    username = input(
        f"Nom d'utilisateur (suggestion: admin_{succursale.code.lower()}) : ").strip() or f"admin_{succursale.code.lower()}"
    email = input(
        f"Email (suggestion: admin.{succursale.code.lower()}@gmes.ma) : ").strip() or f"admin.{succursale.code.lower()}@gmes.ma"
    password = input("Mot de passe : ").strip() or "admin123"

    # Vérifier si l'utilisateur existe déjà
    existing = User.query.filter_by(username=username).first()
    if existing:
        print(f"❌ L'utilisateur '{username}' existe déjà!")
        return

    # Créer l'admin
    admin = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role="admin",
        succursale_id=succursale.id,
        statut="actif",
        terms_accepted=True
    )

    db.session.add(admin)
    db.session.commit()

    print(f"\n✅ ADMIN CRÉÉ AVEC SUCCÈS!")
    print(f"   👤 Username: {username}")
    print(f"   📧 Email: {email}")
    print(f"   🏢 Succursale: {succursale.nom} ({succursale.code})")
    print(f"   🔑 Password: {password}")


def list_succursales():
    """Affiche toutes les succursales"""
    with app.app_context():
        succursales = Succursale.query.all()

        if not succursales:
            print("ℹ️  Aucune succursale trouvée")
            return

        print("\n📋 LISTE DES SUCCURSALES")
        print("=" * 60)

        for i, succ in enumerate(succursales, 1):
            print(f"\n{i}. {succ.nom} ({succ.code})")
            print(f"   📍 {succ.adresse}, {succ.ville}")
            print(f"   📞 {succ.telephone}")
            print(f"   📧 {succ.email}")
            print(f"   📊 Statut: {succ.statut}")

            # Compter les utilisateurs de cette succursale
            from models import User
            users = User.query.filter_by(succursale_id=succ.id).all()
            if users:
                print(f"   👥 Utilisateurs: {len(users)}")
                for user in users:
                    print(f"      - {user.username} ({user.role})")


def create_multiple_succursales():
    """Crée plusieurs succursales de test"""
    with app.app_context():
        print("🏗️  CRÉATION DE SUCCURSALES DE TEST")
        print("=" * 50)

        succursales_data = [
            {
                "code": "CAS001",
                "nom": "Casablanca Centre",
                "ville": "Casablanca",
                "adresse": "123 Boulevard Mohammed V",
                "telephone": "0522-123456",
                "email": "contact.casablanca@gmes.ma"
            },
            {
                "code": "RAB002",
                "nom": "Rabat Agdal",
                "ville": "Rabat",
                "adresse": "45 Avenue Hassan II",
                "telephone": "0537-789012",
                "email": "contact.rabat@gmes.ma"
            },
            {
                "code": "MAR003",
                "nom": "Marrakech Médina",
                "ville": "Marrakech",
                "adresse": "78 Rue de la Koutoubia",
                "telephone": "0524-345678",
                "email": "contact.marrakech@gmes.ma"
            },
            {
                "code": "FES004",
                "nom": "Fès Ville Nouvelle",
                "ville": "Fès",
                "adresse": "56 Avenue Hassan I",
                "telephone": "0535-901234",
                "email": "contact.fes@gmes.ma"
            }
        ]

        created_count = 0
        for data in succursales_data:
            # Vérifier si existe déjà
            existing = Succursale.query.filter_by(code=data["code"]).first()
            if existing:
                print(f"⚠️  {data['code']} existe déjà")
                continue

            # Créer la succursale
            succursale = Succursale(
                code=data["code"],
                nom=data["nom"],
                adresse=data["adresse"],
                ville=data["ville"],
                telephone=data["telephone"],
                email=data["email"],
                statut="active"
            )

            db.session.add(succursale)
            created_count += 1

        db.session.commit()

        print(f"\n✅ {created_count} succursales créées avec succès!")

        # Créer des admins pour chaque succursale
        create_admins = input("\nCréer des administrateurs pour chaque succursale ? (o/N) : ").lower()
        if create_admins in ['o', 'oui', 'y', 'yes']:
            from models import User
            from werkzeug.security import generate_password_hash

            for data in succursales_data:
                succursale = Succursale.query.filter_by(code=data["code"]).first()
                if succursale:
                    admin = User(
                        username=f"admin_{data['code'].lower()}",
                        email=f"admin.{data['code'].lower()}@gmes.ma",
                        password_hash=generate_password_hash("admin123"),
                        role="admin",
                        succursale_id=succursale.id,
                        statut="actif",
                        terms_accepted=True
                    )
                    db.session.add(admin)

            db.session.commit()
            print("✅ Administrateurs créés pour chaque succursale")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🏢 GESTION DES SUCCURSALES - GMES MICROCRÉDIT")
    print("=" * 60)

    print("\nOptions disponibles :")
    print("1. ➕ Créer une nouvelle succursale")
    print("2. 📋 Lister toutes les succursales")
    print("3. 🏗️  Créer plusieurs succursales de test")
    print("4. ❌ Quitter")

    choice = input("\nVotre choix (1-4) : ").strip()

    if choice == "1":
        create_succursale()
    elif choice == "2":
        list_succursales()
    elif choice == "3":
        create_multiple_succursales()
    elif choice == "4":
        print("Au revoir!")
    else:
        print("❌ Choix invalide")