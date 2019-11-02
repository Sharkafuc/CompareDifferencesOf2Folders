# -*- coding: utf-8 -*-
from mymvc.GameFacade import GameFacade
from PyQt5.QtWidgets import QWidget,QPushButton,QGridLayout,QFileDialog,QLineEdit,QMessageBox,QProgressBar
from calculator import compare2DirDifferents
from mymvc.GameMediator import GameMediator
import os

class SelectWidgetView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        GameMediator.registViewMediator(self, selectWidgetMediator)
        self.init()

    def init(self):
        self.FolderInputText1 = QLineEdit("目录1地址")
        self.FolderInputText1.setFixedWidth(500)

        self.FolderInputText2 = QLineEdit("目录2地址")
        self.FolderInputText2.setFixedWidth(500)

        self.selectFolder1Btn = QPushButton("选择目录1")
        self.selectFolder2Btn = QPushButton("选择目录2")

        self.compareButton = QPushButton('比较')
        self.compareButton.setFixedWidth(100)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(0, 0, 500, 25)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)

        layout = QGridLayout()
        layout.addWidget(self.FolderInputText1, 0, 0)
        layout.addWidget(self.FolderInputText2, 1, 0)
        layout.addWidget(self.selectFolder1Btn,0,1)
        layout.addWidget(self.selectFolder2Btn,1,1)
        layout.addWidget(self.compareButton, 2, 1)
        layout.addWidget(self.progressBar,2, 0)

        self.setLayout(layout)
        self.bindButtonEvents()

    def onCompareButtonClick(self):
        path_dir1 = self.FolderInputText1.text()
        path_dir2 = self.FolderInputText2.text()
        if os.path.isdir(path_dir1) == False or os.path.isdir(path_dir2) == False:
            QMessageBox.information(self, "tips", "选择正确的文件夹路径")
            return

        from manager.CorotineMgr import CoroutineManager
        CoroutineManager().startCoroutine(compare2DirDifferents(path_dir1,path_dir2))

    def onSelectFolderClick(self,selectIndex):
        cwd = os.getcwd()
        dir_choose = QFileDialog.getExistingDirectory(self,"选取文件夹",cwd)
        folderInputText = None
        if selectIndex == 1:
            folderInputText = self.FolderInputText1
        elif selectIndex == 2:
            folderInputText = self.FolderInputText2
        if folderInputText:
            if dir_choose:
                folderInputText.setText(dir_choose)

    def bindButtonEvents(self):
        self.compareButton.clicked.connect(self.onCompareButtonClick)
        self.selectFolder1Btn.clicked.connect(lambda: self.onSelectFolderClick(1))
        self.selectFolder2Btn.clicked.connect(lambda: self.onSelectFolderClick(2))

class selectWidgetMediator(GameMediator):
    NAME = "selectWidgetMediator"

    def __init__(self,viewComponent):
        GameMediator.__init__(self,selectWidgetMediator.NAME,viewComponent)
        self.init()
    def init(self):
        pass

    def listNotificationInterests(self):
        from compareCommand import CompareCommand

        self.handler_list = {
            CompareCommand.show_compare_progress_cmd:self.show_compare_progress_cmd_handler,
            CompareCommand.hide_compare_progress_cmd:self.hide_compare_progress_cmd_handler
        }

        return list(self.handler_list.keys())

    def show_compare_progress_cmd_handler(self,notification):
        value = notification
        self.getView().progressBar.setValue(value)
        self.getView().progressBar.setVisible(True)

    def hide_compare_progress_cmd_handler(self,notification):
        self.getView().progressBar.setValue(0)
        self.getView().progressBar.setVisible(False)