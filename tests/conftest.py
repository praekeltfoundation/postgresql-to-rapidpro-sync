from os import environ
from typing import AsyncGenerator

from aiohttp import web
from aiohttp.test_utils import TestClient
from psycopg import AsyncConnection
from pytest import fixture


@fixture
async def database_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with await AsyncConnection.connect(environ.get("DATABASE_DSN", "")) as aconn:
        try:
            yield aconn
        finally:
            await aconn.rollback()


@fixture
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
