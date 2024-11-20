from typing import Annotated
import jwt

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from src.api.exceptions import CredentialException
from src.config import jwt_settings
from src.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='http://localhost:8000/api/auth/token'
)


def retrieve_token_data(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM]
        )
        user_id: int = payload.get('sub')
        company_id: int = payload.get('company_id')
        is_admin: bool = payload.get('is_admin')
        if user_id is None:
            raise CredentialException
        return TokenData(
            user_id=user_id, company_id=company_id, is_admin=is_admin
        )
    except InvalidTokenError:
        raise CredentialException


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:
    return _get_user_from_token(token)


def get_current_admin(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:
    user = get_current_user(token)
    if not user.is_admin:
        raise CredentialException
    return user


def _get_user_from_token(token: str) -> TokenData:
    token_data = retrieve_token_data(token)
    return token_data
