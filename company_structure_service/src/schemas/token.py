from pydantic import BaseModel


class TokenData(BaseModel):
    user_id: int | None = None
    company_id: int | None = None
    is_admin: bool = False
