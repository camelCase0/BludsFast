import hashlib
from app.config import SECRET_KEY


def get_password_hash(password:str) -> str:
    return hashlib.sha256(f'{SECRET_KEY}{password}'.encode('utf8')).hexdigest()