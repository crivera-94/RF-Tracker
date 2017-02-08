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
        exitAction = QAction('&Exit')
        #exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        
        self.statusBar()
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Menubar')
        self.show()
        
        
        
        
        # Status Bar
        self.statusBar().showMessage('Ready')
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Statusbar')
        self.show()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())