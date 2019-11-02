# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget,QGridLayout,QPushButton,QLabel
from compare2dir.treeWidget import TreeWidget
from mymvc.GameFacade import GameFacade

class ResultWidget(QWidget):
    def __init__(self, compare_result ,parent=None):
        QWidget.__init__(self,parent)
        self.init(compare_result)

    def init(self,compare_result):
        if compare_result == None:
            return

        different_dirs_cnt = compare_result["different_dirs_cnt"]
        different_files_cnt = compare_result["different_files_cnt"]
        treedata1 = compare_result["only_dir1_tree"]
        treedata2 = compare_result["only_dir2_tree"]
        treedata3 = compare_result["modified_tree"]

        self.different_dir_label = QLabel("不同的文件夹个数："+str(different_dirs_cnt))
        self.different_file_label = QLabel("不同的文件个数：" + str(different_files_cnt))
        self.tree1 = TreeWidget(treedata1)
        self.tree2 = TreeWidget(treedata2)
        self.tree3 = TreeWidget(treedata3)
        backButton = QPushButton('返回')
        backButton.clicked.connect(self.onBackButtonClick)

        layout = QGridLayout()
        layout.addWidget(self.different_dir_label,0,0)
        layout.addWidget(self.different_file_label,1,0)
        layout.addWidget(self.tree1, 2, 0)
        layout.addWidget(self.tree2, 3, 0)
        layout.addWidget(self.tree3, 4, 0)
        layout.addWidget(backButton, 5, 0)
        self.setLayout(layout)

    def onBackButtonClick(self):
        from compareCommand import CompareCommand
        GameFacade().sendNotification(CompareCommand.back_to_select_cmd)