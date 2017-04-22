#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import phasedetector
import globals

from PyQt5.QtCore import Qt, QTimer, QThread
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction,
                             QApplication, QGridLayout, QWidget,
                             QLabel, QFrame, QSlider,
                             QDialog, QLineEdit, QPushButton, QVBoxLayout, QMessageBox,
                             QStackedLayout)
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


class Settings(QDialog):
    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)
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
        self.setWindowTitle('Settings')

    def handle_login(self):
        if self.textName.text() == 'foo' and self.textPass.text() == 'bar':
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Bad user or password')


class RFTracker(QMainWindow):
    def __init__(self):
        self.current_page = 0
        self.MAX_ACCURATE_RANGE = 2047
        self.MIN_ACCURATE_RANGE = 50
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        self.create_home_widget()
        self.create_menubars()

        # Begin QTimer Poll and Read ADS
        timer = QTimer(self)
        timer.timeout.connect(self.plot.nextAnimationFrame)
        timer.start(10)

        # TODO: test lines
        test_layout = QStackedLayout()
        test_layout.addWidget(self.home_widget)
        # test_layout.setCurrentIndex(0)

        self.central_widget = QWidget()
        self.central_widget.setLayout(test_layout)
        self.setCentralWidget(self.central_widget)
        
        self.showFullScreen()
        self.setWindowTitle('RF Tracker')
        self.show()

    def settings(self):
        settings = Settings()
        settings.exec_()

    def resume_tracking(self):
        self.plot.continue_tracking()
        print("df")

    def pause_tracking(self):
        self.plot.pause_tracking()
        print("df")

    def refresh_grid(self):
        self.plot.refresh()

    def create_menubars(self):
        # Actions
        exit_action = QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit Application')
        exit_action.triggered.connect(self.close)

        refresh_action = QAction(QtGui.QIcon('icons/refresh.png'), 'Refresh Grid', self)
        refresh_action.setShortcut('Ctrl+R')
        refresh_action.setStatusTip('Refresh Grid')
        refresh_action.triggered.connect(self.refresh_grid)

        settings_action = QAction(QtGui.QIcon('icons/adjustSettings.png'), 'Settings', self)
        settings_action.setShortcut('Ctrl+S')
        settings_action.setStatusTip('Adjust Settings')
        settings_action.triggered.connect(self.settings)

        play_action = QAction(QtGui.QIcon('icons/play.png'), 'Start Tracking', self)
        play_action.setShortcut('Ctrl+P')
        play_action.setStatusTip('Continue Tracking')
        play_action.triggered.connect(self.resume_tracking)

        pause_action = QAction(QtGui.QIcon('icons/pause.png'), 'Pause Tracking', self)
        pause_action.setShortcut('Ctrl+O')
        pause_action.setStatusTip('Pause Tracking')
        pause_action.triggered.connect(self.pause_tracking)

        # Status Bar
        self.statusBar().showMessage('Ready')

        # Menu Bar
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(exit_action)

        # Grid Menu and actions
        grid_menu = menubar.addMenu('&Grid')
        grid_menu.addAction(play_action)
        grid_menu.addAction(pause_action)

        # Edit Menu
        edit_menu = menubar.addMenu('&Edit')
        edit_menu.addAction(refresh_action)
        edit_menu.addAction(settings_action)

        # Tool Bar
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit_action)
        toolbar.addAction(refresh_action)
        toolbar.addAction(settings_action)
        toolbar.addAction(pause_action)
        toolbar.addAction(play_action)

    def create_home_widget(self):
        self.home_widget = QWidget()
        layout = QGridLayout()
        self.home_widget.setLayout(layout)

        label = self.create_label(text="Distance")
        label2 = self.create_label(text="Sector A")
        layout.addWidget(label2, 0, 0)
        layout.addWidget(label, 0, 1)

        # Make Plot
        self.plot = Plot()
        layout.addWidget(self.plot, 0, 2)
        slider = QSlider(Qt.Vertical, self)
        slider.setStatusTip('Zoom')
        layout.addWidget(slider, 0, 3)

    def create_label(self, text):
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
