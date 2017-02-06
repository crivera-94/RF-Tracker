# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        
        # For Final Version
        # MainWindow.showFullScreen()
        MainWindow.resize(480, 320)
        
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.btnOn = QtWidgets.QPushButton(self.centralWidget)
        self.btnOn.setGeometry(QtCore.QRect(100, 90, 113, 91))
        self.btnOn.setObjectName("btnOn")
        self.btnOff = QtWidgets.QPushButton(self.centralWidget)
        self.btnOff.setGeometry(QtCore.QRect(280, 90, 113, 91))
        self.btnOff.setObjectName("btnOff")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(110, 60, 271, 16))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralWidget)
        
        # Menu Bar
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 480, 22))
        self.menuBar.setObjectName("menuBar")

        # "File" option
        #file = self.menuBar.addMenu('&File')
        #action = file.addAction('Exit Application')
        #action.triggered.connect(self.close)

        # Open
        openAction = QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a file')
        openAction.triggered.connect(self.close)
        
        # Close
        closeAction = QAction('Close', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Notepad')
        closeAction.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(closeAction)


        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        
        # Status Bar
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        
        MainWindow.setStatusBar(self.statusBar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RF Tracker"))
        
        # setting attribute values
        self.btnOn.setText(_translate("MainWindow", "On"))
        self.btnOff.setText(_translate("MainWindow", "Off"))
        self.label.setText(_translate("MainWindow", "Sample GUI"))

