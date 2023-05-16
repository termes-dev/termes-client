import json
from typing import Final

from aiohttp import ClientSession

from .request import RequestMethod, Request, ContentType
from ..types.errors import APIError
from ..types.responses import UserResponse, ErrorResponse, FindUserResponse

USER_ENDPOINT: Final[str] = "/user/"
GET_USER_ENDPOINT: Final[str] = "/user/{user_id}/"


async def get(
        host: str,
        user_id: int,
        http_session: ClientSession | None = None
) -> UserResponse | APIError:
    status, raw_response = await Request(
        host=host,
        method=RequestMethod.GET,
        endpoint=GET_USER_ENDPOINT.format(user_id=user_id),
    ).accept(ContentType.APPLICATION_JSON).execute(http_session)

    if status == 200:
        return UserResponse(**json.loads(raw_response))

    return APIError(
        status=status,
        response=ErrorResponse(**json.loads(raw_response))
    )


async def find(
        host: str,
        first_name: str | None = None,
        last_name: str | None = None,
        bio: str | None = None,
        username: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        http_session: ClientSession | None = None
) -> FindUserResponse | APIError:
    status, raw_response = await Request(
        host=host,
        method=RequestMethod.GET,
        endpoint=USER_ENDPOINT,
        params={
            "first-name": "@any" if first_name is None else first_name,
            "last-name": "@any" if last_name is None else last_name,
            "bio": "@any" if bio is None else bio,
            "username": "@any" if username is None else username,
            "limit": limit,
            "offset": offset
        }
    ).accept(ContentType.APPLICATION_JSON).execute(http_session)

    if status == 200:
        return FindUserResponse(**json.loads(raw_response))

    return APIError(
        status=status,
        response=ErrorResponse(**json.loads(raw_response))
    )
