from datetime import timedelta
from starlette.background import BackgroundTasks

from src.api.exceptions import (
    InviteNotFoundException,
    CredentialException,
    AccountAlreadyExistsException,
)
from src.config import jwt_settings
from src.models import Invite, Account, User, Company
from src.utils.email_sender import send_email
from src.utils.invite import generate_invite_token
from src.utils.jwt_utils import (
    create_access_token,
)
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode
from src.utils.password import get_password_hash, verify_password


class AuthService(BaseService):
    base_repository = 'account'

    @transaction_mode
    async def sign_up(
        self, email: str, background_tasks: BackgroundTasks
    ) -> None:
        await self._check_account_is_free(email=email)
        invite_token = generate_invite_token()
        await self.uow.invite.add_one(email=email, invite_token=invite_token)
        background_tasks.add_task(
            send_email,
            template_name='sign_up.html',
            receiver=email,
            subject='Подтверждение регистрации',
            data={
                'invite_token': invite_token,
            },
        )

    @transaction_mode
    async def sign_up_complete(
        self,
        email: str,
        invite_token: str,
        first_name: str,
        last_name: str,
        password: str,
        company_name: str,
    ) -> User:
        invite: Invite = await self._check_invite_exists(
            email=email, invite_token=invite_token
        )
        if invite.user_id:
            user = await self.uow.user.update_one_by_id(
                obj_id=invite.user_id,
                first_name=first_name,
                last_name=last_name,
            )
        else:
            user = await self.uow.user.add_one_and_get_obj(
                first_name=first_name, last_name=last_name
            )
            company_id: Company = await self.uow.company.add_one_and_get_id(
                company_name=company_name
            )
            await self.uow.member.add_one(
                company_id=company_id, user_id=user.id, is_admin=True
            )

        account_id = await self.uow.account.add_one_and_get_id(
            email=email,
        )
        await self.uow.secret.add_one(
            account_id=account_id,
            user_id=user.id,
            hashed_password=get_password_hash(password),
        )

        await self.uow.invite.delete_by_query(
            email=email, invite_token=invite_token
        )
        return user

    @transaction_mode
    async def generate_access_token(self, email: str, password: str) -> str:
        account: Account = (
            await self.uow.account.get_by_email_with_user_and_secret(
                email=email
            )
        )
        if (
            not account
            or not account.user
            or not verify_password(password, account.secret.hashed_password)
        ):
            raise CredentialException
        access_token_expires = timedelta(
            minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = create_access_token(
            data={'sub': account.user.id}, expires_delta=access_token_expires
        )
        return access_token

    @transaction_mode
    async def check_account(self, email: str) -> None:
        await self._check_account_is_free(email=email)

    async def _check_account_is_free(self, **kwargs):
        account = await self.uow.account.get_by_query_one_or_none(**kwargs)
        if account:
            raise AccountAlreadyExistsException

    async def _check_invite_exists(self, **kwargs) -> Invite:
        invite = await self.uow.invite.get_by_query_one_or_none(**kwargs)
        if not invite:
            raise InviteNotFoundException
        return invite
