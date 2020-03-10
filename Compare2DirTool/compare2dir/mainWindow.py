# -*- coding: utf-8 -*-
import sys
from PyQt5 import sip
from PyQt5.QtWidgets import QWidget,QMainWindow
from PyQt5.QtCore import QTimer
from compare2dir.resultWidget import ResultWidget
from compare2dir.selectWidget import SelectWidgetView
from mymvc.GameMediator import GameMediator
from manager.updateMgr import UpdateMgr

class MainWidgetView(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        #view绑定Mediator
        GameMediator.registViewMediator(self,MainWidgetMediator)
        self.resultMenu = None
        self.selectMenu = None

        #定时器
        self.appTimer = QTimer(self)
        self.appTimer.start()
        self.appTimer.setInterval(1000/30)
        self.appTimer.timeout.connect(self.loop)

        self.setWindowTitle('文件夹比对工具')
        self.createOrUpdateSelectMenu()
        self.createOrUpdateResultMenu(None)
        self.setCentralWidget(self.selectMenu)

        self.move(100,100)

    def createOrUpdateResultMenu(self,compareResult):
        if self.resultMenu and sip.isdeleted(self.resultMenu) == False :
            self.resultMenu.destroy()
        self.resultMenu = ResultWidget(compareResult)

    def createOrUpdateSelectMenu(self):
        if self.selectMenu and sip.isdeleted(self.selectMenu) == False:
            self.selectMenu.destroy()
        self.selectMenu = SelectWidgetView()

    def setCentralWidget(self,widget):
        super().setCentralWidget(widget)
        self.setFixedSize(widget.sizeHint())

    def loop(self):
        UpdateMgr().update()

class MainWidgetMediator(GameMediator):
    NAME = "MainWidgetMediator"
    def __init__(self,viewComponent):
        GameMediator.__init__(self,MainWidgetMediator.NAME,viewComponent)
        self.init()

    def init(self):
        pass

    def listNotificationInterests(self):
        from compareCommand import CompareCommand

        self.handler_list = {
            CompareCommand.back_to_select_cmd:self.back_to_select_cmd_handler,
            CompareCommand.show_compare_result_cmd:self.show_compare_result_cmd_handler
        }

        return list(self.handler_list.keys())

    def back_to_select_cmd_handler(self,notification):
        self.getView().createOrUpdateSelectMenu()
        self.getView().setCentralWidget(self.getView().selectMenu)

    def show_compare_result_cmd_handler(self,notification):
        self.getView().createOrUpdateResultMenu(notification)
        self.getView().setCentralWidget(self.getView().resultMenu)


