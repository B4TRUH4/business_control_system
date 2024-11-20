from fastapi import Depends

from src.api.exceptions import (
    PositionDoesNotExistsException,
    PositionAlreadyExistsException,
)
from src.api.services.user import UserService
from src.models import Position
from src.schemas.position import PositionWithUsers
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class PositionService(BaseService):
    def __init__(self, user_service: UserService = Depends()):
        super().__init__()
        self.user_service = user_service

    base_repository = 'position'

    @transaction_mode
    async def get_position(
        self, position_id: int, company_id: int
    ) -> PositionWithUsers:
        position = await self._get_position(
            position_id=position_id, company_id=company_id
        )
        users = []
        for user_position in position.users_positions:
            users.append(
                await self.user_service.get_user_by_id(user_position.user_id)
            )
        return position.to_pydantic_schema(users=users)

    @transaction_mode
    async def list_position(self, company_id: int) -> list[PositionWithUsers]:
        positions = await self.uow.position.get_by_query_all_with_user_position(
            company_id=company_id
        )
        result = []
        users_dict = await self.user_service.get_all_users()
        for position in positions:
            users = []
            for user_position in position.users_positions:
                users.append(user_position.user_id)
            users = [
                users_dict[user_id]
                for user_id in users
                if user_id in users_dict
            ]
            result.append(position.to_pydantic_schema(users=users))
        return result

    @transaction_mode
    async def create_position(
        self,
        name: str,
        company_id: int,
        description: str = None,
        user_ids: list[int] = None,
    ) -> PositionWithUsers:
        position_id = await self._create_position(
            name=name, company_id=company_id, description=description
        )
        return await self._add_users_to_position(
            position_id=position_id, user_ids=user_ids
        )

    @transaction_mode
    async def update_position(
        self,
        position_id: int,
        company_id: int,
        name: str,
        description: str = None,
        user_ids: list[int] = None,
    ) -> PositionWithUsers:
        await self._get_position(position_id=position_id, company_id=company_id)
        await self.uow.position.update_one_by_id(
            obj_id=position_id, name=name, description=description
        )
        await self.uow.user_position.delete_by_query(position_id=position_id)
        return await self._add_users_to_position(
            position_id=position_id, user_ids=user_ids
        )

    @transaction_mode
    async def delete_position(self, position_id: int, company_id: int) -> None:
        await self._get_position(position_id=position_id, company_id=company_id)
        await self.uow.position.delete_by_query(id=position_id)

    async def _add_users_to_position(
        self,
        position_id: int,
        user_ids: list[int] = None,
    ) -> PositionWithUsers:
        users = []
        if user_ids:
            for user_id in user_ids:
                users.append(await self.user_service.get_user_by_id(user_id))
                await self.uow.user_position.add_one(
                    user_id=user_id, position_id=position_id
                )

        position = (
            await self.uow.position.get_by_query_one_or_none_with_user_position(
                id=position_id
            )
        )
        return position.to_pydantic_schema(users=users)

    async def _get_position(
        self, position_id: int, company_id: int, **kwargs
    ) -> Position:
        position = (
            await self.uow.position.get_by_query_one_or_none_with_user_position(
                id=position_id,
                company_id=company_id,
                **kwargs,
            )
        )
        if not position:
            raise PositionDoesNotExistsException
        return position

    async def _create_position(
        self, name: str, company_id: int, **kwargs
    ) -> int:
        position = await self.uow.position.get_by_query_one_or_none(
            name=name, company_id=company_id
        )
        if position:
            raise PositionAlreadyExistsException
        return await self.uow.position.add_one_and_get_id(
            name=name, company_id=company_id, **kwargs
        )
