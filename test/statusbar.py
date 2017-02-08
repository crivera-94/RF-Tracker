#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    ZetCode PyQt5 tutorial
    
    This program creates a statusbar.
    
    author: Jan Bodnar
    website: zetcode.com
    last edited: January 2015
    """

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QApplication
from PyQt5.QtGui import QIcon


class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    
    def initUI(self):
        
        # Menu Bar
        self.menuBar = QtWidgets.QMenuBar(Example)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 480, 22))
        self.menuBar.setObjectName("menuBar")
        
        # Menu Bar Options
        file = self.menuBar.addMenu('&File')
        edit = self.menuBar.addMenu('&Edit')
        options = self.menuBar.addMenu('&Options')
        
        # File Actions
        exit_action = file.addAction('Exit')
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)

        
        # Status Bar
        self.statusBar().showMessage('Ready')
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Statusbar')
        self.show()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())