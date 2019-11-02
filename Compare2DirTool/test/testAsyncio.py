# -*- coding: utf-8 -*-
import asyncio

async def foo(x):
    a = 0
    print("执行协程")
    #async 不是重入
    await asyncio.sleep(2)
    print("执行完毕")

if __name__ == "__main__":
    print("操作1")
    loop = asyncio.get_event_loop()
    try:
        print("开始协程")
        task = loop.create_task(foo(5))
        print("开始eventloop")
        loop.run_until_complete(task)
    except:
        pass
    print("操作2")