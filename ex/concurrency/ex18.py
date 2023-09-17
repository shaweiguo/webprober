import asyncio

async def other(id, t):
    await asyncio.sleep(t)
    print(f"I am a coroutine {id}")

async def main():
    t1 = asyncio.create_task(other(1, 10))
    t2 = asyncio.create_task(other(2, 4))
    t3 = asyncio.create_task(other(3, 1))
    await t1
    await t2
    await t3


if __name__ == '__main__':
    asyncio.run(main())
