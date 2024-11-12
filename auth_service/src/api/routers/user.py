from typing import Annotated

from fastapi import APIRouter, BackgroundTasks
from fastapi.params import Depends
from pydantic import EmailStr
from starlette import status

from src.api.services import UserService
from src.models import User
from src.schemas.response import BaseResponse
from src.schemas.user import (
    UserBase,
    UpdateUserRequest,
    UserWithAccounts,
    CreateUserResponse,
)

router = APIRouter(prefix='/users')


@router.get(
    '/me',
    response_model=CreateUserResponse,
    status_code=status.HTTP_200_OK,
)
async def read_users_me(
    user: Annotated[User, Depends(UserService().get_current_user)],
) -> CreateUserResponse:
    return CreateUserResponse(
        payload=UserWithAccounts(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            accounts=[
                account.to_pydantic_schema() for account in user.accounts
            ],
        )
    )


@router.put(
    '/me',
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def update_users_me(
    user_info: UpdateUserRequest,
    user: Annotated[User, Depends(UserService().get_current_user)],
    service: Annotated[UserService, Depends()],
) -> CreateUserResponse:
    user = await service.update(
        user_id=user.id, **user_info.model_dump(exclude_none=True)
    )
    return CreateUserResponse(
        payload=UserWithAccounts(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            accounts=[
                account.to_pydantic_schema() for account in user.accounts
            ],
        )
    )


@router.post(
    '/me/add_email',
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
)
async def add_email_me(
    email: EmailStr,
    user: Annotated[UserService().get_current_user, Depends()],
    service: Annotated[UserService, Depends()],
    background_tasks: BackgroundTasks,
) -> BaseResponse:
    await service.add_email(
        user_id=user.id,
        email=email,
        background_tasks=background_tasks,
    )
    return BaseResponse()


@router.post(
    '/me/unlink_email',
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_email_me(
    email: EmailStr,
    user: Annotated[UserService().get_current_user, Depends()],
    service: Annotated[UserService, Depends()],
) -> BaseResponse:
    await service.delete_email(user_id=user.id, email=email)
    return BaseResponse()


@router.post(
    '',
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_info: UserBase,
    admin_user: Annotated[UserService().get_current_admin, Depends()],
    service: Annotated[UserService, Depends()],
) -> CreateUserResponse:
    user = await service.create_user(
        company_id=admin_user.company.id, **user_info.model_dump()
    )
    return CreateUserResponse(
        payload=UserWithAccounts(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            accounts=[
                account.to_pydantic_schema() for account in user.accounts
            ],
        )
    )


@router.post(
    '/{user_id}/invite',
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
)
async def invite(
    user_id: int,
    email: EmailStr,
    admin_user: Annotated[UserService().get_current_admin, Depends()],
    service: Annotated[UserService, Depends()],
    background_tasks: BackgroundTasks,
) -> BaseResponse:
    await service.invite_user(
        email=email,
        user_id=user_id,
        admin_company_id=admin_user.company.id,
        background_tasks=background_tasks,
    )
    return BaseResponse()


@router.put(
    '/{user_id}',
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def update_user(
    user_id: int,
    user_info: UpdateUserRequest,
    admin_user: Annotated[UserService().get_current_admin, Depends()],
    service: Annotated[UserService, Depends()],
) -> CreateUserResponse:
    user = await service.update(
        user_id=user_id,
        admin_company_id=admin_user.company.id,
        **user_info.model_dump(exclude_none=True),
    )
    return CreateUserResponse(
        payload=UserWithAccounts(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            accounts=[
                account.to_pydantic_schema() for account in user.accounts
            ],
        )
    )


@router.post(
    '/{user_id}/unlink_email',
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_email(
    user_id: int,
    email: EmailStr,
    admin_user: Annotated[UserService().get_current_admin, Depends()],
    service: Annotated[UserService, Depends()],
) -> BaseResponse:
    await service.delete_email(
        user_id=user_id, email=email, admin_company_id=admin_user.company.id
    )
    return BaseResponse()


@router.post(
    '/{user_id}/add_email',
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
)
async def add_email(
    user_id: int,
    email: EmailStr,
    admin_user: Annotated[UserService().get_current_admin, Depends()],
    service: Annotated[UserService, Depends()],
    background_tasks: BackgroundTasks,
) -> BaseResponse:
    await service.add_email(
        user_id=user_id,
        email=email,
        background_tasks=background_tasks,
        admin_company_id=admin_user.company.id,
    )
    return BaseResponse()


# Здесь запрос должен быть POST, но, так как фронта нет, то я
# сделал GET.
@router.get(
    '/confirm_email',
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
)
async def confirm_email(
    email: EmailStr,
    token: str,
    service: Annotated[UserService, Depends()],
) -> BaseResponse:
    await service.confirm_email(email=email, token=token)
    return BaseResponse()
