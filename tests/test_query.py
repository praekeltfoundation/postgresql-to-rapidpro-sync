from os import environ
from typing import AsyncGenerator

from psycopg import AsyncConnection
from pytest import fixture

from sync.query import get_all_rows_query


@fixture
async def database_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with await AsyncConnection.connect(environ.get("DATABASE_DSN", "")) as aconn:
        yield aconn


async def test_get_all_rows(database_connection: AsyncConnection):
    query = get_all_rows_query("test_table")
    assert query.as_string(database_connection) == 'SELECT * FROM "test_table"'

    query = get_all_rows_query('test " \0 ')
    assert query.as_string(database_connection) == 'SELECT * FROM "test "" "'
