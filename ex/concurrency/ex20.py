import asyncio
from loguru import logger


async def gen_serial(n):
    for i in range(n):
        await asyncio.sleep(1)
        yield i

async def countdown_serial():
    async for i in gen_serial(10):
        logger.info(i)

async def gen(n):
    logger.info(f"start iteration step {n}")
    await asyncio.sleep(1)
    logger.info(f"end iteration step {n}")
    return n

async def countdown():
    for j in asyncio.as_completed([gen(i) for i in range(10)]):
        result = await j
        logger.info(f"result received: {result}")

def main():
    asyncio.run(countdown_serial())
    asyncio.run(countdown())


if __name__ == "__main__":
    main()
