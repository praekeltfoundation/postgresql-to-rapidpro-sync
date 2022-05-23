from psycopg.sql import SQL, Composed, Identifier


def get_all_rows_query(table: str) -> Composed:
    return SQL("SELECT * FROM {table}").format(table=Identifier(table))
