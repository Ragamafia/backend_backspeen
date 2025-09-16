from fastapi import APIRouter, Depends

from src.models import User
from src.server.utils import is_admin
from src.server.api.models import ChangeRoleRequest

from logger import logger


def register_admin_router(app):
    admin_router = APIRouter(
        tags=["Admin"],
        prefix="/api/admin"
    )

    @admin_router.post("/change-role")
    async def change_role(request: ChangeRoleRequest, admin: User = Depends(is_admin)):
        if admin:
            logger.info(f"Change role. User ID: {request.user_id}. Role: {request.role}")
            return await app.db.update(request.user_id, role=request.role)

    @admin_router.put("/unblock/{user_id}")
    async def unblock_user(user_id: int, admin: User = Depends(is_admin)):
        if admin.role == "admin":
            logger.info(f"Unblock user. ID: {user_id}")
            return await app.db.update(user_id, is_active=True)


    app.app.include_router(admin_router)
