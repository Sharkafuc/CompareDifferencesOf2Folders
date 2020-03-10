# -*- coding: utf-8 -*-
import asyncio

async def foo(x):
    while True:
        print("执行{0}s协程".format(x))
        await asyncio.sleep(x)
        print("{0}s执行完毕".format(x))

async def main():
    coroutine1 = foo(3)
    coroutine2 = foo(2)
    coroutine3 = foo(1)
    tasks = [
        asyncio.create_task(coroutine1),
        asyncio.create_task(coroutine2),
        asyncio.create_task(coroutine3)
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except:
        pass
    loop.close()
    print("后续操作")