# -*- coding: utf-8 -*-
from puremvc.patterns.command import MacroCommand
from mymvc.ControllerPreCommand import ControllerPreCommand

class StartupCommand(MacroCommand):

    def __init__(self):
        MacroCommand.__init__(self)

    def initializeMacroCommand(self):
        self.addSubCommand(ControllerPreCommand)

    def execute(self, notification):
        super().execute(notification)

