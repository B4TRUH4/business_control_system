import typing

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from ..schemas.struct_adm_position import StructAdmPositionDB

if typing.TYPE_CHECKING:
    from .struct_adm import StructAdm
    from .position import Position


class StructAdmPosition(Base):
    __tablename__ = 'struct_adm_positions'

    struct_adm_id: Mapped[int] = mapped_column(
        ForeignKey('struct_adm.id', ondelete='CASCADE'), primary_key=True
    )
    position_id: Mapped[int] = mapped_column(
        ForeignKey('position.id', ondelete='CASCADE'), primary_key=True
    )
    is_manager: Mapped[bool] = mapped_column(default=False)

    __table_args__ = (
        UniqueConstraint('struct_adm_id', 'position_id', 'is_manager'),
    )

    struct_adm: Mapped['StructAdm'] = relationship(
        'StructAdm', back_populates='struct_positions'
    )
    position: Mapped['Position'] = relationship(
        'Position', back_populates='struct_positions'
    )

    def to_pydantic_schema(self) -> StructAdmPositionDB:
        kwargs = self.__dict__.copy()
        kwargs.pop('position', None)
        return StructAdmPositionDB(
            **kwargs, position=self.position.to_pydantic_schema()
        )
