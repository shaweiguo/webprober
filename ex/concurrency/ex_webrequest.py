import asyncio
import logging
import sys
import aiohttp
from util.delay import async_timed
from loguru import logger


async def fetch_status(session: aiohttp.ClientSession,
                       url: str,
                       delay: int = 0) -> int:
    await asyncio.sleep(delay)
    async with session.get(url) as response:
        return {url: response.status}


@async_timed()
async def ascompleted() -> None:
    async with aiohttp.ClientSession() as session:
        fetchers = [fetch_status(session, 'https://www.example.com', 1),
                    fetch_status(session, 'https://www.example.com', 1),
                    fetch_status(session, 'https://www.example.com', 10),]
        for finished_task in asyncio.as_completed(fetchers):
            logger.info(await finished_task)


@async_timed()
async def ascompleted_timeout() -> None:
    async with aiohttp.ClientSession() as session:
        urls = [
            ('https://www.example.com', 1),
            ('https://www.example.com', 1),
            ('https://www.example.com', 10),
        ]
        # fetchers = [
        #     (fetch_status(session, url[0], url[1]), url[0]) for url in urls
        # ]
        fetchers = {
            fetch_status(session, url[0], url[1]): url[0] for url in urls
        }

        # for finished_task in asyncio.as_completed(fetchers.keys()):
        #     logger.info(await finished_task)
        # tasks = []
        # for item in fetchers:
        #     tasks.append(item[0])
        for done_task in asyncio.as_completed(fetchers.keys(), timeout=5):
            # url = ''
            # for item in fetchers:
            #     if item[0] == done_task:
            #         url = item[1]
            try:
                result = await done_task
                logger.info(f'{result}')
            except asyncio.TimeoutError as e:
                logger.info(f'{e}: timeout!')

        for task in asyncio.tasks.all_tasks():
            logger.info(f'{task}: {task.done()}')


@async_timed()
async def wait_request() -> None:
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'https://example.com')),
            asyncio.create_task(fetch_status(session, 'https://example.com')),
        ]
        done, pending = await asyncio.wait(fetchers)

        logger.info(f'Done task count: {len(done)}')
        logger.info(f'Pending task count: {len(pending)}')

        for done_task in done:
            result = await done_task
            logger.info(f'{result}')


@async_timed()
async def fetch_with_exception() -> None:
    # logger.remove(0)
    # logger.add(sys.stderr, format="\
    #            {time:MMMM D, YYYY > HH:mm:ss} | {level} | {message} | {extra}")
    async with aiohttp.ClientSession() as session:
        good_request = fetch_status(session, 'https://example.com')
        bad_request = fetch_status(session, 'python://bad')

        fetchers = [
            asyncio.create_task(good_request),
            asyncio.create_task(bad_request)
        ]
        done, pending = await asyncio.wait(fetchers)

        logger.info(f'Done task count: {len(done)}')
        logger.info(f'Pending task count: {len(pending)}')

        for done_task in done:
            ex = done_task.exception()
            if ex is None:
                logger.info(f'{done_task.result()}')
            else:
                # logger.error(f'Request got an exception: {ex}')
                logging.error('Request got an exception', exc_info=ex)


@async_timed()
async def fetch_with_cancel() -> None:
    async with aiohttp.ClientSession() as session:
        good_request = fetch_status(session, 'https://example.com', delay=3)
        good_request1 = fetch_status(session, 'https://example.com', delay=3)
        bad_request = fetch_status(session, 'python://bad')

        fetchers = [
            asyncio.create_task(bad_request),
            asyncio.create_task(good_request),
            asyncio.create_task(good_request1),
        ]
        done, pending = await asyncio.wait(fetchers,
                                           return_when=asyncio.FIRST_EXCEPTION)

        logger.info(f'Done task count: {len(done)}')
        logger.info(f'Pending task count: {len(pending)}')

        for done_task in done:
            ex = done_task.exception()
            if ex is None:
                logger.info(f'{done_task.get_name()} {done_task.result()}')
            else:
                # logger.error(f'Request got an exception: {ex}')
                logging.error(
                    f'{done_task.get_name()} Request got an exception',
                    exc_info=ex)

        for pending_task in pending:
            pending_task.cancel()


@async_timed()
async def fetch_with_complete() -> None:
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'

        fetchers = [
            asyncio.create_task(fetch_status(session, url), name='task1'),
            asyncio.create_task(fetch_status(session, url), name='task2'),
            asyncio.create_task(fetch_status(session, url), name='task3'),
        ]
        done, pending = await asyncio.wait(
            fetchers,
            return_when=asyncio.FIRST_COMPLETED)

        logger.info(f'Done task count: {len(done)}')
        logger.info(f'Pending task count: {len(pending)}')

        for done_task in done:
            logger.info(await done_task)

        for pending_task in pending:
            logger.info(f'{pending_task.get_name()}')


@async_timed()
async def fetch_with_process() -> None:
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'
        pending = [
            asyncio.create_task(fetch_status(session, url), name='task1'),
            asyncio.create_task(fetch_status(session, url), name='task2'),
            asyncio.create_task(fetch_status(session, url), name='task3'),
        ]

        while pending:
            done, pending = await asyncio.wait(
                pending,
                return_when=asyncio.FIRST_COMPLETED)

            logger.info(f'Done task count: {len(done)}')
            logger.info(f'Pending task count: {len(pending)}')

            for done_task in done:
                logger.info(f'{done_task.get_name()} done.'
                            f' result: {await done_task}')

            for pending_task in pending:
                logger.info(f'{pending_task.get_name()}')


@async_timed()
async def fetch_with_wait() -> None:
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'
        fetchers = [
            asyncio.create_task(fetch_status(session, url), name='task1'),
            asyncio.create_task(fetch_status(session, url), name='task2'),
            asyncio.create_task(
                fetch_status(session, url, delay=5),
                name='task3'),
        ]
        done, pending = await asyncio.wait(fetchers, timeout=3)

        logger.info(f'Done task count: {len(done)}')
        logger.info(f'Pending task count: {len(pending)}')

        for done_task in done:
            logger.info(f'{done_task.get_name()} done.'
                        f' result: {await done_task}')

        for pending_task in pending:
            logger.info(f'{pending_task.get_name()} pending.')


@async_timed()
async def fetch_without_task() -> None:
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'
        api_a = fetch_status(session, url)
        api_b = fetch_status(session, url, delay=3)

        done, pending = await asyncio.wait([api_a, api_b], timeout=2)

        logger.info(f'Done task count: {len(done)}')
        logger.info(f'Pending task count: {len(pending)}')

        for done_task in done:
            logger.info(f'{done_task.get_name()} done.'
                        f' result: {await done_task}')

        for pending_task in pending:
            if pending_task is api_b:
                logger.info(f'{pending_task.get_name()} pending, canceling...')
                pending_task.cancel()


if __name__ == '__main__':
    asyncio.run(fetch_without_task())
