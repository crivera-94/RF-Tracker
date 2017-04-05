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
import time
import phasedetector
import globals

from PyQt5.QtCore import Qt, QTimer, QThread
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction,
                             QApplication, QGridLayout, QWidget,
                             QLabel, QFrame, QSlider,
                             QDialog, QLineEdit, QPushButton, QVBoxLayout, QMessageBox)
from PyQt5 import QtGui
from plot import Plot
from phasedetector import PhaseDetector
from threadpackage import ADCThread
from threadpackage import FilterThread


# Define a function for the thread
def print_time(thread_name, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print("%s: %s" % (thread_name, time.ctime(time.time())))


#class UpdateGUI(QThread):
    #data_downloaded = QtCore.pyqtSignal(object)

    #def __init__(self, url):
        #QtCore.QThread.__init__(self)
        #self.url = url

    #def run(self):
        #info = urllib2.urlopen(self.url).info()
        #self.data_downloaded.emit('%s\n%s' % (self.url, info))

# http://stackoverflow.com/questions/11812000/login-dialog-pyqt
class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handle_login)
        username_label = QLabel("Username:")
        password_label = QLabel("Password:")
        layout = QGridLayout(self)
        layout.addWidget(username_label, 0, 0)
        layout.addWidget(password_label, 1, 0)
        layout.addWidget(self.textName, 0, 1)
        layout.addWidget(self.textPass, 1, 1)
        layout.addWidget(self.buttonLogin, 2, 1)
        self.setWindowTitle('RF Tracker')

    def handle_login(self):
        if self.textName.text() == 'foo' and self.textPass.text() == 'bar':
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Bad user or password')


class RFTracker(QMainWindow):
    def __init__(self):
        self.MAX_ACCURATE_RANGE = 2047
        self.MIN_ACCURATE_RANGE = 50
        super().__init__()
        self.initUI()

    def initUI(self):
        textEdit = QTextEdit()
        
        # Create main widget to house all other widgets
        main_widget = QWidget()
        layout = QGridLayout()
        main_widget.setLayout(layout)

        label = self.createLabel(text="SAMPLE")
        label2 = self.createLabel(text="TEST TABLE")
        layout.addWidget(label2, 0, 0)
        layout.addWidget(label, 0, 1)
        # layout.addWidget(label, 1, 1)
        
        # Make Plot
        plot = Plot()
        layout.addWidget(plot, 0, 2)
        slider = QSlider(Qt.Vertical, self)
        slider.setStatusTip('Zoom')
        layout.addWidget(slider, 0, 3)
        
        # SET LAYOUT AND SET AS CENTER
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Actions
        exitAction = QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
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

        # Begin QTimer Poll and Read ADS
        timer = QTimer(self)

        timer.timeout.connect(plot.nextAnimationFrame)
        timer.start(10)
        
        self.showFullScreen()
        self.setWindowTitle('RF Tracker')
        self.show()

    def createLabel(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setMargin(2)
        label.setFrameStyle(QFrame.Box | QFrame.Sunken)
        label.setMinimumSize(self.sizeHint())
        return label

if __name__ == '__main__':
    # initialize global variables
    globals.init()

    # start application
    app = QApplication(sys.argv)
    login = Login()
    if login.exec_() == QDialog.Accepted:
        ex = RFTracker()

        # ADC Read Thread
        threadADC = ADCThread()
        threadADC.finished.connect(app.exit)
        threadADC.start()

        # Filter Thread
        threadFilter = FilterThread()
        threadFilter.finished.connect(app.exit)
        threadFilter.start()

        sys.exit(app.exec_())
