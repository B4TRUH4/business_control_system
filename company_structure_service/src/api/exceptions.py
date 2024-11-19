from starlette import status


class ServiceException(Exception):
    def __init__(self, status_code: int, message: str, headers: dict = {}):
        self.message = message
        self.status_code = status_code
        self.headers = headers
        super().__init__(self.message)


class PositionDoesNotExistsException(ServiceException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Position does not exists',
        )


class StructAdmDoesNotExistsException(ServiceException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Struct adm does not exists',
        )


class StructAdmAlreadyExistsException(ServiceException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Struct adm already exists',
        )


class PositionAlreadyExistsException(ServiceException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Position already exists',
        )


class CredentialException(ServiceException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            'Invalid credentials',
            {'WWW-Authenticate': 'Bearer'},
        )
