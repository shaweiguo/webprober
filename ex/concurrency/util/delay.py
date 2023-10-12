import asyncio
import functools
import time
from typing import Any, Callable
from loguru import logger


def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            logger.info(f"starting {func} with args {args} {kwargs}")
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                logger.info(f"finished {func} in {total:.4f} second(s)")
        return wrapped
    return wrapper


# async def delay(delay_seconds: int) -> int:
#     logger.info(f'sleeping for {delay_seconds} second(s)')
#     await asyncio.sleep(delay_seconds)
#     logger.info(f'finished sleeping for {delay_seconds} second(s)')
#     return delay_seconds
@async_timed()
async def delay(delay_seconds: int) -> int:
    logger.info(f"sleeping for {delay_seconds} second(s)")
    await asyncio.sleep(delay_seconds)
    logger.info(f"finished sleeping for {delay_seconds} second(s)")
    return delay_seconds
