from loguru import logger
import trio


async def child1():
    logger.info(f" child1 started! sleeping 1 second now...")
    await trio.sleep(5)
    logger.info(f" child1: exiting!")

async def child2():
    logger.info(f" child2 started! sleeping 1 second now...")
    await trio.sleep(5)
    logger.info(f" child2: exiting!")

async def parent():
    logger.info(f"parent started!")
    async with trio.open_nursery() as nursery:
        logger.info(f"parent: spawning child1...")
        nursery.start_soon(child1)
        
        logger.info(f"parent: spawning child2...")
        nursery.start_soon(child2)
        
        logger.info(f"parent: waiting for children to finish...")
    logger.info(f"parent: all done!")

def main():
    trio.run(parent)


if __name__ == "__main__":
    main()

