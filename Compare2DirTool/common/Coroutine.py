# -*- coding: utf-8 -*-
from types import GeneratorType
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
                return
            else:
                self._stack = self._stack[:length - 1]