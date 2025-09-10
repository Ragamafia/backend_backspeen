import jwt
from datetime import datetime, timedelta

from config import cfg


def create_token(user_id: int):
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {"user_id": user_id, "exp": expire}
    return jwt.encode(to_encode, cfg.SECRET_KEY, algorithm=cfg.ALGORITHM)


def verify_token(token):
    token = token.access_token
    try:
        payload = jwt.decode(token, cfg.SECRET_KEY, algorithms=[cfg.ALGORITHM])
        return payload.get("user_id")

    except jwt.PyJWTError:
        return None