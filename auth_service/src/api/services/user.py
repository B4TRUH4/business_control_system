from typing import Annotated

from fastapi import Depends, BackgroundTasks

from src.api.exceptions import (
    CredentialException,
    UserDoesNotExistException,
    AccountDoesNotExistException,
    LastAccountException,
    InviteNotFoundException,
    AccountAlreadyExistsException,
    NotEnoughRightsException,
)
from src.models import User, Account
from src.utils.email_sender import send_email
from src.utils.invite import generate_invite_token
from src.utils.jwt_utils import oauth2_scheme, retrieve_token_data
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class UserService(BaseService):
    base_repository = 'user'

    @transaction_mode
    async def create_user(
        self, company_id: int, first_name: str, last_name: str
    ) -> User:
        user = await self.uow.user.add_one_and_get_obj(
            first_name=first_name, last_name=last_name
        )
        await self.uow.member.add_one(user_id=user.id, company_id=company_id)
        return user

    @transaction_mode
    async def invite_user(
        self,
        email: str,
        user_id: int,
        admin_company_id: int,
        background_tasks: BackgroundTasks,
    ) -> None:
        if not await self.uow.member.get_by_query_one_or_none(
            user_id=user_id, company_id=admin_company_id
        ):
            raise UserDoesNotExistException
        account = await self.uow.account.get_by_query_one_or_none(email=email)
        if account:
            raise AccountAlreadyExistsException
        invite_token = generate_invite_token()
        await self.uow.invite.add_one_and_get_obj(
            email=email, invite_token=invite_token, user_id=user_id
        )
        background_tasks.add_task(
            send_email,
            template_name='invitation.html',
            receiver=email,
            subject='Приглашение в компанию',
            data={
                'invite_token': invite_token,
            },
        )

    @transaction_mode
    async def get_current_user(
        self, token: Annotated[str, Depends(oauth2_scheme)]
    ) -> User:
        return await self._get_user_from_token(token)

    @transaction_mode
    async def get_current_admin(
        self, token: Annotated[str, Depends(oauth2_scheme)]
    ) -> User:
        user = await self._get_user_from_token(token)
        membership = await self.uow.member.get_by_query_one_or_none(
            user_id=user.id, is_admin=True
        )
        if not membership:
            raise CredentialException
        return user

    @transaction_mode
    async def update(
        self, user_id: int, admin_company_id: int | None = None, **kwargs
    ) -> User:
        if admin_company_id:
            await self._check_admin_and_user_in_one_company(
                user_id, admin_company_id
            )
        return await self._update_user(user_id, **kwargs)

    @transaction_mode
    async def delete_email(
        self, user_id: int, email: str, admin_company_id: int | None = None
    ) -> None:
        if admin_company_id:
            await self._check_admin_and_user_in_one_company(
                user_id, admin_company_id
            )
        account = await self.uow.account.get_by_email_with_user_and_secret(
            email=email
        )
        if not account or not account.user.id == user_id:
            raise AccountDoesNotExistException
        accounts: list[Account] = await self.uow.secret.get_by_query_all(
            user_id=user_id
        )
        if len(accounts) == 1:
            raise LastAccountException
        await self.uow.account.delete_by_query(email=email)

    @transaction_mode
    async def add_email(
        self,
        user_id: int,
        email: str,
        background_tasks: BackgroundTasks,
        admin_company_id: int | None = None,
    ) -> None:
        if admin_company_id:
            await self._check_admin_and_user_in_one_company(
                user_id, admin_company_id
            )
        account = await self.uow.account.get_by_query_one_or_none(email=email)
        if account:
            raise AccountAlreadyExistsException
        invite_token = generate_invite_token()
        await self.uow.invite.add_one_and_get_obj(
            email=email, invite_token=invite_token, user_id=user_id
        )
        background_tasks.add_task(
            send_email,
            template_name='add_email.html',
            receiver=email,
            subject='Подтверждение почты',
            data={
                'confirmation_link': f'http://localhost:8000/api/users/confirm_email?email={email}&token={invite_token}'
            },
        )

    @transaction_mode
    async def confirm_email(self, email: str, token: str) -> None:
        account = await self.uow.account.get_by_query_one_or_none(email=email)
        if account:
            await self.uow.invite.delete_by_query(email=email)
            raise AccountAlreadyExistsException
        invite = await self.uow.invite.get_by_query_one_or_none(
            email=email, invite_token=token
        )
        if not invite:
            raise InviteNotFoundException
        account_id = await self.uow.account.add_one_and_get_id(email=email)
        secret = await self.uow.secret.get_by_query_one_or_none(
            user_id=invite.user_id
        )
        await self.uow.secret.add_one(
            account_id=account_id,
            user_id=secret.user_id,
            hashed_password=secret.hashed_password,
        )

    async def _get_user_from_token(self, token: str) -> User:
        token_data = retrieve_token_data(token)
        user = await self.uow.user.get_user_with_company_and_accounts(
            id=token_data.user_id
        )
        if not user:
            raise CredentialException
        return user

    async def _update_user(self, user_id: int, **kwargs) -> User:
        return await self.uow.user.update_one_by_id_and_get_user(
            obj_id=user_id,
            **kwargs,
        )

    async def _check_admin_and_user_in_one_company(
        self, admin_company_id: int, user_id: int
    ) -> None:
        if not await self.uow.member.get_by_query_one_or_none(
            user_id=user_id, company_id=admin_company_id
        ):
            raise NotEnoughRightsException
