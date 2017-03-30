import time
from PyQt5.QtCore import QThread, QMutex
from phasedetector import PhaseDetector
from pykalman import KalmanFilter
from math import sqrt, pow
from enum import Enum


class Sector(Enum):
    A = 0
    B = 1
    C = 2

# sector A - top left
amplitudeA = 10
phaseA = 0

# sector B - top right
amplitudeB = 0
phaseB = 0

# sector C - bottom
amplitudeC = 0
phaseC = 0

# create mutual exclusion
mutex = QMutex()

# resultant location
resultant_angle = 0
resultant_sector = Sector.A


class ADCThread(QThread):

    def __init__(self):
        QThread.__init__(self)

        # phase_detector0 setup
        # A0 = phase
        # A1 = amplitude
        # A2 = phase (outer)
        self.phase_detector0 = PhaseDetector(48)

        # phase_detector1 setup
        # A0 = phase
        # A1 = amplitude
        # A2 = amplitude (outer)
        self.phase_detector1 = PhaseDetector(52)
        self.sample_size = 10

    def run(self):
        while True:
            mutex.lock()
            for i in range(0, self.sample_size):
                # set amplitude_temp equal to self.phase_detector0.read_amplitude()
                amplitude_temp0 = 10
            global amplitudeA
            amplitudeA = amplitude_temp0 / self.sample_size
            mutex.unlock()

            time.sleep(0.5)
            print("ADCThread -> Amplitude0: {}".format(amplitudeA))
            # TODO: OSError: [Errno 5] Input/output error
            # print('Channel 0: {}'.format(self.phase_detector0.read_amplitude()))


class FilterThread(QThread):

    def sectorA(self):
        voltage = (amplitudeA * self.max_voltage) / self.resolution
        angle = self.quadratic(voltage)
        print("amplitudeA Increasing")

    def sectorB(self):
        voltage = (amplitudeB * self.max_voltage) / self.resolution
        angle = self.quadratic(voltage)

    def sectorC(self):
        voltage = (amplitudeC * self.max_voltage) / self.resolution
        angle = self.quadratic(voltage)

    def quadratic(self, y):
        root = pow(self.b, 2) + (4 * self.a * (y - self.c))
        num = -self.b + root
        den = 2 * self.a
        if num > 0:
            return num/den
        else:
            return -num/den

    def __init__(self):
        QThread.__init__(self)
        self.kf = KalmanFilter(initial_state_mean=0, n_dim_obs=2)
        self.x = 0
        self.y = 0
        self.a = -0.00001729241
        self.b = -0.00001729241
        self.c = 1.21484747253
        self.max_voltage = 2.048
        self.resolution = 2048
        self.options = {
            Sector.A: self.sectorA,
            Sector.B: self.sectorB,
            Sector.C: self.sectorC
        }

    def get_sector(self):
        if amplitudeA > amplitudeB:
            if amplitudeA > amplitudeC:
                return Sector.A
            else:
                return Sector.C
        else:
            if amplitudeB > amplitudeC:
                return Sector.B
            else:
                return Sector.C

    def run(self):
        while True:
            sector = self.get_sector()
            self.options[sector]()

            # mutex.lock()
            time.sleep(0.5)
            print("FilterThread Increasing")
            # mutex.unlock()