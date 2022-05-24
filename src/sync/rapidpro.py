from logging import getLogger
from urllib.parse import SplitResult, urlunsplit

from aiohttp import ClientSession, TCPConnector

logger = getLogger(__name__)


async def create_session(host: str, token: str, concurrency: int) -> ClientSession:
    url = urlunsplit(
        SplitResult(scheme="https", netloc=host, path="", query="", fragment="")
    )
    connector = TCPConnector(limit=concurrency)

    return ClientSession(
        base_url=url,
        connector=connector,
        headers={
            "Authorization": f"Token {token}",
            "User-Agent": "postgresql-to-rapidpro-sync",
        },
    )


async def update_contact(
    session: ClientSession, urn_type: str, urn_value: str, fields: dict[str, str]
) -> None:
    """
    Updates the fields of the contact with the given URN
    """
    response = await session.post(
        "/api/v2/contacts.json",
        params={"urn": f"{urn_type}:{urn_value}"},
        json={"fields": fields},
    )
    if not response.ok:
        logger.error(
            "Received error response %s with body %s",
            response.status,
            await response.text(),
        )
