from typing import AsyncIterator

from psycopg import AsyncConnection
from psycopg.sql import SQL, Composed, Identifier


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
    async with connection.cursor() as cursor:
        await cursor.execute(get_all_rows_query(table))
        if cursor.description is None:
            raise ValueError("No column description in cursor")
        columns = [col.name for col in cursor.description]
        async for record in cursor:
            yield dict(zip(columns, record))
