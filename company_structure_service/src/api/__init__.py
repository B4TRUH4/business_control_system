from fastapi import APIRouter
from .routers import struct_adm_router, position_router

router = APIRouter(prefix='/struct')
router.include_router(struct_adm_router, tags=['Struct'])
router.include_router(position_router, tags=['Position'])
