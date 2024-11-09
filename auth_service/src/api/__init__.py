from fastapi import APIRouter
from .routers import invite_router, auth_router, user_router

router = APIRouter()
router.include_router(invite_router, tags=['Invites'])
router.include_router(auth_router, tags=['Auth'])
router.include_router(user_router, tags=['User'])
