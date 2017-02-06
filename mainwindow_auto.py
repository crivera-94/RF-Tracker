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
        MainWindow.showMaximized()
        # MainWindow.resize(480, 320)
        
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.btnOn = QtWidgets.QPushButton(self.centralWidget)
        # QRect(left, top, width, height)
        self.btnOn.setGeometry(QtCore.QRect(60, 90, 90, 45))
        self.btnOn.setObjectName("btnOn")
        self.btnOff = QtWidgets.QPushButton(self.centralWidget)
        self.btnOff.setGeometry(QtCore.QRect(220, 90, 90, 45))
        self.btnOff.setObjectName("btnOff")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(140, 50, 90, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        
        
        # ONLY FOR DEMO#################################################
        self.testlabel1 = QtWidgets.QLabel(self.centralWidget)
        self.testlabel1.setGeometry(QtCore.QRect(300, 200, 90, 20))
        self.testlabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.testlabel1.setObjectName("testlabel1")
        self.testlabel2 = QtWidgets.QLabel(self.centralWidget)
        self.testlabel2.setGeometry(QtCore.QRect(400, 200, 90, 20))
        self.testlabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.testlabel2.setObjectName("testlabel2")
        self.testlabel3 = QtWidgets.QLabel(self.centralWidget)
        self.testlabel3.setGeometry(QtCore.QRect(500, 200, 90, 20))
        self.testlabel3.setAlignment(QtCore.Qt.AlignCenter)
        self.testlabel3.setObjectName("testlabel3")
        
        
        MainWindow.setCentralWidget(self.centralWidget)
        
        # Menu Bar
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 480, 22))
        self.menuBar.setObjectName("menuBar")

        # Menu Bar Options
        file = self.menuBar.addMenu('&File')
        edit = self.menuBar.addMenu('&Edit')
        
        # File Options
        exit_action = file.addAction('Exit')
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)


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
        self.btnOn.setText(_translate("MainWindow", "Down"))
        self.btnOff.setText(_translate("MainWindow", "Up"))
        self.label.setText(_translate("MainWindow", "Scaling"))




        # ONLY FOR DEMO#################################################
        self.testlabel1.setText(_translate("MainWindow", "Inner Radius\n10"))
        self.testlabel2.setText(_translate("MainWindow", "Middle Radius\n10"))
        self.testlabel3.setText(_translate("MainWindow", "Outer Radius\n10"))


