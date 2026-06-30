import uuid
import hashlib

def generate_reference(prefix="TXN"):
    return f"{prefix}_{uuid.uuid4().hex[:10].upper()}"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
