import typing

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base

if typing.TYPE_CHECKING:
    from .position import Position


class UserPosition(Base):
    __tablename__ = 'user_position'
    id: Mapped[int] = mapped_column(primary_key=True)
    position_id: Mapped[int] = mapped_column(
        ForeignKey('position.id', ondelete='CASCADE')
    )
    user_id: Mapped[int]

    position: Mapped['Position'] = relationship(
        back_populates='users_positions'
    )

    __table_args__ = (UniqueConstraint('position_id', 'user_id'),)
