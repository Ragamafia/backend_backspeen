from datetime import datetime, timedelta

import jwt
from fastapi import FastAPI, Response, Cookie, HTTPException

from server.api.users import NewUserRequest, NewUserResponse, LoginRequest
from db.ctrl import db
from logger import logger
from config import cfg


app = FastAPI()


@app.post("/register")
async def create_user(request: NewUserRequest):
    if user := await db.get_user(request.email):
        logger.warning(f"User {user.name} already exists")
    else:
        await db.create(request.name, request.last_name, request.email, request.password)
        logger.info(f"User {request.name} created")


@app.post("/login")
async def login(request: LoginRequest, response: Response):
    if user := await db.read(request.email, request.password):
        user_data = await user.first().values()
        token = generate_access_token(user_data, timedelta(minutes=cfg.ACCESS_TOKEN_EXPIRE))
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,  # for testing only
            samesite="lax"
        )
        user.is_active = True
        await user.save()

        logger.success(f"User {request.email} logged in")
        return {"access_token": token}

    else:
        logger.warning(f"User not found")
        return NewUserResponse(success=False, result=None)

@app.get("/protected")
def protected_route(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(access_token, cfg.SECRET_KEY, algorithms=[cfg.ALGORITHM])
        name = payload.get("sub")
        return {"name": name}

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def generate_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, cfg.SECRET_KEY, algorithm=cfg.ALGORITHM)