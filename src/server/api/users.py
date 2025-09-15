from fastapi import APIRouter, Depends

from src.server.utils import create_token, is_authorize
from src.server.api.models import User, NewUserRequest, LoginRequest, Ok, NoAccess

from src.logger import logger


def register_users_router(app):
    users_router = APIRouter(
        tags=["Users"],
        prefix="/api/users"
    )

    @users_router.post("/register")
    async def create_user(request: NewUserRequest):
        if user := await app.db.read(request.email, request.password):
            logger.warning(f"User {user.name} {user.last_name} already exists")
            return user
        else:
            user = await app.db.create(request.name, request.last_name, request.email, request.password)
            logger.info(f"Created user: {user.name} {user.last_name}")
            return user

    @users_router.post("/login")
    async def login(request: LoginRequest):
        if user := await app.db.read(request.email, request.password):
            if user.is_active:
                token = create_token(user.id)
                data = {"access_token": token, "token_type": "bearer"}
                logger.success(f"User {user.name} {user.last_name} logged in")
                return Ok(success=True, data=data)
            else:
                return NoAccess(success=False, data=None, error=f"User {request.email} not active")
        else:
            return NoAccess(success=False, data=None, error=None)

    @users_router.post("/me")
    async def auth(user: User = Depends(is_authorize)):
        if user:
            logger.info(f"Get user: {user.name} {user.last_name}")
            return user

    @users_router.post("/logout")
    async def logout(request: dict, user: User = Depends(is_authorize)):
        if user:
            logger.debug(f"User {user.name} {user.last_name} logged out")
            return NoAccess(success=False, data=request, error=None)

    @users_router.delete("/{user_id}")
    async def delete(user_id: int, user: User = Depends(is_authorize)):
        if user:
            await app.db.to_ban(user_id)
            logger.warning(f"User {user.name} {user.last_name} soft removed")
            return NoAccess(success=False, data=None, error=None)


    app.app.include_router(users_router)