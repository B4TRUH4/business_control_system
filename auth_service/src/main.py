from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api.exceptions import (
    ServiceException,
)
from src.config import settings
from src.metadata import TITLE, DESCRIPTION, VERSION, TAG_METADATA
from src.api import router
from src.schemas.response import ErrorResponse


def create_fastapi_app() -> FastAPI:
    if settings.MODE == 'PROD':
        fastapi_app = FastAPI(
            title=TITLE,
            description=DESCRIPTION,
            openapi_tags=TAG_METADATA,
            version=VERSION,
            docs_url=None,
            redoc_url=None,

        )
    else:
        fastapi_app = FastAPI(
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
        )
    fastapi_app.include_router(router, prefix='/api')
    return fastapi_app


app = create_fastapi_app()
