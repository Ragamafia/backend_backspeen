import jwt
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException

from src.db.ctrl import db
from src.logger import logger
from src.server.api.requests import NewUserRequest, NewUserResponse, LoginRequest, TokenRequest
from config import cfg


def register_router(app):
    router = APIRouter()

    @router.post("/register")
    async def create_user(request: NewUserRequest):
        if user := await db.get_user(request.email):
            logger.warning(f"User {user.name} already exists")
        else:
            await db.create(request.name, request.last_name, request.email, request.password)

    @router.post("/login")
    async def login(request: LoginRequest):
        if user := await db.read(request.email, request.password):
            token = create_token(user.id)
            user.is_active = True
            await user.save()

            logger.success(f"User {request.email} logged in")
            return {"access_token": token, "token_type": "bearer"}
        else:
            logger.warning(f"User not found")
            return NewUserResponse(success=False, result=None)

    @router.post("/users/me")
    async def get_user(request: TokenRequest):
        if request is None:
            raise HTTPException(status_code=401, detail="Token missing")
        user_id = verify_token(request)
        return await db.get_user_by_id(user_id)


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

    app.app.include_router(router)