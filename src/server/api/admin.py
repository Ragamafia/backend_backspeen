from fastapi import Request, APIRouter, Depends, HTTPException

from src.server.utils import decode
from src.server.api.models import User, ChangeRoleRequest


def register_admin_router(app):
    admin_router = APIRouter(
        tags=["Admin"],
        prefix="/api/admin"
    )

    async def is_admin(request: Request):
        token = decode(request)
        if isinstance(token, dict):
            if user := await app.db.get_user(token.get("user_id")):
                if user.role == "admin":
                    return user

        raise HTTPException(status_code=401, detail="Bad token")

    @admin_router.post("/change-role")
    async def change_role(request: ChangeRoleRequest, admin: User = Depends(is_admin)):
        if admin:
            return await app.db.update(request.user_id, request.role)


    app.app.include_router(admin_router)