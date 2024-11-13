import functools
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any

from typing_extensions import Never

from src.database import async_session_maker
from src.repositories import (
    AccountRepository,
    InviteRepository,
    CompanyRepository,
    SecretRepository,
    MemberRepository,
    UserRepository,
)
from src.utils.custom_types import AsyncFunc


class AbstractUnitOfWork(ABC):
    @abstractmethod
    def __init__(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType,
    ) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> Never:
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        self.session_factory = async_session_maker

    async def __aenter__(self) -> None:
        self.session = self.session_factory()
        self.account = AccountRepository(self.session)
        self.invite = InviteRepository(self.session)
        self.user = UserRepository(self.session)
        self.company = CompanyRepository(self.session)
        self.member = MemberRepository(self.session)
        self.secret = SecretRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


def transaction_mode(func: AsyncFunc) -> AsyncFunc:
    """Decorate a function with transaction mode."""

    @functools.wraps(func)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        async with self.uow:
            return await func(self, *args, **kwargs)

    return wrapper
