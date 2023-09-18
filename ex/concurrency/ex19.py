import asyncio
from loguru import logger
import sys


async def get_result(future):
    await asyncio.sleep(5)
    future.set_result("... an awaited result")

async def main():
    my_future = asyncio.Future()
    t1 = asyncio.create_task(get_result(my_future))
    await t1
    logger.debug("I'm waiting for ...")
    logger.debug(await my_future)
    logger.debug("Before continuing with my execution")


if __name__ == "__main__":
    logger.remove(0)
    logger.add(sys.stderr, level="TRACE")
    logger.trace("A trace message")
    logger.warning("A warning message")
    logger.debug("Starting ...")
    asyncio.run(main())
    logger.debug("Finished ...")

