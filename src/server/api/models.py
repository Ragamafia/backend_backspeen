from typing import Literal
from pydantic import BaseModel


Role = Literal["admin", "user", "moderator"]


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
    data: dict | None = None
    error: str = "Access denied"


class Error(Response):
    success: bool = False
    data: dict | None = None
    error: str


class NewUserRequest(BaseModel):
    name: str
    last_name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ChangeRoleRequest(BaseModel):
    user_id: int
    role: Role
