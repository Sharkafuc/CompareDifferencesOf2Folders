# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTreeWidget,QTreeWidget,QTreeWidgetItem
from tree import Tree,TreeNode

class TreeWidget(QTreeWidget):
    def __init__(self, treedata, parent=None):
        QTreeWidget.__init__(self,parent)
        self.setTreeData(treedata)

    def setTreeData(self,treedata):
        if treedata and isinstance(treedata,Tree):
            self.setColumnCount(1)
            # 设置头部信息，因为上面设置列数为2，所以要设置两个标识符
            self.setHeaderLabels([treedata.name])
            # 设置root为self.tree的子树，所以root就是跟节点
            root = self.createTreeFromTreedata(treedata)
            self.addTopLevelItem(root)

    def createTreeFromTreedata(self,treedata):
        root = QTreeWidgetItem(self)
        if treedata and isinstance(treedata, Tree):
            root.setText(0,treedata.root.name)
            self.visitCreateTreeNode(treedata.root,root)
        return root

    def visitCreateTreeNode(self,treeNode,widgetItem):
        childs = treeNode.get_childs()
        for name,child in childs.items():
            childNode = QTreeWidgetItem(widgetItem)
            childNode.setText(0,name)
            if len(child.get_childs().keys())>0:
                self.visitCreateTreeNode(child,childNode)
