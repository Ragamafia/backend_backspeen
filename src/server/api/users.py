import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel, field_validator, Secret, EmailStr

from models import User
from server.utils import create_token, is_authorize
from server.models import Ok, Error
from logger import logger


class NewUserRequest(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    password: Secret[str]

    @field_validator("email", mode="before")
    def normalize_email(cls, v):
        return v.lower()


class LoginRequest(BaseModel):
    email: str
    password: str


class EditUserRequest(BaseModel):
    name: str
    last_name: str


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
                return Error(error="Access denied")
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
            return Error(error="Access denied")

    @users_router.delete("/")
    async def delete(user: User = Depends(is_authorize)):
        await app.db.update(user.user_id, is_active=False)
        await app.db.kill_session(user.user_id)
        logger.warning(f"User {user.name} {user.last_name} removed")
        return Ok(data={})

    @users_router.post("/edit")
    async def edit_user(request: EditUserRequest, user: User = Depends(is_authorize)):
        return await app.db.update(user.user_id, name=request.name, last_name=request.last_name)


    app.app.include_router(users_router)
