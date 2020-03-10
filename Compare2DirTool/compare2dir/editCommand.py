# -*- coding: utf-8 -*-
from puremvc.patterns.command import SimpleCommand
class EditCommand(SimpleCommand):

    NAME = "EditCommand"

    # cmd
    single_click_file_cmd = "single_click_file_cmd"
    add_file_to_target_dir_cmd = "add_file_to_target_dir_cmd"
    remove_file_from_target_dir_cmd = "remove_file_from_target_dir_cmd"
    export_edit_trees_cmd = "export_edit_trees_cmd"

    commands = [
    ]

    def __init__(self):
        SimpleCommand.__init__(self)

    @classmethod
    def regist(cls):
        for command in EditCommand.commands:
            from mymvc.GameFacade import GameFacade
            GameFacade().registerCommand(command,EditCommand)

    @classmethod
    def remove(cls):
        for command in EditCommand.commands:
            from mymvc.GameFacade import GameFacade
            GameFacade().removeCommand(command)

    def execute(self, notification):
        cmd = notification.getName().lower()
        handler_name = 'do_'+cmd
        if hasattr(self,handler_name):
            handler = getattr(self,handler_name)
            handler(notification.getBody())