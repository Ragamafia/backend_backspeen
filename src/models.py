from typing import Literal
from pydantic import BaseModel


Role = Literal["admin", "user", "moderator"]


class User(BaseModel):
    name: str
    last_name: str
    email: str
    password: str

    is_active: bool | None = None
    role: Role | None
