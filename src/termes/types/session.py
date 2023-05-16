from termes.types.user import UserSession


class Session(UserSession):
    token: str
