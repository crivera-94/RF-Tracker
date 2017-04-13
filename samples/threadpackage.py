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
            amplitude_c = 11.1
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
            #        globals.prev_covariances#,
            #        globals.observation
            #    )
            #)

            # TODO: Remove -1, only used for testing in sector A
            globals.amplitudeA = amplitude_a / self.sample_size
            globals.amplitudeB = amplitude_b / self.sample_size
            globals.amplitudeC = amplitude_c / self.sample_size
            globals.distance = distance / self.sample_size

            globals.mutex.unlock()

            # print('Channel 0: {}'.format(self.phase_detector0.read_channel_zero()))
            # print('Channel 2: {}'.format(self.phase_detector0.read_channel_two()))
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

        if num < 0:
            num = -self.b - root
            return num/den
        else:
            return num/den
        # root = ((y-self.c)/self.a) + (pow(self.b, 2)/(4*pow(self.a, 2)))
        # result = -(self.b/(2 * self.a)) + sqrt(root)
        # return result

    def update_globals(self, amplitude_reading, rho, reference_angle):
        voltage = (amplitude_reading * self.max_voltage) / self.resolution
        phi = reference_angle - self.quadratic(voltage)
        coordinates = self.polar_to_cartesian(rho, phi)

        if self.min_valid_voltage < voltage < self.max_valid_voltage:
            globals.global_x = coordinates[0]
            globals.global_y = coordinates[1]
        else:
            globals.global_x = 0
            globals.global_y = 220

    def sectorA(self):
        # distance can be a max of 180, defined by plot size
        # globals.distance = 90
        # self.update_globals(globals.amplitudeA, globals.distance, 210)
        # self.update_globals(globals.amplitudeA, globals.distance, -150)
        self.update_globals(globals.amplitudeA, globals.distance, self.reference_angle_a)

    def sectorB(self):
        self.update_globals(globals.amplitudeB, globals.distance, self.reference_angle_b)

    def sectorC(self):
        self.update_globals(globals.amplitudeC, globals.distance, self.reference_angle_c)

    def __init__(self):
        QThread.__init__(self)
        self.x = 0
        self.y = 0

        # original
        self.a = -0.00001729241
        self.b = -0.00437652647
        self.c = 1.21484747253

        # fake
        # self.a = 0.00000004311
        # self.b = -0.00560240357
        # self.c = 1.22201299145

        self.reference_angle_a = 100
        self.reference_angle_b = 90
        self.reference_angle_c = -30

        self.max_voltage = 2.048
        self.resolution = 2048
        self.max_valid_voltage = 1.38
        self.min_valid_voltage = 0.38

        self.sector = Sector.A

        self.options = {
            Sector.A: self.sectorA,
            Sector.B: self.sectorB,
            Sector.C: self.sectorC
        }

    def at_edge(self):
        # Tuple returned
        # return[0] = edge status
        # return[1] =   True -> high edge
        #               False -> low edge
        if self.sector == Sector.A:
            if globals.amplitudeA < self.min_valid_voltage:
                return True, False
            elif globals.amplitudeA > self.max_valid_voltage:
                return True, True
            else:
                return False
        elif self.sector == Sector.B:
            if globals.amplitudeB < self.min_valid_voltage:
                return True, False
            elif globals.amplitudeB > self.max_valid_voltage:
                return True, True
            else:
                return False
        elif self.sector == Sector.C:
            if globals.amplitudeC < self.min_valid_voltage:
                return True, False
            elif globals.amplitudeC > self.max_valid_voltage:
                return True, True
            else:
                return False, False

    def get_neighbor(self, edge):
        # edge =    True -> high
        #           False -> low
        if self.sector == Sector.A:
            if edge:
                return Sector.C
            else:
                return Sector.B
        elif self.sector == Sector.B:
            if edge:
                return Sector.A
            else:
                return Sector.C
        elif self.sector == Sector.C:
            if edge:
                return Sector.B
            else:
                return Sector.A

    def get_sector(self):
        status = self.at_edge()
        if not status[0]:
            # not at edge
            return self.sector
        else:
            self.sector = self.get_neighbor(status[1])
            return self.sector

        #if globals.amplitudeA > globals.amplitudeB:
        #    if globals.amplitudeA > globals.amplitudeC:
        #        return Sector.A
        #    else:
        #        return Sector.C
        #else:
        #    if globals.amplitudeB > globals.amplitudeC:
        #        return Sector.B
        #    else:
        #        return Sector.C

    def run(self):
        while True:
            self.get_sector()
            # print(sector)
            # self.options[sector]()
            self.options[self.sector]()
            print(self.sector)
            # mutex.lock()s
            time.sleep(0.00001)
            # mutex.unlock()
