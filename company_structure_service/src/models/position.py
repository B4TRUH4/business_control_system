import typing

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from ..schemas.position import PositionDB, PositionWithUsers
from ..schemas.user import User

if typing.TYPE_CHECKING:
    from .struct_adm_position import StructAdmPosition
    from .user_position import UserPosition


class Position(Base):
    __tablename__ = 'position'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    company_id: Mapped[int] = mapped_column(nullable=False)
    users_positions: Mapped[list['UserPosition']] = relationship(
        back_populates='position', cascade='all, delete-orphan'
    )

    struct_positions: Mapped[list['StructAdmPosition']] = relationship(
        back_populates='position',
        cascade='all, delete-orphan',
    )

    __table_args__ = (
        UniqueConstraint(
            'name',
            'company_id',
        ),
    )

    def to_pydantic_schema(
        self, users: list[User] = None
    ) -> PositionDB | PositionWithUsers:
        if not users:
            return PositionDB(**self.__dict__)
        return PositionWithUsers(**self.__dict__, users=users)
