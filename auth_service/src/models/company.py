import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from ..schemas.company import CompanyDB

if typing.TYPE_CHECKING:
    from .user import User


class Company(Base):
    __tablename__ = 'company'
    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(unique=True)

    employees: Mapped[list['User']] = relationship(
        secondary='member', back_populates='company'
    )

    def to_pydantic_schema(self) -> CompanyDB:
        return CompanyDB(**self.__dict__)
