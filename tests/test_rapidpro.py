import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from sync.rapidpro import update_contact


@pytest.fixture
async def fake_whatsapp(aiohttp_client) -> TestClient:
    app = web.Application()
    app["requests"] = []

    async def contacts(request):
        app["requests"].append(request)
        # Load the body so that we can assert on it
        await request.text()
        return web.Response()

    app.add_routes([web.post("/api/v2/contacts.json", contacts)])
    return await aiohttp_client(app)


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
