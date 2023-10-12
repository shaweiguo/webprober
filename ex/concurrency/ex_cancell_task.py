import asyncio
import signal
import typing

from loguru import logger

from util.delay import delay


def cancel_tasks():
    logger.info("Got a SIGINT!")
    tasks: typing.Set[asyncio.Task] = asyncio.all_tasks()
    logger.info(f"Cancelling {len(tasks)} task(s).")
    [task.cancel() for task in tasks]


async def cancel_tasks():
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, cancel_tasks)
    await delay(5)
    await delay(8)
    await delay(10)


class GracefulExit(SystemExit):
    pass


def shutdown():
    raise GracefulExit()


def graceful_exit():
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, shutdown)
    
    try:
        loop.run_until_complete(wait_tasks())
    except GracefulExit:
        loop.run_until_complete(close_echo_tasks(echo_tasks))
    finally:
        loop.close()


async def close_echo_tasks(echo_tasks: typing.List[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            pass
    tasks = asyncio.all_tasks()
    [await task for task in tasks]


async def wait_tasks():
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT,
                            lambda: asyncio.create_task(await_all_tasks()))




asyncio.run(wait_tasks())
