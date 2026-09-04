init_db(app)

with app.app_context():
    creer_produit_epargne_defaut()

    db.create_all()

    print("✅ Tables vérifiées/créées")

    # Vérifier les clients disponibles
    client_admin = Client.query.first()

    print(
        f"👤 Client disponible : {client_admin.id}"
        if client_admin
        else "⚠️ Aucun client dans la base"
    )