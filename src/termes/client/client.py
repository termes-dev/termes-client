from aiohttp import ClientSession

from .client_account import ClientAccount
from .client_module import ClientModule
from ..types.errors import HTTPSessionClosedError
from ..types.session import Session

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class Client(ClientModule):
    def __init__(self, host: str, session: Session, http_session: ClientSession | None = None):
        if http_session is not None and http_session.closed:
            raise HTTPSessionClosedError()

        super().__init__(host, session, ClientSession() if http_session is None else http_session)

        self.account: ClientAccount = ClientAccount(self.host, self.session, self.http_session)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.http_session.closed:
            await self.http_session.close()
