from flask import abort
from models import Client

def verifier_acceptation(client_id):
    client = Client.query.get(client_id)
    if not client or not client.terms_accepted:
        abort(403, "Le client n'a pas accepté les conditions")
    return True
