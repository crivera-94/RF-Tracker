#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    ZetCode PyQt5 tutorial
    
    In this example, we connect a signal
    of a QSlider to a slot of a QLCDNumber.
    
    author: Jan Bodnar
    website: zetcode.com
    last edited: January 2015
    """

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, QLabel,
                             QVBoxLayout, QGridLayout, QApplication)


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    
    def initUI(self):
        
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Vertical, self)
        label = self.createLabel(text = "Zoom")
        
        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(lcd, 1, 0 )
        layout.addWidget(sld, 1, 1)
        
        self.setLayout(layout)
        sld.valueChanged.connect(lcd.display)
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal & slot')
        self.show()

    def createLabel(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setMargin(2)
        label.setFrameStyle(QFrame.Box | QFrame.Sunken)
        return label


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())