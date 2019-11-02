# -*- coding: utf-8 -*-
from puremvc.patterns.command import SimpleCommand
class CompareCommand(SimpleCommand):

    NAME = "CompareCommand"

    #cmd
    start_compare_main_window_cmd = "start_compare_main_window_cmd"
    back_to_select_cmd = "back_to_select_cmd"
    show_compare_result_cmd = "show_compare_result_cmd"
    show_compare_progress_cmd = "show_compare_progress_cmd"
    hide_compare_progress_cmd = "hide_compare_progress_cmd"

    commands = [
        start_compare_main_window_cmd,
    ]

    def __init__(self):
        SimpleCommand.__init__(self)

    @classmethod
    def regist(cls):
        for command in CompareCommand.commands:
            from mymvc.GameFacade import GameFacade
            GameFacade().registerCommand(command,CompareCommand)

    @classmethod
    def remove(cls):
        for command in CompareCommand.commands:
            from mymvc.GameFacade import GameFacade
            GameFacade().removeCommand(command)

    def execute(self, notification):
        cmd = notification.getName().lower()
        handler_name = 'do_'+cmd
        if hasattr(self,handler_name):
            handler = getattr(self,handler_name)
            handler(notification.getBody())

    def do_start_compare_main_window_cmd(self,notification):
        from mainWindow import MainWidgetView
        from PyQt5.QtWidgets import QApplication
        import sys
        app = QApplication(sys.argv)
        app.aboutToQuit.connect(app.deleteLater)
        tp = MainWidgetView()
        tp.show()
        app.exec_()