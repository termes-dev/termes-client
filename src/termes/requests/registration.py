import json
from typing import Final

from aiohttp import ClientSession

from .request import ContentType, Request, RequestMethod
from ..types.errors import APIError
from ..types.requests import RegistrationRequest
from ..types.responses import ErrorResponse, RegistrationResponse

REGISTRATION_ENDPOINT: Final[str] = "/registration/"


async def register(
        host: str,
        data: RegistrationRequest,
        http_session: ClientSession | None = None
) -> RegistrationResponse | APIError:
    status, raw_response = await Request(
        host=host,
        method=RequestMethod.POST,
        endpoint=REGISTRATION_ENDPOINT,
        data=data.json()
    ).content_type(ContentType.APPLICATION_JSON).execute(http_session)

    if status == 200:
        return RegistrationResponse(**json.loads(raw_response))

    return APIError(
        status=status,
        response=ErrorResponse(**json.loads(raw_response))
    )
