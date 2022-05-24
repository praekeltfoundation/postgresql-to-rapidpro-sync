from aiohttp import ClientSession


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
