# -*- coding: utf-8 -*-
from common.Singleton import Singleton
from common.Coroutine import Coroutine
class CoroutineManager(metaclass=Singleton):
    def __init__(self):
        super(CoroutineManager, self).__init__()
        self._coroutines = []

    def update(self):
        if not self.hasCoroutine():
            return

        for coroutine in self._coroutines:
            try:
                coroutine.next()
            except StopIteration:
                self._coroutines.remove(coroutine)

    def startCoroutine(self, generator):
        coroutine = Coroutine(generator)
        self._coroutines.append(coroutine)
        return coroutine

    def removeCoroutine(self, coroutine):
        if coroutine and coroutine in self._coroutines:
            self._coroutines.remove(coroutine)

    def clear(self):
        self._coroutines = []

    def hasCoroutine(self):
        if len(self._coroutines) > 0:
            return True
        else:
            return False

def waitForSeconds(second):
    import time
    curTime = time.time()
    endTime = curTime + second
    while curTime < endTime:
        yield
        curTime = time.time()

#test demo
def mycoroutine():
    print("等待3s后say hello")
    yield waitForSeconds(3)
    print("say hello")

if __name__ == "__main__":
    coroutMg = CoroutineManager()
    coroutMg.startCoroutine(mycoroutine())
    while 1:
        coroutMg.update()