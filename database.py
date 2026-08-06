from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

    with app.app_context():


        db.drop_all()
        db.create_all()

        print("✅ Toutes les tables ont été recréées.")