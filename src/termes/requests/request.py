from enum import Enum
from typing import Any
from urllib.parse import urljoin

from aiohttp import ClientSession

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class ContentType(Enum):
    APPLICATION_JSON = "application/json"


class Request:
    def __init__(
            self,
            host: str,
            *,
            method: RequestMethod | None = None,
            endpoint: str | None = None,
            headers: dict[str, Any] | None = None,
            params: dict[str, Any] | None = None,
            data: str | None = None
    ):
        self._host: str = host
        self._method: RequestMethod | None = method
        self._endpoint: str | None = endpoint
        self._headers: dict[str, Any] | None = headers
        self._params: dict[str, Any] | None = params
        self._data: str | None = data

    def method(self, method: RequestMethod) -> Self:
        self._method = method
        return self

    def endpoint(self, endpoint: str) -> Self:
        self._endpoint = endpoint
        return self

    def headers(self, headers: dict[str, Any]) -> Self:
        self._headers = headers
        return self

    def params(self, params: dict[str, Any]) -> Self:
        self._params = params
        return self

    def data(self, data: str) -> Self:
        self._data = data
        return self

    def content_type(self, content_type: str | ContentType) -> Self:
        if self._headers is None:
            self._headers = {}
        if isinstance(content_type, ContentType):
            self._headers["Content-Type"] = content_type.value
        else:
            self._headers["Content-Type"] = content_type
        return self

    def accept(self, accept: str | ContentType) -> Self:
        if self._headers is None:
            self._headers = {}
        if isinstance(accept, ContentType):
            self._headers["Content-Type"] = accept.value
        else:
            self._headers["Content-Type"] = accept
        return self

    def x_token(self, x_token: str) -> Self:
        if self._headers is None:
            self._headers = {}
        self._headers["X-Token"] = x_token
        return self

    async def _make_request(self, session: ClientSession) -> tuple[int, str]:
        async with session.request(
                method=RequestMethod.GET.value if self._method is None else self._method.value,
                url=urljoin(self._host, self._endpoint),
                headers={} if self._headers is None else self._headers,
                params={} if self._params is None else self._params,
                data=self._data
        ) as response:
            return response.status, await response.text()

    async def execute(self, session: ClientSession | None = None) -> tuple[int, str]:
        if session is None:
            async with ClientSession() as session:
                return await self._make_request(session)
        async with session:
            return await self._make_request(session)


def get(host: str) -> Request:
    return Request(host).method(RequestMethod.GET)


def post(host: str) -> Request:
    return Request(host).method(RequestMethod.POST)


def put(host: str) -> Request:
    return Request(host).method(RequestMethod.PUT)


def delete(host: str) -> Request:
    return Request(host).method(RequestMethod.DELETE)
