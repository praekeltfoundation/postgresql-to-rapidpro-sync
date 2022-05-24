from urllib.parse import SplitResult, urlunsplit

from aiohttp import BaseConnector, ClientSession


async def create_session(host: str, token: str, concurrency: int) -> ClientSession:
    url = urlunsplit(
        SplitResult(scheme="https", netloc=host, path="", query="", fragment="")
    )
    connector = BaseConnector(limit=concurrency)

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
    await session.post(
        "api/v2/contacts.json",
        params={"urn": f"{urn_type}:{urn_value}"},
        json={"fields": fields},
        raise_for_status=True,
    )
