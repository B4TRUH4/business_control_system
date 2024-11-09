import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import User
from .base import Base
from ..schemas.account import AccountDB

if typing.TYPE_CHECKING:
    from .user import User
    from .secret import Secret


class Account(Base):
    __tablename__ = 'account'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)

    user: Mapped['User'] = relationship(
        secondary='secret', back_populates='accounts'
    )
    secret: Mapped['Secret'] = relationship()

    def to_pydantic_schema(self) -> AccountDB:
        return AccountDB(**self.__dict__)
