from loguru import logger
import asyncio
import random


async def producer(name, queue):
    n = random.randint(0, 10)
    await asyncio.sleep(n)
    await queue.put(n)
    logger.info(f"Producer {name} adds {n} to the queue")

async def consumer(name, queue):
    while True:
        n = await queue.get()
        await asyncio.sleep(n)
        logger.info(f"Consumer {name} reveives {n} from the queue")
        queue.task_done()

async def async_queue(nproducers, nconsumers):
    q = asyncio.Queue()
    producers = [asyncio.create_task(producer(n, q)) for n in range(nproducers)]
    consumers = [asyncio.create_task(consumer(n, q)) for n in range(nconsumers)]
    await asyncio.gather(*producers)
    await q.join()
    for c in consumers:
        c.cancel()

def main():
    asyncio.run(async_queue(4, 2))


if __name__ == '__main__':
    main()
