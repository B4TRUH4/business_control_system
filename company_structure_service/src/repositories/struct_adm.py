from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import select, Result, insert, update
from sqlalchemy.orm import selectinload

from src.models import StructAdm, StructAdmPosition
from src.utils.repository import SqlAlchemyRepository


class StructAdmRepository(SqlAlchemyRepository):
    model = StructAdm

    async def get_by_query_one_or_none_with_positions(
        self, **kwargs: Any
    ) -> model | None:
        query = (
            select(self.model)
            .filter_by(**kwargs)
            .options(
                selectinload(self.model.struct_positions).joinedload(
                    StructAdmPosition.position
                )
            )
        )
        res: Result = await self.session.execute(query)
        return res.unique().scalar_one_or_none()

    async def get_by_query_all_with_positions(
        self, **kwargs: Any
    ) -> Sequence[model]:
        query = (
            select(self.model)
            .filter_by(**kwargs)
            .options(
                selectinload(self.model.struct_positions).joinedload(
                    StructAdmPosition.position
                )
            )
        )
        res: Result = await self.session.execute(query)
        return res.scalars().all()

    async def add_one_and_get_obj_with_positions(self, **kwargs: Any) -> model:
        query = (
            insert(self.model)
            .values(**kwargs)
            .returning(self.model)
            .options(
                selectinload(self.model.struct_positions).joinedload(
                    StructAdmPosition.position
                )
            )
        )
        obj: Result = await self.session.execute(query)
        return obj.scalar_one()

    async def update_one_by_id_with_positions(
        self, obj_id: int | str | UUID, **kwargs: Any
    ) -> model | None:
        query = (
            update(self.model)
            .filter(self.model.id == obj_id)
            .values(**kwargs)
            .returning(self.model)
            .options(
                selectinload(self.model.struct_positions).joinedload(
                    StructAdmPosition.position
                )
            )
        )
        obj: Result | None = await self.session.execute(query)
        return obj.scalar_one_or_none()
