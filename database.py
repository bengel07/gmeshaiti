from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from models import *
db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        print("📦 Modèles SQLAlchemy chargés :")
        for table in db.metadata.sorted_tables:
            print(f"   ✅ {table.name}")

        db.create_all()

        print("✅ Toutes les tables ont été créées.")