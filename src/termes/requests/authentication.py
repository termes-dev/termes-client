import json
from typing import Final

from aiohttp import ClientSession

from .request import ContentType, Request, RequestMethod
from ..types.errors import APIError
from ..types.requests import AuthenticationRequest
from ..types.responses import AuthenticationResponse, ErrorResponse

AUTHENTICATION_ENDPOINT: Final[str] = "/authentication/"


async def authenticate(
        host: str,
        data: AuthenticationRequest,
        http_session: ClientSession | None = None
) -> AuthenticationResponse | APIError:
    status, raw_response = await Request(
        host=host,
        method=RequestMethod.POST,
        endpoint=AUTHENTICATION_ENDPOINT,
        data=data.json()
    ).content_type(ContentType.APPLICATION_JSON).execute(http_session)

    if status == 200:
        return AuthenticationResponse(**json.loads(raw_response))

    return APIError(
        status=status,
        response=ErrorResponse(**json.loads(raw_response))
    )

