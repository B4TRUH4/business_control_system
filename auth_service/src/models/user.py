import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:
    from .account import Account
    from .company import Company

from .base import Base
from ..schemas.user import UserDB


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]

    accounts: Mapped[list['Account']] = relationship(
        secondary='secret', back_populates='user'
    )
    company: Mapped['Company'] = relationship(
        secondary='member', back_populates='employees'
    )

    def to_pydantic_schema(self) -> UserDB:
        return UserDB(**self.__dict__)
