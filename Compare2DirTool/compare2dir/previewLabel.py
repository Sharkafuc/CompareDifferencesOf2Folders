# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel,QMenu,QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from common.tree import *
from mymvc.GameFacade import GameFacade
from data.notificationData import *
from editCommand import EditCommand

class PreviewLabel(QLabel):
    def __init__(self, preview_dir_type , preview_data = None):
        QLabel.__init__(self)
        self.dir_type = preview_dir_type
        self.preview_data = preview_data

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)  # 开放右键策略

    def setData(self,preview_data):
        self.preview_data = click_file_data(open_path=preview_data.open_path, file_name=preview_data.file_name, path_list=preview_data.path_list)
        self.setToolTip(self.preview_data.open_path +"/" + self.preview_data.file_name)

    def rightMenuShow(self, pos):  # 添加右键菜单
        if(self.preview_data is not None):
            self.contextMenu = QMenu(self)

            if self.dir_type == 0 :
                self.AddFile = self.contextMenu.addAction('增加到目录2')
                self.AddFile.triggered.connect(self.AddFileEvent)
            else:
                self.RmoveFile = self.contextMenu.addAction('从目录2删除')
                self.RmoveFile.triggered.connect(self.RemoveFileEvent)
            self.contextMenu.exec_(QCursor.pos())

    def AddFileEvent(self):
        item_data = self.preview_data
        print("add file event",item_data)
        treenode = TreeNode(item_data.file_name)
        edit_tree_data = add_to_edit_tree_data(open_path=item_data.open_path, tree_node=treenode)
        GameFacade.getInstance().sendNotification(EditCommand.add_file_to_target_dir_cmd, edit_tree_data)

    def RemoveFileEvent(self):
        item_data = self.preview_data
        print("remove file event", item_data)
        treenode = TreeNode(item_data.file_name)
        edit_tree_data = add_to_edit_tree_data(open_path=item_data.open_path, tree_node=treenode)
        GameFacade.getInstance().sendNotification(EditCommand.remove_file_from_target_dir_cmd, edit_tree_data)
