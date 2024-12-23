from fastapi import APIRouter
from typing import Annotated

from fastapi.params import Depends
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from src.api.services import StructAdmService
from src.models import StructAdm
from src.schemas.response import BaseResponse
from src.schemas.struct_adm import (
    CreateStructAdmRequest,
    CreateStructAdmResponse,
    StructAdmResponse,
    ListStructAdmResponse,
)
from src.schemas.token import TokenData
from src.utils.jwt_utils import get_current_admin, get_current_user

router = APIRouter(prefix='/adm')


@router.post(
    '', response_model=CreateStructAdmResponse, status_code=HTTP_201_CREATED
)
async def create_struct_adm(
    admin: Annotated[TokenData, Depends(get_current_admin)],
    service: Annotated[StructAdmService, Depends()],
    struct_adm: CreateStructAdmRequest,
) -> CreateStructAdmResponse:
    struct: StructAdm = await service.create_struct_adm(
        company_id=admin.company_id, **struct_adm.model_dump()
    )
    return CreateStructAdmResponse(payload=struct.to_pydantic_schema())


@router.get('', response_model=ListStructAdmResponse, status_code=HTTP_200_OK)
async def list_struct_adm(
    user: Annotated[TokenData, Depends(get_current_user)],
    service: Annotated[StructAdmService, Depends()],
) -> ListStructAdmResponse:
    structs: list[StructAdm] = await service.list_struct_adm(
        company_id=user.company_id,
    )
    return ListStructAdmResponse(
        payload=[struct.to_pydantic_schema() for struct in structs]
    )


@router.get(
    '/{struct_id}', response_model=StructAdmResponse, status_code=HTTP_200_OK
)
async def get_struct_adm(
    struct_id: int,
    user: Annotated[TokenData, Depends(get_current_user)],
    service: Annotated[StructAdmService, Depends()],
) -> StructAdmResponse:
    struct: StructAdm = await service.get_struct_adm(
        struct_adm_id=struct_id,
        company_id=user.company_id,
    )
    return StructAdmResponse(payload=struct.to_pydantic_schema())


@router.put(
    '/{struct_id}',
    response_model=CreateStructAdmResponse,
    status_code=HTTP_201_CREATED,
)
async def update_struct_adm(
    struct_id: int,
    admin: Annotated[TokenData, Depends(get_current_admin)],
    service: Annotated[StructAdmService, Depends()],
    struct_adm: CreateStructAdmRequest,
) -> CreateStructAdmResponse:
    struct: StructAdm = await service.update_struct_adm(
        struct_adm_id=struct_id,
        company_id=admin.company_id,
        **struct_adm.model_dump(),
    )
    return CreateStructAdmResponse(payload=struct.to_pydantic_schema())


@router.delete(
    '/{struct_id}', response_model=BaseResponse, status_code=HTTP_204_NO_CONTENT
)
async def delete_struct_adm(
    struct_id: int,
    admin: Annotated[TokenData, Depends(get_current_admin)],
    service: Annotated[StructAdmService, Depends()],
) -> BaseResponse:
    await service.delete_struct_adm(
        struct_adm_id=struct_id,
        company_id=admin.company_id,
    )
    return BaseResponse(status=HTTP_204_NO_CONTENT)
