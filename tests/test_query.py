from os import environ
from typing import AsyncGenerator

from psycopg import AsyncConnection
from pytest import fixture

from sync.query import get_all_rows, get_all_rows_query


@fixture
async def database_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with await AsyncConnection.connect(environ.get("DATABASE_DSN", "")) as aconn:
        yield aconn
        await aconn.rollback()


async def create_test_database_data(database_connection: AsyncConnection) -> None:
    async with database_connection.cursor() as cursor:
        await cursor.execute(
            """
        CREATE TABLE test_table (
            whatsapp varchar(20),
            field1 varchar(20),
            field2 varchar(20)
        )
        """
        )
        await cursor.execute(
            """
        INSERT INTO test_table(whatsapp, field1, field2) VALUES
            ('27820001001', 'c1f1', 'c1f2'),
            ('27820001002', 'c2f1', 'c2f2')
        """
        )


async def test_get_all_rows_query(database_connection: AsyncConnection):
    """
    Properly escapes the table name in the query
    """
    query = get_all_rows_query("test_table")
    assert query.as_string(database_connection) == 'SELECT * FROM "test_table"'

    query = get_all_rows_query('test " \0 ')
    assert query.as_string(database_connection) == 'SELECT * FROM "test "" "'


async def test_get_all_rows(database_connection: AsyncConnection):
    """
    Fetches all the rows from the table, and returns them as dictionaries
    """
    await create_test_database_data(database_connection)

    rows = [r async for r in get_all_rows(database_connection, "test_table")]
    assert sorted(rows, key=lambda r: r["whatsapp"]) == [
        {"field1": "c1f1", "field2": "c1f2", "whatsapp": "27820001001"},
        {"field1": "c2f1", "field2": "c2f2", "whatsapp": "27820001002"},
    ]
