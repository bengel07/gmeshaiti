import os
from app import app, db
from models import User, Client

with app.app_context():  # ← AJOUTE CETTE LIGNE
    # 1. Compter les clients
    clients = Client.query.filter_by(role='client').all()
    print(f"📊 {len(clients)} client(s) trouvé(s)")
    db.session.commit()
    print(f"✅ {len(clients)} client(s) supprimés!")
