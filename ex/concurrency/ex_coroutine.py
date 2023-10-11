import asyncio
from loguru import logger
from util.delay import delay


async def add_one(number: int) -> int:
    return number + 1


async def hello_world_message() -> str:
    await delay(1)
    return "Hello World!"


async def ex01() -> None:
    logger.info("main started.")
    message = await hello_world_message()
    one_plus_one = await add_one(1)
    logger.info(f"one plus one: {one_plus_one}")
    logger.info(f"message: {message}")


async def ex02() -> None:
    sleep_for_three = asyncio.create_task(delay(3))
    logger.info(type(sleep_for_three))
    result = await sleep_for_three
    logger.info(f"result: {result}")


async def ex03() -> None:
    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(3))
    sleep_once_more = asyncio.create_task(delay(3))

    await sleep_for_three
    await sleep_again
    await sleep_once_more


async def hello_every_second() -> None:
    for i in range(2):
        await asyncio.sleep(1)
        logger.info("I'm running other code while I'm waiting!")


async def ex04() -> None:
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))
    await hello_every_second()
    await first_delay
    await second_delay


async def ex05() -> None:
    long_task = asyncio.create_task(delay(10))

    seconds_elapsed = 0

    while not long_task.done():
        logger.info("Task not finished, checking again in 1 second!")
        await asyncio.sleep(1)
        seconds_elapsed += 1
        logger.info(f"seconds elapsed: {seconds_elapsed}")
        if seconds_elapsed >= 5:
            long_task.cancel()

    try:
        await long_task
    except asyncio.CancelledError as e:
        logger.info(f'Our task was cancelled. Reason: {e}')


async def ex06() -> None:
    delay_task = asyncio.create_task(delay(2))
    try:
        result = await asyncio.wait_for(delay_task, timeout=1)
        logger.info(f'Result: {result}')
    except asyncio.exceptions.TimeoutError:
        logger.info('Got a timeout')
        logger.info(f'Was the task cancelled? {delay_task.cancelled()}')


async def ex07() -> None:
    task = asyncio.create_task(delay(10))

    try:
        result = await asyncio.wait_for(asyncio.shield(task), 5)
        logger.info(f'Result: {result}')
    except asyncio.exceptions.TimeoutError:
        logger.info('Task took longer than five seconds, it will finish soon!')
        result = await task
        logger.info(f'Result: {result}')


asyncio.run(ex07())
