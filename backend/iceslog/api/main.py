from fastapi import APIRouter
from iceslog.api.routes import items,users, login, auth

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(login.router, prefix="", tags=["login"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])