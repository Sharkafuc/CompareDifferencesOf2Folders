# -*- coding: utf-8 -*-
from treeWidgetBase import TreeWidgetBase
from data.notificationData import *
from data.constData import *
from mymvc.GameFacade import GameFacade
from editCommand import EditCommand
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from common.tree import *

class EditTreeWidget(TreeWidgetBase):

    def __init__(self, treename, rootname, parent=None):
        from common.tree import Tree, TreeNode
        treedata = Tree(TreeNode(rootname), treename)
        TreeWidgetBase.__init__(self,treedata,None,parent)

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

    def singleClickHandler(self, item):
        send_data = self.getClickFileData(item)
        print("single click:", send_data.open_path, item.text(0))
        GameFacade().sendNotification(EditCommand.single_click_file_cmd, send_data)

    def rightMenuShow(self):
        self.contextMenu = QMenu(self)
        curItem = self.currentItem()
        if curItem is not None and curItem is not self.root:
            if self.name == add_modify_tree_name:
                self.WithDraw = self.contextMenu.addAction('撤销增加或修改')
            elif self.name == remove_tree_name:
                self.WithDraw = self.contextMenu.addAction('撤销删除')
            self.WithDraw.triggered.connect(lambda: self.WithDrawEvent(curItem))
            self.contextMenu.exec_(QCursor.pos())

    def WithDrawEvent(self,item):
        print("withdraw event",item.text(0))
        item_data = self.getClickFileData(item)
        node_path = item_data.open_path + "/" + item_data.file_name
        if self.treedata and isinstance(self.treedata,Tree):
            self.treedata.delete_child_by_path(node_path)
            self.updateTree()