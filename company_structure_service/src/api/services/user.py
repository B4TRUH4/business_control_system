from typing import Annotated

import httpx
from fastapi import Depends, HTTPException
from starlette import status

from src.schemas.user import User
from src.utils.jwt_utils import oauth2_scheme


class UserService:
    def __init__(self, token: Annotated[str, Depends(oauth2_scheme)]):
        self.token = token

    async def get_user_by_id(self, user_id: int) -> User:
        async with httpx.AsyncClient() as client:
            headers = {'Authorization': f'Bearer {self.token}'}
            response = await client.get(
                f'http://auth_service:8000/api/users/{user_id}', headers=headers
            )
            if response.status_code == 200:
                user_data = response.json().get('payload')
                return User(**user_data)
            elif response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'User with ID {user_id} not found',
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail='Failed to retrieve user information',
                )

    async def get_all_users(self) -> dict[int, User]:
        async with httpx.AsyncClient() as client:
            headers = {'Authorization': f'Bearer {self.token}'}
            response = await client.get(
                'http://auth_service:8000/api/users', headers=headers
            )
            if response.status_code == 200:
                user_data = response.json().get('payload')
                return {data['id']: User(**data) for data in user_data}
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail='Failed to retrieve user information',
                )
