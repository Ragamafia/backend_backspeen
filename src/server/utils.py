import jwt
from datetime import datetime, timedelta

from fastapi import Request

from config import cfg


def create_token(user_id: int):
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {"user_id": user_id, "exp": expire}
    return jwt.encode(to_encode, cfg.SECRET_KEY, algorithm=cfg.ALGORITHM)

def token_from_headers(request: Request):
    try:
        return request.headers.get("Authorization").split(" ")[1]
    except:
        ...

def decode(request: Request):
    if not request:
        return

    token = token_from_headers(request) or request.cookies.get("token")
    decoded = jwt.decode(token, cfg.SECRET_KEY, algorithms=[cfg.ALGORITHM])
    if isinstance(decoded, dict):
        return decoded
