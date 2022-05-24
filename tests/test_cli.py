from contextlib import asynccontextmanager
from os import environ
from unittest.mock import MagicMock, patch

from psycopg import AsyncConnection

from sync.cli import main
from tests.test_query import create_test_database_data
from tests.test_rapidpro import TestClient


@patch("sync.cli.create_session")
@patch("sync.cli.AsyncConnection")
async def test_main(
    mock_connection: MagicMock,
    create_session: MagicMock,
    database_connection: AsyncConnection,
    fake_whatsapp: TestClient,
):
    """
    This test does a lot of mocking, but that's okay because we've unit tested
    all of the components already, we just want to make sure that they all work together
    """
    environ.setdefault("DATABASE_DSN", "")
    environ.setdefault("DATABASE_TABLE", "test_table")
    environ.setdefault("RAPIDPRO_HOST", "example.org")
    environ.setdefault("RAPIDPRO_TOKEN", "testtoken")
    environ.setdefault("URN_TYPE", "whatsapp")
    await create_test_database_data(database_connection)
    create_session.return_value = fake_whatsapp

    async def mock_connect(dsn):
        """
        We need to mock with an async function, that returns an async context manager,
        that returns the database connection, in order to mirror the psycopg API
        """
        assert dsn == ""

        @asynccontextmanager
        async def connect():
            yield database_connection

        return connect()

    mock_connection.connect = mock_connect
    await main()
    assert fake_whatsapp.app is not None
    [r1, r2] = sorted(fake_whatsapp.app["requests"], key=lambda r: r.query["urn"])
    assert r1.query == {"urn": "whatsapp:27820001001"}
    assert await r1.json() == {"fields": {"field1": "c1f1", "field2": "c1f2"}}
    assert r2.query == {"urn": "whatsapp:27820001002"}
    assert await r2.json() == {"fields": {"field1": "c2f1", "field2": "c2f2"}}
