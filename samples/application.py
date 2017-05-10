#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import phasedetector
import globals
import re
import socket

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
from threadpackage import DatabaseThread
import pyrebase

REMOTE_SERVER = "www.google.com"


# http://stackoverflow.com/questions/11812000/login-dialog-pyqt
class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textEmail = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handle_login)
        username_label = QLabel("Email:")
        password_label = QLabel("Password:")
        layout = QGridLayout(self)
        layout.addWidget(username_label, 0, 0)
        layout.addWidget(password_label, 1, 0)
        layout.addWidget(self.textEmail, 0, 1)
        layout.addWidget(self.textPass, 1, 1)
        layout.addWidget(self.buttonLogin, 2, 1)
        self.setWindowTitle('RF Tracker')
        self.auth = globals.firebase.auth()
        self.EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    def handle_login(self):
        if self.EMAIL_REGEX.match(self.textEmail.text()):
            user = self.auth.sign_in_with_email_and_password(self.textEmail.text(), self.textPass.text())
            try:
                if user['idToken']:
                    globals.user_token = user['idToken']
                    self.accept()
                else:
                    QMessageBox.warning(self, 'Error', 'Bad user or password!')
            except KeyError:
                QMessageBox.warning(self, 'Error', 'Bad user or password!')
        else:
            QMessageBox.warning(self, 'Error', 'Not a valid email address!')


class Settings(QDialog):
    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)
        self.line_color_text_field = QLineEdit(self)
        self.point_color_text_field = QLineEdit(self)
        self.buttonLogin = QPushButton('Accept', self)
        self.buttonLogin.clicked.connect(self.update_values)
        line_label = QLabel("Plot Color")
        point_label = QLabel("Point Color")
        layout = QGridLayout(self)

        layout.addWidget(line_label, 0, 0)
        layout.addWidget(point_label, 1, 0)
        layout.addWidget(self.line_color_text_field, 0, 1)
        layout.addWidget(self.point_color_text_field, 1, 1)
        layout.addWidget(self.buttonLogin, 2, 1)

        self.setWindowTitle('Settings')
        self.pattern = re.compile("#[0-9|A-F|a-f]"
                                  "[0-9|A-F|a-f]"
                                  "[0-9|A-F|a-f]"
                                  "[0-9|A-F|a-f]"
                                  "[0-9|A-F|a-f]"
                                  "[0-9|A-F|a-f]")

    def populate_text_fields(self, plot_line_color, plot_point_color):
        self.line_color_text_field.setText(plot_line_color)
        self.point_color_text_field.setText(plot_point_color)

    def update_values(self):
        if self.pattern.match(self.line_color_text_field.text()) and \
                self.pattern.match(self.point_color_text_field.text()):
            self.line = self.line_color_text_field.text()
            self.point = self.point_color_text_field.text()
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid Values')


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
        settings.populate_text_fields(self.plot.line_color, self.plot.point_color)
        settings.exec_()
        self.plot.change_colors(settings.line, settings.point)

    def resume_tracking(self):
        self.plot.continue_tracking()

    def pause_tracking(self):
        self.plot.pause_tracking()

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
        # fromRow, fromColumn, rowSpan, columnSpan
        self.home_widget = QWidget()
        layout = QGridLayout()
        self.home_widget.setLayout(layout)

        label = self.create_label(text="Distance")
        label2 = self.create_label(text="Sector A")
        label3 = self.create_label(text="Angle")
        layout.addWidget(label3, 1, 1)
        layout.addWidget(label2, 0, 0, 2, 1)
        layout.addWidget(label, 0, 1)

        # Make Plot
        self.plot = Plot()
        layout.addWidget(self.plot, 0, 2, 2, 1)
        # slider = QSlider(Qt.Vertical, self)
        # slider.setStatusTip('Zoom')
        # layout.addWidget(slider, 0, 3)

    def create_label(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setMargin(2)
        label.setFrameStyle(QFrame.Box | QFrame.Sunken)
        label.setMinimumSize(self.sizeHint())
        return label


def is_connected():
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(REMOTE_SERVER)
        # connect to the host -- tells us if the host is reachable
        temp = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


def setup_firebase():
    config = {
        "apiKey": "AIzaSyCobF9FiE7NMo6RUISeEcTWQb9qmL2MukU",
        "authDomain": "rf-tracker.firebaseapp.com",
        "databaseURL": "https://rf-tracker.firebaseio.com",
        "storageBucket": "rf-tracker.appspot.com",
    }
    firebase = pyrebase.initialize_app(config)
    return firebase

if __name__ == '__main__':
    # initialize global variables
    globals.init()

    if is_connected():
        # setup firebase
        globals.firebase = setup_firebase()
        globals.database = globals.firebase.database()

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

            # Database Thread
            databaseThread = DatabaseThread(login.textEmail.text())
            databaseThread.finished.connect(app.exit)
            databaseThread.start()

            sys.exit(app.exec_())
    else:
        app = QApplication(sys.argv)
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
