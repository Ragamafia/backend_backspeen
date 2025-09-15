from fastapi import APIRouter, Depends

from src.server.utils import is_admin
from src.server.api.models import User, ChangeRoleRequest
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
            return await app.db.update(request.user_id, request.role)

    @admin_router.get("/unblock/{user_id}")
    async def unblock(user_id: int, admin: User = Depends(is_admin)):
        if admin:
            logger.info(f"Unblock user. ID: {user_id}")
            return await app.db.unblock(user_id)

    @admin_router.delete("/{user_id}")
    async def delete_user(user_id: int, admin: User = Depends(is_admin)):
        if admin:
            logger.info(f"Delete user. ID: {user_id}")
            return f"Delete user: {user_id}"
            #return app.db.delete(user_id)

    app.app.include_router(admin_router)