import time
from PyQt5.QtCore import QThread, QMutex
from phasedetector import PhaseDetector
from pykalman import KalmanFilter
from math import sqrt, pow, sin, cos, pi, radians
from enum import Enum
import globals


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
# distance = 0

# create mutual exclusion
# mutex = QMutex()


class ADCThread(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.sample_size = 10
        # addr = empty -> 0x48
        # addr = sda -> 0x4a
        # addr = scl -> 0x4b

        # phase_detector0 setup
        # A0 = amplitude
        # A2 = distance
        self.phase_detector0 = PhaseDetector(0x48)

        # phase_detector1 setup
        # A0 = amplitude
        self.phase_detector1 = PhaseDetector(0x4a)

        # additional phase detector
        self.phase_detector2 = PhaseDetector(0x4b)
        self.kf = KalmanFilter(initial_state_mean=0, n_dim_obs=2)

    def run(self):
        while True:
            globals.mutex.lock()

            # update previous globals
            globals.pAmplitudeA = globals.amplitudeA
            globals.pAmplitudeB = globals.amplitudeB
            globals.pAmplitudeC = globals.amplitudeC
            globals.prev_state_means = globals.curr_state_means
            globals.prev_covariances = globals.curr_covariances

            amplitude_a = 0
            amplitude_b = 0
            amplitude_c = 0
            distance = 0

            for i in range(0, self.sample_size):
                # set amplitude buffers using readings from phase detectors
                amplitude_a = amplitude_a + self.phase_detector0.read_channel_zero()
                amplitude_b = amplitude_b + self.phase_detector0.read_channel_three()
                # amplitude_c = amplitude_c + self.phase_detector0.read_channel_zero()
                distance = distance + self.phase_detector0.read_channel_two()

            # from plot_online.py
            #globals.curr_state_means, globals.curr_covariances = (
            #    self.kf.filter_update(
            #        globals.prev_state_means,
            #        globals.prev_covariances,
            #        globals.observation
            #    )
            #)

            # TODO: Remove -1, only used for testing in sector A
            globals.amplitudeA = amplitude_a / self.sample_size
            globals.amplitudeB = amplitude_b / self.sample_size
            globals.amplitudeC = amplitude_c / self.sample_size - 1
            globals.distance = distance / self.sample_size

            globals.mutex.unlock()

            print('Channel 0: {}'.format(self.phase_detector0.read_channel_zero()))
            print('Channel 2: {}'.format(self.phase_detector0.read_channel_two()))
            time.sleep(0.00001)


class FilterThread(QThread):
    @staticmethod
    def polar_to_cartesian(rho, phi):
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
        self.update_globals(globals.amplitudeA, globals.distance, 210)

    def sectorB(self):
        self.update_globals(globals.amplitudeB, globals.distance, 90)

    def sectorC(self):
        self.update_globals(globals.amplitudeC, globals.distance, -30)

    def __init__(self):
        QThread.__init__(self)
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

    @staticmethod
    def get_sector():
        if globals.amplitudeA > globals.amplitudeB:
            if globals.amplitudeA > globals.amplitudeC:
                return Sector.A
            else:
                return Sector.C
        else:
            if globals.amplitudeB > globals.amplitudeC:
                return Sector.B
            else:
                return Sector.C

    def run(self):
        while True:
            sector = self.get_sector()
            self.options[sector]()
            # mutex.lock()
            time.sleep(0.00001)
            # mutex.unlock()
