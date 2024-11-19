from fastapi import APIRouter
from typing import Annotated

from fastapi.params import Depends
from starlette.status import HTTP_204_NO_CONTENT

from src.api.services import PositionService
from src.schemas.position import (
    CreatePositionRequest,
    CreatePositionResponse,
    PositionResponse,
    ListPositionResponse,
    UpdatePositionRequest,
    UpdatePositionResponse,
)
from src.schemas.response import BaseResponse
from src.schemas.token import TokenData
from src.utils.jwt_utils import get_current_user, get_current_admin

router = APIRouter(prefix='/position')


@router.get('', response_model=ListPositionResponse)
async def list_position(
    user: Annotated[TokenData, Depends(get_current_user)],
    service: Annotated[PositionService, Depends()],
):
    positions = await service.list_position(company_id=user.company_id)
    return ListPositionResponse(payload=positions)


@router.post('', response_model=CreatePositionResponse)
async def create_position(
    admin: Annotated[TokenData, Depends(get_current_admin)],
    service: Annotated[PositionService, Depends()],
    position: CreatePositionRequest,
):
    position = await service.create_position(
        company_id=admin.company_id, **position.model_dump()
    )
    return CreatePositionResponse(payload=position)


@router.get('/{position_id}', response_model=PositionResponse)
async def get_position(
    user: Annotated[TokenData, Depends(get_current_user)],
    position_id: int,
    service: Annotated[PositionService, Depends()],
):
    position = await service.get_position(
        position_id=position_id, company_id=user.company_id
    )
    return PositionResponse(payload=position)


@router.put('/{position_id}', response_model=CreatePositionResponse)
async def update_position(
    position_id: int,
    admin: Annotated[TokenData, Depends(get_current_admin)],
    service: Annotated[PositionService, Depends()],
    position: UpdatePositionRequest,
):
    position = await service.update_position(
        position_id=position_id,
        company_id=admin.company_id,
        **position.model_dump(),
    )
    return UpdatePositionResponse(payload=position)


@router.delete('/{position_id}', response_model=BaseResponse)
async def delete_position(
    position_id: int,
    admin: Annotated[TokenData, Depends(get_current_admin)],
    service: Annotated[PositionService, Depends()],
):
    await service.delete_position(
        position_id=position_id, company_id=admin.company_id
    )
    return BaseResponse(status=HTTP_204_NO_CONTENT)