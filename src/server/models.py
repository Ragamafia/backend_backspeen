from pydantic import BaseModel


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