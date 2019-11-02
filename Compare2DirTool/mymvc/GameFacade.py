# -*- coding: utf-8 -*-
from puremvc.patterns.facade import Facade
from common.Singleton import Singleton
from mymvc.StartupCommand import StartupCommand

class GameFacade(Facade,metaclass=Singleton):
    start_up_cmd = "start_up_cmd"

    def __init__(self):
        Facade.__init__(self)

    def initializeController(self):
        super().initializeController()
        self.registerCommand(GameFacade.start_up_cmd,StartupCommand)

    def startUp(self):
        self.sendNotification(GameFacade.start_up_cmd)
        self.removeCommand(GameFacade.start_up_cmd)
        from compareCommand import CompareCommand
        self.sendNotification(CompareCommand.start_compare_main_window_cmd)