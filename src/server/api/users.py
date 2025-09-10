from fastapi import APIRouter, HTTPException

from src.server.utils import create_token, verify_token
from src.logger import logger
from src.server.api.requests import NewUserRequest, NewUserResponse, LoginRequest, TokenRequest

def register_users_router(app):
    users_router = APIRouter(
        tags=["Users"],
        prefix="/api/users"
    )

    @users_router.post("/register")
    async def create_user(request: NewUserRequest):
        if user := await app.db.get_user(request.email):
            logger.warning(f"User {user.name} already exists")
        else:
            await app.db.create(request.name, request.last_name, request.email, request.password)

    @users_router.post("/login")
    async def login(request: LoginRequest):
        if user := await app.db.read(request.email, request.password):
            token = create_token(user.id)
            user.is_active = True
            await user.save()

            logger.success(f"User {request.email} logged in")
            return {"access_token": token, "token_type": "bearer"}
        else:
            logger.warning(f"User not found")
            return NewUserResponse(success=False, result=None)

    @users_router.post("/me")
    async def get_user(request: TokenRequest):
        if request is None:
            raise HTTPException(status_code=401, detail="Token missing")
        user_id = verify_token(request)
        return await app.db.get_user_by_id(user_id)


    app.app.include_router(users_router)
