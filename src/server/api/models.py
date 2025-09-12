from typing import Literal
from pydantic import BaseModel


Role = Literal["admin", "user", "moderator"]


class User(BaseModel):
    class Config:
        from_attributes = True

    name: str
    last_name: str
    email: str
    password: str

    is_active: bool | None = None
    role: Role | None

class NewUserRequest(BaseModel):
    name: str
    last_name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LogoutRequest(BaseModel):
    token: dict

class LoginResponse(BaseModel):
    success: bool
    data: dict


class LogoutResponse(BaseModel):
    success: bool
    data: dict

class AuthorizeRequest(BaseModel):
    token: dict

class AuthorizeResponse(BaseModel):
    success: bool
    data: dict

class TokenRequest(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ChangeRoleRequest(BaseModel):
    user_id: int
    role: Role

class DeleteUserRequest(BaseModel):
    user_id: int