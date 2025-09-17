import uuid
from fastapi import APIRouter, Depends, Request

from src.models import User
from src.server.utils import create_token, is_authorize, decode
from src.server.api.models import NewUserRequest, LoginRequest, Ok, NoAccess, Error

from logger import logger


def register_users_router(app):
    users_router = APIRouter(
        tags=["Users"],
        prefix="/api/users"
    )

    @users_router.post("/register")
    async def create_user(request: NewUserRequest):
        return await app.db.ensure_user(request.model_dump())

    @users_router.post("/login")
    async def login(request: LoginRequest):
        if user := await app.db.get_user(request.email, request.password):
            if user.is_active:
                session_id = str(uuid.uuid4())
                token = create_token(user.id, session_id)
                data = {"access_token": token, "token_type": "bearer"}
                logger.success(f"User {user.name} {user.last_name} logged in")

                await app.db.create_session(user.id, session_id)
                return Ok(data=data)
            else:
                return NoAccess()
        else:
            return Error(error="User not found")

    @users_router.get("/logout")
    async def logout(request: Request):
        decoded = decode(request)
        await app.db.kill_session(decoded.get("session_id"))
        logger.debug(f"Logged out")
        return NoAccess()

    @users_router.post("/me")
    async def auth(user: User = Depends(is_authorize)):
        logger.info(f"Get user: {user.name} {user.last_name}")
        return user

    @users_router.delete("/")
    async def delete(user: User = Depends(is_authorize)):
        await app.db.update(user.id, is_active=False)
        logger.warning(f"User {user.name} {user.last_name} soft removed")
        return NoAccess()


    app.app.include_router(users_router)
