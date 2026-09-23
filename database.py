from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()

        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS notifications_client (
                id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL,
                titre VARCHAR(150) NOT NULL,
                message TEXT NOT NULL,
                type VARCHAR(30) DEFAULT 'info',
                lien VARCHAR(255),
                lue BOOLEAN DEFAULT FALSE,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_notifications_client_client
                    FOREIGN KEY (client_id)
                    REFERENCES clients(id)
                    ON DELETE CASCADE
            )
        """))

        db.session.commit()