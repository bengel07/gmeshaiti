from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        # IMPORTANT :
        # charger les modèles APRÈS que db existe
        import models

        print("========================================")
        print("📦 MODÈLES SQLALCHEMY CHARGÉS")
        print("========================================")

        for table in db.metadata.sorted_tables:
            print(f"   ✅ {table.name}")

        print("========================================")
        print(f"📊 TOTAL : {len(db.metadata.tables)} tables")
        print("========================================")

        db.create_all()

        print("========================================")
        print("✅ TOUTES LES TABLES ONT ÉTÉ CRÉÉES/VÉRIFIÉES")
        print("========================================")