import typing

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_utils import LtreeType, Ltree

from .base import Base
from ..schemas.struct_adm import StructAdmDB

if typing.TYPE_CHECKING:
    from .struct_adm_position import StructAdmPosition


class StructAdm(Base):
    __tablename__ = 'struct_adm'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    path: Mapped[Ltree] = mapped_column(LtreeType, nullable=True, index=True)
    company_id: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint(
            'company_id',
            'name',
        ),
    )

    struct_positions: Mapped[list['StructAdmPosition']] = relationship(
        'StructAdmPosition',
        back_populates='struct_adm',
        cascade='all, delete-orphan',
    )

    def to_pydantic_schema(self) -> StructAdmDB:
        kwargs = self.__dict__.copy()
        kwargs.pop('struct_positions', None)
        return StructAdmDB(
            **kwargs,
            struct_positions=[
                position.to_pydantic_schema()
                for position in self.struct_positions
            ],
        )
