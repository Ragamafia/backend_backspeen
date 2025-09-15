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

class Response(BaseModel):
    success: bool
    data: dict | None
    error: str | None

class Ok(Response):
    success: bool = True
    data: dict
    error: str | None = None

class NoAccess(Response):
    success: bool = False


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

class ChangeRoleRequest(BaseModel):
    user_id: int
    role: Role
