# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict

import jwt
# from decouple import config
from app.config import SECRET_KEY, ALGORITHM

# JWT_SECRET = config("secret")
# JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}