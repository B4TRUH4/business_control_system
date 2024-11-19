from pydantic import BaseModel

from src.schemas.response import BaseCreateResponse, BaseResponse
from src.schemas.user import User


class PositionID(BaseModel):
    id: int


class PositionBase(BaseModel):
    name: str
    description: str | None = None


class PositionDB(PositionBase, PositionID):
    company_id: int


class PositionWithUsers(PositionBase, PositionID):
    users: list[User]


class CreatePositionRequest(PositionBase):
    user_ids: list[int] | None = None


class UpdatePositionRequest(CreatePositionRequest):
    pass


class PositionResponse(BaseResponse):
    payload: PositionWithUsers


class ListPositionResponse(BaseResponse):
    payload: list[PositionWithUsers | PositionDB]


class CreatePositionResponse(BaseCreateResponse):
    payload: PositionWithUsers


class UpdatePositionResponse(CreatePositionResponse):
    pass
