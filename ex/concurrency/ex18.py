import asyncio
import time

async def other(id, t):
    await asyncio.sleep(t)
    print(f"I am a coroutine {id}")
    return t + 2

async def serial():
    start = time.perf_counter()
    await other(1, 10)
    await other(2, 4)
    await other(3, 1)
    end = time.perf_counter()
    elapsed_time = end - start
    print(f"Elapsed time {elapsed_time}")


async def concurrent():
    start = time.perf_counter()
    t1 = asyncio.create_task(other(1, 10))
    t2 = asyncio.create_task(other(2, 4))
    t3 = asyncio.create_task(other(3, 1))
    await t1
    await t2
    await t3
    end = time.perf_counter()
    elapsed_time = end - start
    print(f"Elapsed time {elapsed_time}")

async def gather():
    start = time.perf_counter()
    results = await asyncio.gather(
        other(1, 10),
        other(2, 4),
        other(3, 1),
    )
    end = time.perf_counter()
    elapsed_time = end - start
    print(f"Elapsed time {elapsed_time}")
    print(f"The results are: {results}")


if __name__ == '__main__':
    # asyncio.run(serial())
    # asyncio.run(concurrent())
    asyncio.run(gather())
