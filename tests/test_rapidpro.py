from aiohttp.test_utils import TestClient

from sync.rapidpro import create_session, update_contact


async def test_update_contact(fake_whatsapp: TestClient):
    await update_contact(
        session=fake_whatsapp,
        urn_type="whatsapp",
        urn_value="27820001001",
        fields={"field": "value"},
    )
    assert fake_whatsapp.app is not None
    [request] = fake_whatsapp.app["requests"]
    assert request.query == {"urn": "whatsapp:27820001001"}
    assert await request.json() == {"fields": {"field": "value"}}


async def test_create_session():
    session = await create_session("example.org", "testtoken", 7)
    assert session.headers == {
        "Authorization": "Token testtoken",
        "User-Agent": "postgresql-to-rapidpro-sync",
    }
    assert str(session._base_url) == "https://example.org"
    assert session.connector.limit == 7
