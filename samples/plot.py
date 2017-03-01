from PyQt5.QtCore import QRectF, QSize
from PyQt5.QtGui import QColor, QPainter, QPalette, QPen
from PyQt5.QtWidgets import QSizePolicy, QWidget

from time import sleep

class Plot(QWidget):
    def __init__(self, parent=None):
        super(Plot, self).__init__(parent)
        
        self.floatBased = False
        self.antialiased = False
        self.setup = False
        self.frameNo = 0
        
        self.setBackgroundRole(QPalette.Base)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.paintEvent = self.setup_plot
        self.update()
        self.paintEvent = self.draw_point

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

    def setup_plot(self, event):
        alpha = .1
        color = QColor(0, 0, 0, alpha)
        color.setNamedColor('#4080fe')
            
        painter = QPainter(self)
        painter.setPen(color)
        painter.setRenderHint(QPainter.Antialiasing, self.antialiased)
        painter.translate(self.width() / 2, self.height() / 2)
            
        for diameter in range(0, 390, 30):    
            delta = abs((40 % 128) - diameter / 2)
            alpha = 255 - (delta * delta) / 4 - diameter
            painter.drawEllipse(QRectF(-diameter / 2.0, -diameter / 2.0, diameter, diameter))

        for l in range(0,180,1):
            painter.drawPoint(0,-l)

        i = 0
        step_x = .8660254
        step_y = .5

        # 180 is a fixed bound
        for i in range(0,180,1):
            painter.drawPoint(i * step_x, i * step_y)
            painter.drawPoint(-i * step_x, i * step_y)

    def draw_point(self, event):
        alpha = .1
        color = QColor(0, 0, 0, alpha)
        color.setNamedColor('#4080fe')
            
        painter = QPainter(self)
        painter.setPen(color)
        painter.setRenderHint(QPainter.Antialiasing, self.antialiased)
        painter.translate(self.width() / 2, self.height() / 2)
            
        for diameter in range(0, 390, 30):    
            delta = abs((40 % 128) - diameter / 2)
            alpha = 255 - (delta * delta) / 4 - diameter
            painter.drawEllipse(QRectF(-diameter / 2.0, -diameter / 2.0, diameter, diameter))


        # draw lines
        for l in range(0,180,1):
            painter.drawPoint(0,-l)

        i = 0
        step_x = .8660254
        step_y = .5

        # 180 is a fixed bound
        for i in range(0,180,1):
            painter.drawPoint(i * step_x, i * step_y)
            painter.drawPoint(-i * step_x, i * step_y)

        x = 90
        y = 90

        for i in range(0,5,1):
            painter.drawPoint(x+i,y)
            painter.drawPoint(x-i,y)
            painter.drawPoint(x,y+i)
            painter.drawPoint(x,y-i)



