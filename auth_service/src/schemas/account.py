from pydantic import BaseModel


class AccountID(BaseModel):
    id: int


class BaseAccount(BaseModel):
    email: str


class AccountDB(BaseAccount, AccountID):
    pass


class CheckAccountRequest(BaseAccount):
    pass
