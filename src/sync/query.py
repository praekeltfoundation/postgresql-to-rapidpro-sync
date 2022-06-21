from typing import AsyncIterator

import psycopg
from psycopg import AsyncConnection
from psycopg.sql import SQL, Composed, Identifier

# Fix for Redshift
# https://github.com/psycopg/psycopg/issues/122
psycopg._encodings._py_codecs["UNICODE"] = "utf-8"
psycopg._encodings.py_codecs.update(
    (k.encode(), v) for k, v in psycopg._encodings._py_codecs.items()
)

CURSOR_NAME = "rapidpro_sync"


def get_all_rows_query(table: str) -> Composed:
    """
    SQL query for getting all rows from the table
    """
    return SQL("SELECT * FROM {table}").format(table=Identifier(table))


async def get_all_rows(
    connection: AsyncConnection, table: str
) -> AsyncIterator[dict[str, str]]:
    """
    Async iterator that returns all the rows of the table, as dictionaries
    """
    async with connection.cursor(name=CURSOR_NAME) as cursor:
        await cursor.execute(get_all_rows_query(table))
        if cursor.description is None:
            raise ValueError("No column description in cursor")
        columns = [col.name for col in cursor.description]
        async for record in cursor:
            yield dict(zip(columns, record))
