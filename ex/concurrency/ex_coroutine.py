import asyncio
from asyncio import Future
import time
from loguru import logger
import requests
from util.delay import async_timed, delay


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


def make_request() -> Future:
    future = Future()
    asyncio.create_task(set_future_value(future))
    return future


async def set_future_value(future) -> None:
    await asyncio.sleep(1)
    future.set_result(28)


async def ex08() -> None:
    future = make_request()
    logger.info(f'Is the future done? {future.done()}')
    value = await future
    logger.info(f'Is thre future done? {future.done()}')
    logger.info(f'value: {value}')


async def ex09() -> None:
    start = time.time()
    await asyncio.sleep(1)
    end = time.time()
    elapsed_time = end - start
    logger.info(f"Elapsed time {elapsed_time}")


@async_timed()
async def ex10() -> None:
    task_one = asyncio.create_task(delay(2))
    task_two = asyncio.create_task(delay(3))

    await task_one
    await task_two


@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for i in range(100000000):
        counter += 1
    return counter


@async_timed()
async def ex11() -> None:
    task_one = asyncio.create_task(cpu_bound_work())
    task_two = asyncio.create_task(cpu_bound_work())
    await task_one
    await task_two


@async_timed()
async def ex12() -> None:
    task_one = asyncio.create_task(cpu_bound_work())
    task_two = asyncio.create_task(cpu_bound_work())
    delay_task = asyncio.create_task(delay(4))
    await task_one
    await task_two
    await delay_task


@async_timed()
async def get_example_status() -> int:
    return requests.get('http://www.example.com').status_code


@async_timed()
async def ex13() -> None:
    task1 = asyncio.create_task(get_example_status())
    task2 = asyncio.create_task(get_example_status())
    task3 = asyncio.create_task(get_example_status())
    await task1
    await task2
    await task3


def ex14() -> None:
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(delay(2))
    finally:
        loop.close()


def call_later() -> None:
    logger.info("I'm being called in the future!")


@async_timed()
async def ex15() -> None:
    # loop = asyncio.get_running_loop()
    loop = asyncio.get_event_loop()
    loop.call_soon(call_later)
    await delay(1)


async def ex16() -> None:
    loop = asyncio.get_running_loop()
    loop.slow_callback_duration = .250


asyncio.run(ex16(), debug=True)
# ex16()
