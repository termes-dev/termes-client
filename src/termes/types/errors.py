from pydantic import BaseModel

from .responses import ErrorResponse


class APIError(BaseModel):
    status: int
    response: ErrorResponse


class ClientError(Exception):
    def __init__(self, message: str = "An error occurred"):
        super().__init__(message)


class HTTPSessionClosedError(ClientError):
    pass


class InvalidCredentialsError(ClientError):
    pass


class CredentialsUsedError(ClientError):
    pass


class UnauthorizedError(ClientError):
    pass


class AccessDeniedError(ClientError):
    pass


class UserDeletedError(ClientError):
    pass
