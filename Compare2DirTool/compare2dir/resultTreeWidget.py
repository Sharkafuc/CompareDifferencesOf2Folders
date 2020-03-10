# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QCursor
from treeWidgetBase import TreeWidgetBase
from data.constData import *
from mymvc.GameFacade import GameFacade
from editCommand import EditCommand
from data.notificationData import *
from common.tree import *

class ResultTreeWidget(TreeWidgetBase):

    def __init__(self,treedata, ext_info, parent=None):
        TreeWidgetBase.__init__(self,treedata, ext_info, parent)
        self.dir1 = self.ext_info["path_dir1"]
        self.dir2 = self.ext_info["path_dir2"]

    def doubleClickHandler(self,item):
        visit = item
        paths = []
        #paths.append(visit.text(0))
        while visit.parent():
            visit = visit.parent()
            paths.append(visit.text(0))
        paths.reverse()
        openPath = "/".join(paths)
        print(openPath, item.text(0))

        if self.root_text == "modify_root":
            print("modify_root")
            path1 = openPath.replace("modify_root",self.dir1)
            path2 = openPath.replace("modify_root", self.dir2)
            self.selectExploreFile(path1, item.text(0))
            self.selectExploreFile(path2, item.text(0))
        else:
            self.selectExploreFile(openPath,item.text(0))

    def singleClickHandler(self, item):
        send_data = self.getClickFileData(item)
        print("single click:", send_data.open_path, item.text(0))
        GameFacade().sendNotification(EditCommand.single_click_file_cmd, send_data)

    def selectExploreFile(self,openPath,single_file):
        import os
        cmd = "{0}".format(openPath + "/" + single_file)
        cmd = cmd.replace("/", "\\")
        cmd = "explorer /select, " + cmd
        os.system(cmd)
        print(cmd)

    def rightMenuShow(self):
        self.contextMenu = QMenu(self)
        curItem = self.currentItem()
        if curItem is not None and curItem is not self.root:
            if self.name == dir1_tree_name:
                self.AddFile = self.contextMenu.addAction('增加到目录2')
                self.AddFile.triggered.connect(lambda:self.AddFileEvent(curItem))
            elif self.name == dir2_tree_name:
                self.RmoveFile = self.contextMenu.addAction('从目录2删除')
                self.RmoveFile.triggered.connect(lambda:self.RemoveFileEvent(curItem))
            elif self.name == modified_tree_name:
                self.AddFile = self.contextMenu.addAction('替换到目录2')
                self.AddFile.triggered.connect(lambda:self.AddFileEvent(curItem))
            self.contextMenu.exec_(QCursor.pos())

    def getClickFileData(self,item):
        visit = item
        paths = []
        while visit.parent():
            visit = visit.parent()
            paths.append(visit.text(0))
        paths.reverse()
        openPath = "/".join(paths)
        send_data = click_file_data(open_path=openPath, file_name=item.text(0), path_list=paths)
        return send_data

    def AddFileEvent(self,item):
        print("add file event",item.text(0))
        item_data = self.getClickFileData(item)
        node_path = item_data.open_path + "/" + item_data.file_name
        if self.treedata and isinstance(self.treedata,Tree):
            treenode = self.treedata.find_child_by_path(node_path)
            open_path = item_data.open_path
            if open_path.find(modified_tree_root) > -1:
                open_path = open_path.replace(modified_tree_root,self.dir1)
            edit_tree_data = add_to_edit_tree_data(open_path=open_path,tree_node=treenode)
            GameFacade.getInstance().sendNotification(EditCommand.add_file_to_target_dir_cmd,edit_tree_data)

    def RemoveFileEvent(self,item):
        print("remove file event",item.text(0))
        item_data = self.getClickFileData(item)
        node_path = item_data.open_path + "/" + item_data.file_name
        if self.treedata and isinstance(self.treedata, Tree):
            treenode = self.treedata.find_child_by_path(node_path)
            open_path = item_data.open_path
            edit_tree_data = add_to_edit_tree_data(open_path=open_path, tree_node=treenode)
            GameFacade.getInstance().sendNotification(EditCommand.remove_file_from_target_dir_cmd, edit_tree_data)