import jwt
from datetime import timedelta, timezone, datetime

from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from src.api.exceptions import CredentialException
from src.config import jwt_settings
from src.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token')


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM
    )
    return encoded_jwt


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
