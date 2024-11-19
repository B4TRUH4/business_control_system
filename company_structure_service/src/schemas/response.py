from typing import Any

from pydantic import BaseModel
from starlette.status import HTTP_200_OK, HTTP_201_CREATED


class BaseResponse(BaseModel):
    status: int = HTTP_200_OK
    error: bool = False
    payload: dict | list = {}


class BaseCreateResponse(BaseResponse):
    status: int = HTTP_201_CREATED


class ErrorResponse(BaseModel):
    status: int
    error: bool = True
    message: Any = 'Something went wrong'
