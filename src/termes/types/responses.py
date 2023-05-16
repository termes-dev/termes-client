from pydantic import BaseModel

from .user import User, UserSession


class ErrorResponse(BaseModel):
    detail: str


class UserResponse(BaseModel):
    user: User


class FindUserResponse(BaseModel):
    users: list[User]


class RegistrationResponse(BaseModel):
    user: User


class AuthenticationResponse(BaseModel):
    token: str
    session: UserSession
