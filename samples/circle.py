from PyQt5.QtCore import QRectF, QSize
from PyQt5.QtGui import QColor, QPainter, QPalette, QPen
from PyQt5.QtWidgets import QSizePolicy, QWidget

from time import sleep

class CircleWidget(QWidget):
    def __init__(self, parent=None):
        super(CircleWidget, self).__init__(parent)
        
        self.floatBased = False
        self.antialiased = False
        self.setup = False
        self.frameNo = 0
        
        self.setBackgroundRole(QPalette.Base)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.update()

    def setFloatBased(self, floatBased):
        self.floatBased = floatBased
        self.update()
    
    def setAntialiased(self, antialiased):
        self.antialiased = antialiased
        self.update()
    
    def minimumSizeHint(self):
        return QSize(50, 50)
    
    def sizeHint(self):
        return QSize(180, 180)
    
    def nextAnimationFrame(self):
        self.frameNo += 1
        self.update()
    
    def paintEvent(self, event):
        # sample
        size = self.size()
        
        color = QColor(0, 0, 0)
        color.setNamedColor('#4080fe')
        
        painter = QPainter(self)
        painter.setPen(color)
        painter.setRenderHint(QPainter.Antialiasing, self.antialiased)
        painter.translate(self.width() / 2, self.height() / 2)
        
        for diameter in range(0, 360, 30):
            
            delta = abs((40 % 128) - diameter / 2)
            alpha = 255 - (delta * delta) / 4 - diameter
            painter.drawEllipse(QRectF(-diameter / 2.0, -diameter / 2.0, diameter, diameter))


        for l in range(0,360,1)
            painter.drawPoint(l,l)


        #painter.drawEllipse(QRectF(-100 / 2.0, -100 / 2.0, 100, 100))
        #painter.drawPoint(-size.width()/2,-size.height()/2)
        #updatePoint()
            

    def updatePoint(self, amplitudein, phasein):
        self.amplitude = amplitudein
        self.phase = phasein
        self.update_point = True
        self.update()
