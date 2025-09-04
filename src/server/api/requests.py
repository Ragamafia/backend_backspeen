from pydantic import BaseModel

from src.models import User


class NewUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class NewUserResponse(BaseModel):
    success: bool
    result: User | None

class LoginRequest(BaseModel):
    email: str
    password: str
