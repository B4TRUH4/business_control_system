from pydantic import BaseModel

from src.schemas.account import AccountDB
from src.schemas.response import BaseResponse


class UserID:
    id: int


class UserBase(BaseModel):
    first_name: str
    last_name: str


class UserDB(UserBase, UserID):
    pass


class UserWithAccounts(UserDB):
    accounts: list[AccountDB]


class UserResponse(BaseResponse):
    payload: UserWithAccounts


class ListUserResponse(BaseResponse):
    payload: list[UserWithAccounts]


class CreateUserRequest(UserBase):
    password: str


class CreateUserResponse(UserResponse):
    pass


class UpdateUserRequest(UserBase):
    first_name: str | None = None
    last_name: str | None = None
