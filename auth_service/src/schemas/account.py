from pydantic import BaseModel, EmailStr


class AccountID(BaseModel):
    id: int


class BaseAccount(BaseModel):
    email: EmailStr


class AccountDB(BaseAccount, AccountID):
    pass


class CheckAccountRequest(BaseAccount):
    pass
