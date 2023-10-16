import asyncio
import aiohttp
from loguru import logger
from util.delay import async_timed, delay


@async_timed()
async def delay_tasks() -> None:
    delay_times = [3, 3, 3]
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    [await task for task in tasks]


@async_timed()
async def fetch_status(session: aiohttp.ClientSession, url: str) -> int:
    # ten_millis = aiohttp.ClientTimeout(total=1)
    # async with session.get(url, timeout=ten_millis) as response:
    async with session.get(url) as response:
        return response.status


@async_timed()
async def fetch():
    session_timeout = aiohttp.ClientTimeout(total=5, connect=3)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        url = 'https://www.example.com'
        status = await fetch_status(session, url)
        logger.info(f'Status for {url} was {status}')


@async_timed()
async def fetcher() -> None:
    async with aiohttp.ClientSession() as session:
        urls = ['https://www.example.com' for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        logger.info(f'Status codes:\r\n{status_codes}')


asyncio.run(fetcher())
