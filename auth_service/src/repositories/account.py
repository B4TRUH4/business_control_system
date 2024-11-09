from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload

from src.models import Account
from src.utils.repository import SqlAlchemyRepository


class AccountRepository(SqlAlchemyRepository):
    model = Account

    async def get_by_email_with_user_and_secret(self, email: str) -> Account:
        query = (
            select(self.model)
            .where(self.model.email == email)
            .options(joinedload(self.model.user), joinedload(self.model.secret))
        )
        res: Result = await self.session.execute(query)
        return res.scalar_one_or_none()
