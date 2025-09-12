from fastapi import APIRouter, Request, HTTPException, Depends

from src.server.utils import create_token, decode
from src.server.api.models import (User,
                                   NewUserRequest,
                                   LoginRequest,
                                   LoginResponse,
                                   LogoutRequest,
                                   LogoutResponse,
                                   AuthorizeRequest,
                                   AuthorizeResponse)
from src.logger import logger


def register_users_router(app):
    users_router = APIRouter(
        tags=["Users"],
        prefix="/api/users"
    )
    async def is_authorize(request: Request):
        token = decode(request)
        if isinstance(token, dict):
            if user := await app.db.get_user(token.get("user_id")):
                return user

        raise HTTPException(status_code=401, detail="Bad token")

    @users_router.post("/register")
    async def create_user(request: NewUserRequest):
        if user := await app.db.read(request.email, request.password):
            logger.warning(f"User {user.name} already exists")
            return user
        else:
            user = await app.db.create(request.name, request.last_name, request.email, request.password)
            logger.info(f"User {request.email} created")
            return user

    @users_router.post("/me")
    async def auth(user: User = Depends(is_authorize)):
        return user

    @users_router.post("/login")
    async def login(request: LoginRequest):
        if user := await app.db.read(request.email, request.password):
            token = create_token(user.id)
            data = {"access_token": token, "token_type": "bearer"}
            logger.success(f"User {user.email} logged in")
            return LoginResponse(success=True, data=data)
        else:
            logger.warning(f"User {request.email} not found")
            return LoginResponse(success=False, data={})

    @users_router.post("/logout")
    async def logout(request: dict, user: User = Depends(is_authorize)):
        if user:
            return LogoutResponse(success=False, data=request)


    app.app.include_router(users_router)