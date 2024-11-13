from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class Member(Base):
    __tablename__ = 'member'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    company_id: Mapped[int] = mapped_column(ForeignKey('company.id'))
    is_admin: Mapped[bool] = mapped_column(default=False)
