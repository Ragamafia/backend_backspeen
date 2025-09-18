import jwt
from datetime import datetime, timedelta

from fastapi import Request, HTTPException, Depends

from config import cfg


def create_token(user_id: int, session_id: str):
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {
        "user_id": user_id,
        "exp": expire,
        "session_id": session_id,
    }
    return jwt.encode(to_encode, cfg.secret_key, algorithm=cfg.algorithm)

def token_from_headers(request: Request):
    try:
        return request.headers.get("Authorization").split(" ")[1]
    except:
        ...

def decode(request: Request):
    if not request:
        return

    token = token_from_headers(request) or request.cookies.get("token")
    decoded = jwt.decode(token, cfg.secret_key, algorithms=[cfg.algorithm])
    if isinstance(decoded, dict):
        return decoded

async def is_authorize(request: Request):
    db = request.app.db
    token = decode(request)
    if isinstance(token, dict):
        if user := await db.get_user_by_id(token.get("user_id")):
            try:
                if await db.validate_session(user.id, token.get("session_id")):
                    return user
            except:
                raise HTTPException(status_code=401, detail="No session ID")

    raise HTTPException(status_code=401, detail="Bad token")

async def is_admin(user=Depends(is_authorize)):
    if user.role == "admin":
        return user
    raise HTTPException(status_code=401, detail="Not admin")
