from typing import Literal

from pydantic import BaseModel, field_validator, Secret, EmailStr


Role = Literal["admin", "user", "moderator"]


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


class EditUserRequest(BaseModel):
    name: str
    last_name: str
