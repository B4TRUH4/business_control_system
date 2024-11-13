from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    account_id: int | None = None
    user_id: int | None = None
    email: str | None = None
