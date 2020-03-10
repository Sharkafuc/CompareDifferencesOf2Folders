# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget,QPushButton,QLabel,QHBoxLayout,QVBoxLayout
from compare2dir.resultTreeWidget import ResultTreeWidget
from mymvc.GameFacade import GameFacade

class ResultWidget(QWidget):
    def __init__(self, compare_result ,parent=None):
        QWidget.__init__(self,parent)
        self.init(compare_result)

    def init(self,compare_result):
        if compare_result == None:
            return

        #数据
        different_dirs_cnt = compare_result["different_dirs_cnt"]
        different_files_cnt = compare_result["different_files_cnt"]
        treedata1 = compare_result["only_dir1_tree"]
        treedata2 = compare_result["only_dir2_tree"]
        treedata3 = compare_result["modified_tree"]

        #显示结果数据
        self.different_dir_label = QLabel("不同的文件夹个数："+str(different_dirs_cnt))
        self.different_file_label = QLabel("不同的文件个数：" + str(different_files_cnt))
        ext_info = {
            "path_dir1": compare_result["path_dir1"],
            "path_dir2": compare_result["path_dir2"],
        }
        self.tree1 = ResultTreeWidget(treedata1, ext_info)
        self.tree2 = ResultTreeWidget(treedata2, ext_info)
        self.tree3 = ResultTreeWidget(treedata3, ext_info)
        self.tree1.setFixedWidth(450)
        self.tree2.setFixedWidth(450)
        self.tree3.setFixedWidth(450)
        backButton = QPushButton('返回')
        backButton.clicked.connect(self.onBackButtonClick)
        exportButton = QPushButton("导出编辑结果")
        exportButton.setStyleSheet("background-color: #00FF7F")
        exportButton.clicked.connect(self.onExportButtonClick)
        buttonBox = QWidget()
        buttonBox_layout = QHBoxLayout()
        buttonBox.setLayout(buttonBox_layout)
        buttonBox_layout.addWidget(backButton)
        buttonBox_layout.addWidget(exportButton)
        buttonBox_layout.setStretch(0,1)
        buttonBox_layout.setStretch(1,2)

        #编辑结果数据
        from editWidget import EditWidget
        self.editWidget = EditWidget(ext_info)

        #主layout
        main_layout = QHBoxLayout()
        result_show_widget = QWidget()
        main_layout.addWidget(result_show_widget)
        main_layout.addWidget(self.editWidget)

        #左侧layout
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.different_dir_label)
        left_layout.addWidget(self.different_file_label)
        left_layout.addWidget(self.tree1)
        left_layout.addWidget(self.tree2)
        left_layout.addWidget(self.tree3)
        left_layout.addWidget(buttonBox)
        result_show_widget.setLayout(left_layout)

        self.setLayout(main_layout)

    def onBackButtonClick(self):
        from compareCommand import CompareCommand
        GameFacade().sendNotification(CompareCommand.back_to_select_cmd)

    def onExportButtonClick(self):
        from editCommand import EditCommand
        GameFacade().sendNotification(EditCommand.export_edit_trees_cmd)