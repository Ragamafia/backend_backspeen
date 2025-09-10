from fastapi import APIRouter


def register_admin_router(app):
    admin_router = APIRouter(
        tags=["Admin"],
        prefix="/api/admin"
    )


    app.app.include_router(admin_router)