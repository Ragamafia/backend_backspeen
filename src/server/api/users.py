import uuid
from pydantic import BaseModel
from fastapi import APIRouter, Depends

from src.models import User
from src.server.utils import create_token, is_authorize
from src.server.api.models import NewUserRequest, LoginRequest, EditUserRequest

from logger import logger


class Response(BaseModel):
    success: bool
    data: dict | None
    error: str | None


class Ok(Response):
    success: bool = True
    error: str | None = None


class Error(Response):
    success: bool = False
    data: dict | None = None


class NoAccess(Error):
    error: str = "Access denied"


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
                token = create_token(user.user_id, session_id)
                data = {"access_token": token, "token_type": "bearer"}
                logger.success(f"User {user.name} {user.last_name} logged in")

                await app.db.create_session(user.user_id, session_id)
                return Ok(data=data)
            else:
                return NoAccess()
        else:
            return Error(error="User not found")

    @users_router.get("/logout")
    async def logout(user: User = Depends(is_authorize)):
        await app.db.kill_session(user.user_id)
        logger.debug(f"User ID - {user.user_id} logged out")
        return Ok(data={})

    @users_router.get("/me")
    async def auth(user: User = Depends(is_authorize)):
        if user:
            logger.info(f"Get user: {user.name} {user.last_name}")
            return user
        else:
            return NoAccess()

    @users_router.delete("/")
    async def delete(user: User = Depends(is_authorize)):
        await app.db.update(user.user_id, is_active=False)
        await app.db.kill_session(user.user_id)
        logger.warning(f"User {user.name} {user.last_name} removed")
        return NoAccess()

    @users_router.post("/edit")
    async def edit_user(request: EditUserRequest, user: User = Depends(is_authorize)):
        return await app.db.update(user.user_id, name=request.name, last_name=request.last_name)


    app.app.include_router(users_router)
