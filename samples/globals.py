from PyQt5.QtCore import QMutex
from enum import Enum


class Sector(Enum):
    A = 0
    B = 1
    C = 2


def init():
    global amplitudeA
    amplitudeA = 0
    global amplitudeB
    amplitudeB = 0
    global amplitudeC
    amplitudeC = 0
    global distance
    distance = 0
    global mutex
    mutex = QMutex()
    global global_x
    global_x = 0
    global global_y
    global_y = 0
