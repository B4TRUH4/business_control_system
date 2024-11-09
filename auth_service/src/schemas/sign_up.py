from src.schemas.company import CreateCompanyRequest
from src.schemas.user import CreateUserRequest, UserDB, CreateUserResponse


class SignUpRequest(CreateCompanyRequest, CreateUserRequest):
    pass


class SignUpResponse(CreateUserResponse):
    payload: UserDB
