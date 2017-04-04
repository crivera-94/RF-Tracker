import time
from PyQt5.QtCore import QThread, QMutex
from phasedetector import PhaseDetector
from pykalman import KalmanFilter
from math import sqrt, pow, sin, cos, pi, radians
from enum import Enum
import globals
import Adafruit_ADS1x15


class Sector(Enum):
    A = 0
    B = 1
    C = 2

# sector A - top left
amplitudeA = 10

# sector B - top right
amplitudeB = 0

# sector C - bottom
amplitudeC = 0

# distance
distance = 0

# create mutual exclusion
mutex = QMutex()


class ADCThread(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.sample_size = 10
        # phase_detector0 setup
        # A0 = phase
        # A1 = amplitude
        # A2 = phase (outer)
        self.phase_detector0 = PhaseDetector(0x48)

        # phase_detector1 setup
        # A0 = phase
        # A1 = amplitude
        # A2 = amplitude (outer)
        self.phase_detector1 = PhaseDetector(0x52)

    def run(self):
        while True:
            mutex.lock()
            amplitude_temp0 = 0
            for i in range(0, self.sample_size):
                # set amplitude_temp equal to self.phase_detector0.read_amplitude()
                amplitude_temp0 = amplitude_temp0 + self.phase_detector0.read_amplitude()
            #global amplitudeA
            #amplitudeA = amplitude_temp0 / self.sample_size
            globals.amplitudeA = amplitude_temp0 / self.sample_size

            # globals.amplitudeA = (globals.amplitudeA + 0.05) % 2

            mutex.unlock()

            time.sleep(0.001)
            print("ADCThread -> Amplitude0: {}".format(amplitudeA))
            print("ADCThread -> Global: {}".format(globals.amplitudeA))

            # TODO: OSError: [Errno 5] Input/output error
            print('Channel 0: {}'.format(self.phase_detector0.read_amplitude()))
            print('Channel 1: {}'.format(self.phase_detector0.read_phase()))


class FilterThread(QThread):

    def polar_to_cartesian(self, rho, phi):
        x = rho * cos(phi)
        y = rho * sin(phi)
        return x, y

    def quadratic(self, y):
        root = pow(self.b, 2) + (4 * self.a * (y - self.c))
        num = -self.b + root
        den = 2 * self.a
        if num > 0:
            return num/den
        else:
            return -num/den

    def update_globals(self, amplitude_reading, rho, reference_angle):
        voltage = (amplitude_reading * self.max_voltage) / self.resolution
        phi = reference_angle - self.quadratic(voltage)
        coordinates = self.polar_to_cartesian(rho, phi)

        globals.global_x = coordinates[0]
        globals.global_y = coordinates[1]

    def sectorA(self):
        # distance can be a max of 180, defined by plot size
        distance = 90
        print("Global: {}".format(globals.amplitudeA))
        self.update_globals(globals.amplitudeA, distance, 210)

    def sectorB(self):
        self.update_globals(globals.amplitudeB, distance, 90)

    def sectorC(self):
        self.update_globals(globals.amplitudeC, distance, -30)

    def __init__(self):
        QThread.__init__(self)
        self.kf = KalmanFilter(initial_state_mean=0, n_dim_obs=2)
        self.x = 0
        self.y = 0
        self.a = -0.00001729241
        self.b = -0.00437652647
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
            time.sleep(0.001)
            print("FilterThread Increasing")
            # mutex.unlock()