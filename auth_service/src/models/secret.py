import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base

if typing.TYPE_CHECKING:
    pass


class Secret(Base):
    __tablename__ = 'secret'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    account_id: Mapped[int] = mapped_column(ForeignKey('account.id'))
    hashed_password: Mapped[str]
