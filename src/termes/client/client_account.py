from datetime import timedelta
from typing import Final

from aiohttp import ClientSession

from .client_module import ClientModule
from ..requests import account
from ..types.errors import UnauthorizedError, ClientError, UserDeletedError
from ..types.responses import UserResponse
from ..types.session import Session
from ..types.user import User
from ..utils.cache import MemoryCached, CacheExpiredError

DEFAULT_CACHE_TTL: Final[timedelta] = timedelta(seconds=60)


class ClientAccount(ClientModule):
    def __init__(
            self,
            host: str,
            session: Session,
            http_session: ClientSession,
            cache_ttl: timedelta = DEFAULT_CACHE_TTL
    ):
        super().__init__(host, session, http_session)

        self.cache_ttl: timedelta = cache_ttl
        self.cached_user: MemoryCached[User] | None = None

    async def _get(self) -> User:
        response = await account.get(self.host, self.session.token, self.http_session)

        if isinstance(response, UserResponse):
            return response.user

        if response.status == 401:
            raise UnauthorizedError(response.response.detail)

        if response.status == 410:
            raise UserDeletedError(response.response.detail)

        raise ClientError(response.response.detail)

    async def get(self, *, cached: bool = True, update_cache: bool = True) -> User:
        if not cached:
            return await self._get()

        if self.cached_user is None:
            user = await self._get()
            if update_cache:
                self.cached_user = MemoryCached(user, self.cache_ttl)
            return user

        try:
            return self.cached_user.get()
        except CacheExpiredError as error:
            if not update_cache:
                return error.value
            user = await self._get()
            self.cached_user.set(user)
            return user

    async def delete(self, *, update_cache: bool = True) -> User:
        response = await account.delete(self.host, self.session.token, self.http_session)

        if isinstance(response, UserResponse):
            if update_cache:
                self.cached_user = None
            return response.user

        if response.status == 401:
            raise UnauthorizedError(response.response.detail)

        if response.status == 410:
            raise UserDeletedError(response.response.detail)

        raise ClientError(response.response.detail)
