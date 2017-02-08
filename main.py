# From https://www.baldengineer.com/raspberry-pi-gui-tutorial.html
# by James Lewis (@baldengineer)
# Minimal python code to start PyQt5 GUI
#

# always seem to need this
import sys

# This gets the Qt stuff
import PyQt5

from PyQt5 import QtCore

from PyQt5.QtWidgets import *

# This is our window from QtCreator
import mainwindow_auto
#import concentriccircles.py

# create class for our Raspberry Pi GUI
class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    # access variables inside of the UI's file

    ### functions for the buttons to call
    def pressedOnButton(self):
        self.fade()
        print ("Scaling up!")


    def pressedOffButton(self):
        print ("Scaling down!")
    

    def __init__(self):
        self.auto_scale = True
        super(self.__class__, self).__init__()
        self.setupUi(self) # gets defined in the UI file


        layout = QGridLayout()
        layout.addWidget(self.btnOn, 0, 1)
        layout.addWidget(self.btnOff, 1, 0)
        layout.addWidget(self.label, 1, 1)
        layout.addWidget(asf, 2, 2)


        ### Hooks to for buttons
        self.btnOn.clicked.connect(lambda: self.pressedOnButton())
        self.btnOff.clicked.connect(lambda: self.pressedOffButton())

        # core application (e.g. main menu) inside
        
        
        
        # main menu code
        #extractAction = QAction("&Quit",self)
        #extractAction.setShortcut("Ctrl+Q")
        #extractAction.setStatusTip('Leave The App')
        #extractAction.triggered.connect(self.close_application)
    
        # only need once
        # self.statusBar()
        
        #mainMenu = self.menuBar()
        #fileMenu = mainMenu.addMenu('&File')
        #fileMenu.addAction(extractAction)
        

    # make functions that are specific to page
    def fade(self):
        self.btnOn.setWindowOpacity(0.5)
        QtCore.QTimer.singleShot(1000, self.unfade)


    def unfade(self):
        self.btnOn.setWindowOpacity(1)


    def close_application(self):
        self.close()


    def toggle_autoscale_state(self):
        if self.auto_scale == True:
            self.auto_scale = False
        else:
            self.auto_scale = True

# I feel better having one of these
def main():
    # a new app instance
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    # without this, the script exits immediately.
    sys.exit(app.exec_())

# python bit to figure how who started This
if __name__ == "__main__":
    main()