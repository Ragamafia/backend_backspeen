from pydantic import BaseModel


class User(BaseModel):
    name: str
    last_name: str
    email: str
    password: str

    is_active: bool | None = None
    is_admin: bool | None = None

class NewUserRequest(BaseModel):
    name: str
    last_name: str
    email: str
    password: str

class NewUserResponse(BaseModel):
    success: bool
    result: User | None

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenRequest(BaseModel):
    access_token: str
    token_type: str = "bearer"
