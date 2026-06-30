from itsdangerous import URLSafeTimedSerializer
from flask import current_app
import sqlite3
def generate_terms_token(client_id):
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return s.dumps(client_id, salt="terms-accept")

def verify_terms_token(token, max_age=86400):  # 24h
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return s.loads(token, salt="terms-accept", max_age=max_age)

