import asyncio
from os import environ

from aiohttp import ClientSession
from psycopg import AsyncConnection

from sync.config import Config
from sync.query import get_all_rows
from sync.rapidpro import create_session, update_contact


async def rapidpro_worker(
    config: Config, session: ClientSession, queue: asyncio.Queue
) -> None:
    while True:
        row = await queue.get()
        urn_value = row.pop(config.urn_type)
        await update_contact(
            session=session, urn_type=config.urn_type, urn_value=urn_value, fields=row
        )
        queue.task_done()


async def main():
    config = Config.from_environment(environ)
    queue = asyncio.Queue(maxsize=config.concurrency)
    session = await create_session(
        host=config.rapidpro_host,
        token=config.rapidpro_token,
        concurrency=config.concurrency,
    )
    worker_tasks = [
        asyncio.create_task(
            rapidpro_worker(config=config, session=session, queue=queue)
        )
        for _ in range(config.concurrency)
    ]

    async with await AsyncConnection.connect(config.database_dsn) as conn:
        async for row in get_all_rows(connection=conn, table=config.database_table):
            await queue.put(row)
    await queue.join()

    for worker_task in worker_tasks:
        worker_task.cancel()
    await asyncio.gather(*worker_tasks, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
