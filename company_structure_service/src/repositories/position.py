from typing import Any, Sequence

from sqlalchemy import Result, select
from sqlalchemy.orm import selectinload

from src.models import Position
from src.utils.repository import SqlAlchemyRepository


class PositionRepository(SqlAlchemyRepository):
    model = Position

    async def get_by_query_one_or_none_with_user_position(
        self, **kwargs: Any
    ) -> model | None:
        query = (
            select(self.model)
            .filter_by(**kwargs)
            .options(selectinload(self.model.users_positions))
        )
        res: Result = await self.session.execute(query)
        return res.unique().scalar_one_or_none()

    async def get_by_query_all_with_user_position(
        self, **kwargs: Any
    ) -> Sequence[model]:
        query = (
            select(self.model)
            .filter_by(**kwargs)
            .options(selectinload(self.model.users_positions))
        )
        res: Result = await self.session.execute(query)
        return res.scalars().all()
