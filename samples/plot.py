from PyQt5.QtCore import QRectF, QSize
from PyQt5.QtGui import QColor, QPainter, QPalette, QPen
from PyQt5.QtWidgets import QSizePolicy, QWidget

from time import sleep

class Plot(QWidget):
    def __init__(self, parent=None):
        super(Plot, self).__init__(parent)
        
        self.floatBased = False
        self.antialiased = False
        self.frameNo = 0
        
        self.setBackgroundRole(QPalette.Base)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.alpha = 0
        self.radius = 30
        self.rings_plotted = False
        self.setup_finished = False
        self.paintEvent = self.draw_rings
        #self.update()
        #self.paintEvent = self.draw_point

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
        if self.rings_plotted == True:
            # read data and plot
            if self.alpha >= 240:
                self.alpha = 255
                self.update()
                self.paintEvent = self.draw_point
            else:
                self.alpha += 20
                self.update()
            
        else:
            if self.radius > 390 :
                self.paintEvent = self.draw_lines
                self.rings_plotted = True
                self.alpha = 0
                self.update()
            else:
                self.alpha = (self.alpha + 20) % 260
                if self.alpha == 0:
                    self.radius += 30
                self.update()


    def setup_plot(self, event):
        color = QColor(0, 0, 0)
        color.setNamedColor('#4080fe')
        color.setAlpha(self.alpha)
        
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


    # draw rings new
    def draw_rings(self, event):
        color_solid = QColor(0, 0, 0)
        color_solid.setNamedColor('#4080fe')

        color_light = QColor(0, 0, 0)
        color_light.setNamedColor('#4080fe')
        color_light.setAlpha(self.alpha)

        painter = QPainter(self)
        painter.setPen(color_light)
        painter.setRenderHint(QPainter.Antialiasing, self.antialiased)
        painter.translate(self.width() / 2, self.height() / 2)
        
        # max should be relative, fixed at 390 right now
        #for diameter in range(0, self.radius, 30):
        for diameter in range(0, 390, 30):
            
            if diameter <= self.radius:
                # draw whole
                painter.setPen(color_solid)

                delta = abs((40 % 128) - diameter / 2)
                alpha = 255 - (delta * delta) / 4 - diameter
                painter.drawEllipse(QRectF(-diameter / 2.0, -diameter / 2.0, diameter, diameter))
            else:
                painter.setPen(color_light)

                delta = abs((40 % 128) - diameter / 2)
                alpha = 255 - (delta * delta) / 4 - diameter
                painter.drawEllipse(QRectF(-diameter / 2.0, -diameter / 2.0, diameter, diameter))
                break


    def draw_lines(self, event):
        
        
        color = QColor(0, 0, 0)
        color.setNamedColor('#4080fe')
        
        painter = QPainter(self)
        painter.setPen(color)
        painter.setRenderHint(QPainter.Antialiasing, self.antialiased)
        painter.translate(self.width() / 2, self.height() / 2)
        
        for diameter in range(0, 390, 30):
            delta = abs((40 % 128) - diameter / 2)
            alpha = 255 - (delta * delta) / 4 - diameter
            painter.drawEllipse(QRectF(-diameter / 2.0, -diameter / 2.0, diameter, diameter))
    
    
        color.setAlpha(self.alpha)
        painter_light = QPainter(self)
        painter_light.setPen(color)
        painter_light.setRenderHint(QPainter.Antialiasing, self.antialiased)
        painter_light.translate(self.width() / 2, self.height() / 2)
    
        for l in range(0,180,1):
            painter_light.drawPoint(0,-l)
        
        i = 0
        step_x = .8660254
        step_y = .5
        
        # 180 is a fixed bound
        for i in range(0,180,1):
            painter_light.drawPoint(i * step_x, i * step_y)
            painter_light.drawPoint(-i * step_x, i * step_y)


    def draw_point(self, event):
        color = QColor(0, 0, 0)
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



