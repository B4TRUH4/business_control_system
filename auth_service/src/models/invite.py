from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from ..schemas.invites import InviteDB


class Invite(Base):
    __tablename__ = 'invite'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    invite_token: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)

    def to_pydantic_schema(self) -> InviteDB:
        return InviteDB(**self.__dict__)
