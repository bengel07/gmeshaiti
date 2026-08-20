from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)


def attribuer_id_clients_existants():
    from models import Client

    clients = Client.query.filter(
        (Client.id_client.is_(None)) |
        (Client.id_client == '')
    ).all()

    for client in clients:
        client.id_client = f"CLI-{client.id:06d}"

    db.session.commit()

    return len(clients)