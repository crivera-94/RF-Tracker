#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    ZetCode PyQt5 tutorial
    
    This program creates a skeleton of
    a classic GUI application with a menubar,
    toolbar, statusbar, and a central widget.
    
    author: Jan Bodnar
    website: zetcode.com
    last edited: January 2015
    """

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction,
                             QApplication, QGridLayout, QWidget,
                             QLabel, QFrame, QSlider)
from PyQt5.QtGui import QIcon
from circle import CircleWidget

class RFTracker(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    
    def initUI(self):
        
        textEdit = QTextEdit()
        
        # Create main widget to house all other widgets
        main_widget = QWidget()
        layout = QGridLayout()
        main_widget.setLayout(layout)
        
        
        label = self.createLabel(text = "SAMPLE")
        label2 = self.createLabel(text = "ASDF")
        layout.addWidget(label2, 0, 0)
        layout.addWidget(label, 1, 1)
        
        
        plot = CircleWidget()
        plot.update()
        layout.addWidget(plot, 0, 1)
        
        slider = QSlider(Qt.Vertical, self)
        layout.addWidget(slider, 0, 2)

        
        # SET LAYOUT AND SET AS CENTER
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)


        # Actions
        exitAction = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        # Status Bar
        self.statusBar().showMessage('Ready')
        
        # Menu Bar
        menubar = self.menuBar()
        
        # File Menu and actions
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        
        # Edit Menu and actions
        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(exitAction)


        # Tool Bar
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        
        
        self.showFullScreen()
        self.setWindowTitle('RF Tracker')
        self.show()
    

    def createLabel(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setMargin(2)
        label.setFrameStyle(QFrame.Box | QFrame.Sunken)
        return label


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = RFTracker()
    sys.exit(app.exec_())