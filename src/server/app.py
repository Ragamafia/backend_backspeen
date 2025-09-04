from fastapi import FastAPI

from server.api.requests import NewUserRequest, NewUserResponse, LoginRequest
from db.ctrl import db
from logger import logger


app = FastAPI()


@app.post("/register")
async def create_user(data: NewUserRequest):
    if user := await db.create(data.first_name, data.last_name, data.email, data.password):
        return NewUserResponse(success=True, result=user)
    else:
        logger.debug(f"User already exists")
        return NewUserResponse(success=False, result=None)


@app.post("/login")
async def login(data: LoginRequest):
    if user := await db.read(data.email, data.password):
        logger.success(f"User {user["first_name"]} logged in")
        return NewUserResponse(success=True, result=user)
    else:
        logger.warning(f"User {data.email} not found")
        return NewUserResponse(success=False, result=None)
