from fastapi import FastAPI

from src.config import settings
from src.metadata import TITLE, DESCRIPTION, VERSION


def create_fastapi_app() -> FastAPI:
    if settings.MODE == 'PROD':
        fastapi_app = FastAPI(
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            docs_url=None,
            redoc_url=None,
        )
    else:
        fastapi_app = FastAPI(
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
        )

    return fastapi_app


app = create_fastapi_app()
