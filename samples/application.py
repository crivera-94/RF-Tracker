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

from PyQt5.QtCore import Qt, QTimer, QThread
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction,
                             QApplication, QGridLayout, QWidget,
                             QLabel, QFrame, QSlider)
from PyQt5.QtGui import QIcon
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


def update_amplitude(phase_detector0, phase_detector1, filter):
    filter.update(phase_detector0.read_amplitude(), phase_detector1.read_amplitude(), phase_detector1.read_third_value())


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

        # Begin QTimer Poll and Read ADS
        timer = QTimer(self)

        x = 0
        y = 0

        timer.timeout.connect(plot.nextAnimationFrame)
        
        timer.start(20)
        
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
    # phase_detector0 setup
    # A0 = phase
    # A1 = amplitude
    # A2 = phase (outer)
    phase_detector0 = PhaseDetector(48)

    # phase_detector1 setup
    # A0 = phase
    # A1 = amplitude
    # A2 = amplitude (outer)
    phase_detector1 = PhaseDetector(52)

    # start application
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
