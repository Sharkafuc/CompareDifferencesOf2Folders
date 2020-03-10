# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTreeWidget,QTreeWidgetItem
from common.tree import Tree
from PyQt5.QtCore import Qt

class TreeWidgetBase(QTreeWidget):
    def __init__(self, treedata, ext_info, parent=None):
        QTreeWidget.__init__(self,parent)
        self.name = ""
        self.root_text = ""
        self.ext_info = ext_info
        self.setTreeData(treedata)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)  # 开放右键策略

    def setTreeData(self,treedata):
        from copy import deepcopy
        self.treedata = deepcopy(treedata)
        self.updateTree()

    def visitCreateTreeNode(self,treeNode,widgetItem):
        childs = treeNode.get_childs()
        for name,child in childs.items():
            childNode = QTreeWidgetItem(widgetItem)
            childNode.setText(0,name)
            childNode.setToolTip(0,name)
            if len(child.get_childs().keys())>0:
                self.visitCreateTreeNode(child,childNode)

    def createTreeFromTreedata(self,treedata):
        root = QTreeWidgetItem(self)
        if treedata and isinstance(treedata, Tree):
            root.setText(0,treedata.root.name)
            root.setToolTip(0, treedata.root.name)
            self.visitCreateTreeNode(treedata.root,root)
        self.itemDoubleClicked.connect(self.doubleClickHandler)
        self.itemClicked.connect(self.singleClickHandler)
        self.expandAll()
        return root

    def updateTree(self):
        treedata = self.treedata
        if treedata and isinstance(treedata,Tree):
            self.clear()
            self.setColumnCount(1)
            # 设置头部信息，因为上面设置列数为2，所以要设置两个标识符
            self.setHeaderLabels([treedata.name])
            self.name = treedata.name
            self.root_text = treedata.root.name
            # 设置root为self.tree的子树，所以root就是跟节点
            root = self.createTreeFromTreedata(treedata)
            self.addTopLevelItem(root)
            self.root = root

    def removeTree(self):
        pass

    def doubleClickHandler(self, item):
        pass

    def singleClickHandler(self, item):
        pass

    def rightMenuShow(self):
        pass