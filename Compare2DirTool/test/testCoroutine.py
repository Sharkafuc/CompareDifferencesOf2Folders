# -*- coding: utf-8 -*-

from types import GeneratorType
from common.Singleton import Singleton
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


class Coroutine(object):

    def __init__(self, generator):
        super(Coroutine, self).__init__()
        self._stack = [generator]

    def next(self):
        length = len(self._stack)
        coroutine = self._stack[length - 1]
        try:
            while True:
                if coroutine == None:
                    raise StopIteration
                result = next(coroutine)
                if isinstance(result, GeneratorType):
                    self._stack.append(result)
                    coroutine = result
                    length += 1
                else:
                    break
        except StopIteration:
            if length == 1:
                raise
            else:
                self._stack = self._stack[:length - 1]


def waitForSeconds(second):
    import time
    curTime = time.time()
    endTime = curTime + second
    while curTime < endTime:
        yield
        curTime = time.time()
    return

def mycoroutine():
    print("等待3s后say hello")
    yield waitForSeconds(3)
    print("say hello")


if __name__ == "__main__":
    coroutMg = CoroutineManager()
    coroutMg.startCoroutine(mycoroutine())
    while 1:
        coroutMg.update()




