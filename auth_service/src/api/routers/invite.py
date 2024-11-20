from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.api.exceptions import InviteNotFoundException
from src.api.services import InviteService
from src.schemas.invites import BaseInvite, InviteResponse

router = APIRouter(prefix='/invites')


@router.get('/', status_code=status.HTTP_200_OK, response_model=InviteResponse)
async def get_invite(
    invite: Annotated[BaseInvite, Depends()],
    service: Annotated[InviteService, Depends()],
) -> InviteResponse:
    invite = await service.get_by_query_one_or_none(**invite.model_dump())
    if not invite:
        raise InviteNotFoundException
    return InviteResponse(payload=invite.to_pydantic_schema())
