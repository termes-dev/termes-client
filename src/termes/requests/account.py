import json
from typing import Final

from aiohttp import ClientSession

from .request import Request, RequestMethod, ContentType
from ..types.errors import APIError
from ..types.responses import UserResponse, ErrorResponse

ACCOUNT_ENDPOINT: Final[str] = "/account/"


async def get(
        host: str,
        token: str,
        http_session: ClientSession | None = None
) -> UserResponse | APIError:
    status, raw_response = await Request(
        host=host,
        method=RequestMethod.GET,
        endpoint=ACCOUNT_ENDPOINT,
    ).accept(ContentType.APPLICATION_JSON).x_token(token).execute(http_session)

    if status == 200:
        return UserResponse(**json.loads(raw_response))

    return APIError(
        status=status,
        response=ErrorResponse(**json.loads(raw_response))
    )


async def delete(
        host: str,
        token: str,
        http_session: ClientSession | None = None
) -> UserResponse | APIError:
    status, raw_response = await Request(
        host=host,
        method=RequestMethod.DELETE,
        endpoint=ACCOUNT_ENDPOINT,
    ).accept(ContentType.APPLICATION_JSON).x_token(token).execute(http_session)

    if status == 200:
        return UserResponse(**json.loads(raw_response))

    return APIError(
        status=status,
        response=ErrorResponse(**json.loads(raw_response))
    )
