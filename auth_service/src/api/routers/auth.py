from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.api.services import AuthService
from src.schemas.account import BaseAccount
from src.schemas.invites import CreateInviteRequest
from src.schemas.response import BaseCreateResponse, BaseResponse
from src.schemas.sign_up import SignUpRequest, SignUpResponse
from src.schemas.token import Token

router = APIRouter(prefix='/auth')


@router.post(
    '/sign-up',
    status_code=status.HTTP_200_OK,
    response_model=BaseCreateResponse,
)
async def sign_up(
    account: Annotated[BaseAccount, Depends()],
    service: Annotated[AuthService, Depends()],
) -> BaseCreateResponse:
    await service.sign_up(**account.model_dump())
    return BaseCreateResponse()


@router.post(
    '/sign-up-complete',
    status_code=status.HTTP_200_OK,
    response_model=SignUpResponse,
)
async def sign_up_complete(
    create_invite_request: Annotated[CreateInviteRequest, Depends()],
    sign_up_info: SignUpRequest,
    service: Annotated[AuthService, Depends()],
) -> SignUpResponse:
    user = await service.sign_up_complete(
        **create_invite_request.model_dump(), **sign_up_info.model_dump()
    )
    return SignUpResponse(payload=user.to_pydantic_schema())


@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends()],
) -> Token:
    token = await service.generate_access_token(
        email=form_data.username, password=form_data.password
    )
    return Token(access_token=token, token_type='bearer')


@router.get(
    '/check_account',
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse,
)
async def check_account(
    account: Annotated[BaseAccount, Depends()],
    service: Annotated[AuthService, Depends()],
) -> BaseResponse:
    await service.check_account(**account.model_dump())
    return BaseResponse()
