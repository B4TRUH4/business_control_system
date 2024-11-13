from starlette import status


class ServiceException(Exception):
    def __init__(self, status_code: int, message: str, headers: dict = {}):
        self.message = message
        self.status_code = status_code
        self.headers = headers
        super().__init__(self.message)


class UserAlreadyExistsException(ServiceException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'User already exists',
        )


class AccountAlreadyExistsException(ServiceException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Account with such email already exists',
        )


class InviteNotFoundException(ServiceException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Invite not found',
        )


class CredentialException(ServiceException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            'Invalid credentials',
            {'WWW-Authenticate': 'Bearer'},
        )


class NotEnoughRightsException(ServiceException):
    def __init__(self):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            'Forbidden',
        )


class UserDoesNotExistException(ServiceException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'User does not exist',
        )


class AccountDoesNotExistException(ServiceException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Account does not exist',
        )


class LastAccountException(ServiceException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'User has only one account. Deletion denied',
        )
