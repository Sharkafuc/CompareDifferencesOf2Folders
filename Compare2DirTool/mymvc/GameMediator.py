# -*- coding: utf-8 -*-
from puremvc.patterns.mediator import Mediator
from mymvc.GameFacade import GameFacade
class GameMediator(Mediator):
    def __init__(self,mediatorname,viewcomp):
        Mediator.__init__(self,mediatorname,viewcomp)
        self.handler_list = {}

    @classmethod
    def registViewMediator(cls,view,mediatorCls):
        mediator = mediatorCls(view)
        #删除旧的mediator和ui
        oldMediator = GameFacade().retrieveMediator(mediatorCls.NAME)
        if oldMediator:
            GameFacade.getInstance().removeMediator(mediatorCls.NAME)
            try:
                oldMediator.viewComponent.destroy()
            except:
                print("旧view component已删除")

        GameFacade().registerMediator(mediator)

        #绑定删除
        oldViewDestroy = None
        if hasattr(view, "destroy"):
            oldViewDestroy = getattr(view, "destroy")

        def onViewDestroy(self, destroyWindow=True, destroySubWindows=True):
            if oldViewDestroy:
                oldViewDestroy(destroyWindow,destroySubWindows)
            if mediatorCls.NAME and  mediatorCls.NAME != "" and isinstance(mediatorCls.NAME,str):
                GameFacade.getInstance().removeMediator(mediatorCls.NAME)

        from types import MethodType
        view.destroy = MethodType(onViewDestroy, view)

    def handleNotification(self,notification):
        handler = self.handler_list[notification.getName()]
        if handler:
            handler(notification.getBody())

    def getView(self):
        return self.viewComponent