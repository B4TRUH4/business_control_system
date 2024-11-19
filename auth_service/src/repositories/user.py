from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import select, Result, update, insert
from sqlalchemy.orm import joinedload, selectinload

from src.models import User, Company
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User

    async def add_one_and_get_obj(self, **kwargs: Any) -> model:
        query = (
            insert(self.model)
            .values(**kwargs)
            .returning(self.model)
            .options(
                joinedload(self.model.company),
                selectinload(self.model.accounts),
            )
        )
        obj: Result = await self.session.execute(query)
        return obj.scalar_one()

    async def get_user_with_company_and_accounts(
        self, company_id: int = None, **kwargs
    ) -> model:
        query = (
            select(self.model)
            .filter_by(**kwargs)
            .join(self.model.company)
            .options(
                joinedload(self.model.company),
                selectinload(self.model.accounts),
            )
        )
        if company_id:
            query = query.filter(Company.id == company_id)
        obj: Result = await self.session.execute(query)
        return obj.scalar_one_or_none()

    async def get_all_users_with_company_and_accounts(
        self, company_id: int = None, **kwargs
    ) -> Sequence[model]:
        query = (
            select(self.model)
            .filter_by(**kwargs)
            .join(self.model.company)
            .options(
                joinedload(self.model.company),
                selectinload(self.model.accounts),
            )
        )
        if company_id:
            query = query.filter(Company.id == 9)
        res: Result = await self.session.execute(query)
        return res.scalars().all()

    async def update_one_by_id_and_get_user(
        self, obj_id: int | str | UUID, **kwargs: Any
    ) -> model | None:
        query = (
            update(self.model)
            .filter(self.model.id == obj_id)
            .values(**kwargs)
            .returning(self.model)
            .options(
                joinedload(self.model.company),
                selectinload(self.model.accounts),
            )
        )
        obj: Result | None = await self.session.execute(query)
        return obj.scalar_one_or_none()
