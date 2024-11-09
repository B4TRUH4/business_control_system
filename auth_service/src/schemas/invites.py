from pydantic import BaseModel

from src.schemas.response import BaseResponse


class InviteID(BaseModel):
    id: int


class BaseInvite(BaseModel):
    email: str
    invite_token: str


class InviteDB(BaseInvite, InviteID):
    pass


class InviteResponse(BaseResponse):
    payload: InviteDB | None


class CreateInviteRequest(BaseInvite):
    pass
