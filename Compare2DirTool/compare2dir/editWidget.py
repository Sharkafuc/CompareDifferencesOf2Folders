# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QListWidget,QListWidgetItem,QLabel,QMessageBox
from PyQt5.QtGui import QPixmap
from mymvc.GameFacade import GameFacade
from mymvc.GameMediator import GameMediator
from data.notificationData import *
from previewLabel import PreviewLabel
from editTreeWidget import EditTreeWidget
from common.tree import *
from data.constData import *
from manager.editResultMgr import EditResultMgr

class EditWidget(QWidget):
    def __init__(self,ext_info,parent=None):
        QWidget.__init__(self,parent)
        GameMediator.registViewMediator(self, EditWidgetMediator)

        ext_data = compare_dir_paths_data(path_dir1= ext_info['path_dir1'],path_dir2= ext_info['path_dir2'])
        self.dir1 = ext_data.path_dir1
        self.dir2 = ext_data.path_dir2

        main_layout = QVBoxLayout()
        topWidget = QWidget()
        self.add_List = EditTreeWidget("添加/修改树",self.dir1)
        self.add_List.setFixedSize(500, 700)
        self.remove_list = EditTreeWidget("删除树",self.dir2)
        self.remove_list.setFixedSize(500, 700)
        self.add_edit_result_to_target_dir()

        downWidget = QWidget()
        self.dir1preview = PreviewLabel(0)
        self.dir1preview.setFixedSize(500, 500)
        self.dir1preview.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(0.5, 0.5, 0.5);")
        self.dir2preview = PreviewLabel(1)
        self.dir2preview.setFixedSize(500, 500)
        self.dir2preview.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(0.5, 0.5, 0.5);")

        list_layout = QHBoxLayout()
        preview_layout = QHBoxLayout()

        add_list_box = QWidget()
        add_list_box_layout = QVBoxLayout()
        add_list_box.setLayout(add_list_box_layout)
        remove_list_box = QWidget()
        remove_list_box_layout = QVBoxLayout()
        remove_list_box.setLayout(remove_list_box_layout)
        add_list_box_layout.addWidget(QLabel("向目录2添加的文件:"))
        add_list_box_layout.addWidget(self.add_List)
        remove_list_box_layout.addWidget(QLabel("目录2删除的文件:"))
        remove_list_box_layout.addWidget(self.remove_list)
        list_layout.addWidget(add_list_box)
        list_layout.addWidget(remove_list_box)

        preview1Box = QWidget()
        preview1Box_layout = QVBoxLayout()
        preview1Box.setLayout(preview1Box_layout)
        preview2Box = QWidget()
        preview2Box_layout = QVBoxLayout()
        preview2Box.setLayout(preview2Box_layout)
        preview1Box_layout.addWidget(QLabel("目录1文件预览:"))
        preview1Box_layout.addWidget(self.dir1preview)
        preview2Box_layout.addWidget(QLabel("目录2文件预览:"))
        preview2Box_layout.addWidget(self.dir2preview)
        preview_layout.addWidget(preview1Box)
        preview_layout.addWidget(preview2Box)

        topWidget.setLayout(list_layout)
        downWidget.setLayout(preview_layout)
        main_layout.addWidget(topWidget)
        main_layout.addWidget(downWidget)

        self.setLayout(main_layout)

    def add_edit_result_to_target_dir(self):
        self.add_edit_result_to_dir_core(self.add_List,edit_result_add_file_name)
        self.add_edit_result_to_dir_core(self.remove_list,edit_result_remove_file_name)

    def add_edit_result_to_dir_core(self,add_list,resultfile):
        target_dir_results =  EditResultMgr().getTargetDirResult(resultfile,add_list.treedata.root.path)
        add_tree = add_list.treedata
        if len(target_dir_results) > 0 and add_list and isinstance(add_tree,Tree):
            for file in target_dir_results:
                filename = file.replace(add_list.treedata.root.path,"")
                add_tree.addFilePathToTree(filename)
            add_list.updateTree()

    def add_treenode_to_target_dir(self,open_path,tree_node):
        self.add_treenode_to_dir_core(open_path, tree_node, self.add_List);

    def remove_treenode_to_target_dir(self,open_path,tree_node):
        self.add_treenode_to_dir_core(open_path,tree_node,self.remove_list);

    def add_treenode_to_dir_core(self,open_path,tree_node, add_list):
        #把open_path 加入树
        if add_list is self.add_List:
            open_path = open_path.replace(self.dir1,"")
        else:
            open_path = open_path.replace(self.dir2,"")
        patharr = open_path.split("/")
        patharr = [file for file in patharr if file.strip() != ""]
        pathNode = add_list.treedata.root
        for pathfile in patharr:
            if pathNode:
                childNode = pathNode.get_child(pathfile)
                if childNode is None:
                    newNode = TreeNode(pathfile)
                    pathNode.add_child(newNode)
                    pathNode = newNode
                else:
                    pathNode = childNode

        #处理节点的父关系
        from copy import deepcopy
        add_node = deepcopy(tree_node)
        pathNode.add_child(add_node)
        add_list.updateTree()

class EditWidgetMediator(GameMediator):
    NAME = "EditWidgetMediator"

    def __init__(self, viewComponent):
        GameMediator.__init__(self, EditWidgetMediator.NAME, viewComponent)
        self.init()

    def init(self):
        pass

    def listNotificationInterests(self):
        from editCommand import EditCommand

        self.handler_list = {
            EditCommand.single_click_file_cmd: self.single_click_file_cmd_handler,
            EditCommand.add_file_to_target_dir_cmd: self.add_file_to_target_dir_cmd_handler,
            EditCommand.remove_file_from_target_dir_cmd:self.remove_file_to_target_dir_cmd_handler,
            EditCommand.export_edit_trees_cmd:self.export_edit_trees_cmd_handler,
        }
        return list(self.handler_list.keys())

    def single_click_file_cmd_handler(self,notification):
        notification_data = click_file_data(open_path=notification.open_path, file_name=notification.file_name, path_list=notification.path_list)
        print(notification_data.open_path,notification_data.file_name,notification_data.path_list)

        # 判断是否是图片
        file_name = notification_data.file_name
        open_path = notification_data.open_path
        path_list = notification_data.path_list
        from util.fileUtils import isImageFile
        if isImageFile(file_name):
            self.drawImagePreview(file_name,open_path,path_list)

    def drawImagePreview(self,file_name,open_path,path_list):
        editWidgetView = self.getView()
        dir1 = editWidgetView.dir1
        dir2 = editWidgetView.dir2

        if open_path.find(modified_tree_root) > -1:
            path1 = open_path.replace(modified_tree_root,dir1)
            path2 = open_path.replace(modified_tree_root,dir2)
            self.showTargetPreview(editWidgetView.dir1preview, path1, file_name, path_list)
            self.showTargetPreview(editWidgetView.dir2preview, path2, file_name, path_list)
        else:
            targetPreview = editWidgetView.dir1preview
            if open_path.find(dir2) > -1:
                targetPreview = editWidgetView.dir2preview
            self.showTargetPreview(targetPreview,open_path,file_name,path_list)

    def showTargetPreview(self,target,open_path,file_name,path_list):
        print("preview pixmap:",open_path + "/" + file_name)
        target.setData(click_file_data(open_path=open_path, file_name=file_name, path_list=path_list))
        from PyQt5.QtCore import Qt
        pixmap = QPixmap(open_path + "/" + file_name).scaled(target.width(), target.height(),Qt.KeepAspectRatio, Qt.SmoothTransformation)
        target.setPixmap(pixmap)

    def add_file_to_target_dir_cmd_handler(self,notification):
        edit_tree_data = add_to_edit_tree_data(open_path=notification.open_path, tree_node=notification.tree_node)
        open_path = edit_tree_data.open_path
        tree_node = edit_tree_data.tree_node
        editWidgetView = self.getView()
        editWidgetView.add_treenode_to_target_dir(open_path,tree_node)

    def remove_file_to_target_dir_cmd_handler(self,notification):
        edit_tree_data = add_to_edit_tree_data(open_path=notification.open_path, tree_node=notification.tree_node)
        open_path = edit_tree_data.open_path
        tree_node = edit_tree_data.tree_node
        editWidgetView = self.getView()
        editWidgetView.remove_treenode_to_target_dir(open_path, tree_node)

    def export_edit_trees_cmd_handler(self,notification):
        print("导出对目录2的编辑结果")
        editWidgetView = self.getView()
        #以main.py 为参照
        add_file_path =  edit_result_add_file_name
        remove_file_path = edit_result_remove_file_name

        QMessageBox.information(editWidgetView, "tips", "导出成功")
        EditResultMgr().writeEditTreeToResult(editWidgetView.add_List.treedata,add_file_path)
        EditResultMgr().writeEditTreeToResult(editWidgetView.remove_list.treedata,remove_file_path)




