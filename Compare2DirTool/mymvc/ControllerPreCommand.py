# -*- coding: utf-8 -*-
from puremvc.patterns.command import SimpleCommand
from compareCommand import CompareCommand
from editCommand import EditCommand

class ControllerPreCommand(SimpleCommand):
    def __init__(self):
        SimpleCommand.__init__(self)

    def execute(self, notification):
        CompareCommand.regist()
        EditCommand.regist()