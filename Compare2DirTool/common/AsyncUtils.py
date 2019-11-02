# -*- coding: utf-8 -*-

import asyncio

def startAsyncFuction(foo):
    loop = asyncio.get_event_loop()
    try:
        print("开始异步方法")
        task = loop.create_task(foo(5))
        print("结束异步方法")
        loop.run_until_complete(task)
    except:
        pass
