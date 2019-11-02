# -*- coding: utf-8 -*-
from common.Singleton import Singleton
from common.Handler import Handler

class UpdateMgr(metaclass=Singleton):

    def __init__(self):
        super(UpdateMgr, self).__init__()
        from manager.CorotineMgr import CoroutineManager
        self.updateHandlers = {}
        self.addHandlerByName("CorroutineMgrUpdate",Handler(CoroutineManager(),CoroutineManager().update))

    def update(self):
        for name,handler in self.updateHandlers.items():
            if isinstance(handler,Handler):
                handler.run()

    def addHandlerByName(self,name,handler):
        self.updateHandlers[name] = handler

    def removeHandler(self,name):
        del self.updateHandlers[name]
