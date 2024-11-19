from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api.exceptions import (
    ServiceException,
)
from src.config import settings
from src.metadata import TITLE, DESCRIPTION, VERSION, TAG_METADATA
from src.schemas.response import ErrorResponse
from src.api import router


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


@app.exception_handler(ServiceException)
async def service_exception_handler(request: Request, exc: ServiceException):
    return JSONResponse(
        content=ErrorResponse(
            status=exc.status_code,
            message=exc.message,
        ).model_dump(),
        status_code=exc.status_code,
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        content=ErrorResponse(
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=exc.errors(),
        ).model_dump(),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        content=ErrorResponse(
            status=exc.status_code,
            message=exc.detail,
        ).model_dump(),
        status_code=exc.status_code,
        headers=exc.headers,
    )
