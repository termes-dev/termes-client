from aiohttp import ClientSession

from ..types.session import Session


class ClientModule:
    def __init__(self, host: str, session: Session, http_session: ClientSession):
        self.host: str = host
        self.session: session = session
        self.http_session: ClientSession = http_session
