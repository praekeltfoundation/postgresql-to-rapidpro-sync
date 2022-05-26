import asyncio
from logging import INFO, basicConfig, getLogger
from os import environ
from time import monotonic

from aiohttp import ClientSession
from psycopg import AsyncConnection

from sync.config import Config
from sync.query import get_all_rows
from sync.rapidpro import create_session, update_contact

logger = getLogger(__name__)
basicConfig(level=INFO)


async def rapidpro_worker(
    config: Config, session: ClientSession, queue: asyncio.Queue
) -> None:
    logger.info("Started worker")
    async with session as s:
        while True:
            row = await queue.get()
            try:
                urn_value = row.pop(config.urn_type)
                await update_contact(
                    session=s, urn_type=config.urn_type, urn_value=urn_value, fields=row
                )
            except Exception:
                logger.exception("Error updating contact")
            queue.task_done()


async def async_main():
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

    start = monotonic()
    count = 0
    async with await AsyncConnection.connect(config.database_dsn) as conn:
        async for row in get_all_rows(connection=conn, table=config.database_table):
            await queue.put(row)
            count += 1
            if monotonic() - start > 1:
                logger.info(
                    "Processing %s contacts per second",
                    (count - queue.qsize()) / (monotonic() - start),
                )
                count = 0
                start = monotonic()

    await queue.join()
    for worker_task in worker_tasks:
        worker_task.cancel()
    await asyncio.gather(*worker_tasks, return_exceptions=True)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
