from pydantic import BaseModel


class User(BaseModel):
    first_name: str | None
    last_name: str | None
    email: str | None
    password: str | None

    is_active: bool | None = None
    is_admin: bool | None = None
