from app import app, db
from sqlalchemy import text

from app import app, db

with app.app_context():
    db.create_all()
    print("✅ Tables manquantes créées.")