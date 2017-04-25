import time
from PyQt5.QtCore import QThread, QMutex
from phasedetector import PhaseDetector
from pykalman import KalmanFilter
from math import sqrt, pow, sin, cos, pi, radians
from enum import Enum

from scipy.stats import norm
import numpy as np

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

        n_timesteps = 501
        n_dim_state = 5
        filtered_state_means = np.zeros((n_timesteps, n_dim_state))
        filtered_state_covariances = np.zeros((n_timesteps, n_dim_state, n_dim_state))
        print(filtered_state_means)

        # measurements = [[1, 0], [0, 0], [0, 1]]
        # print(self.kf.em(measurements).smooth([[2, 0], [2, 1], [2, 2]])[0])

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

            # tolerable range: +/- 5 value

            #for i in range(0, self.sample_size):
            #    # set amplitude buffers using readings from phase detectors
            #    amplitude_a = amplitude_a + self.phase_detector0.read_channel_zero()
            #    # amplitude_b = amplitude_b + self.phase_detector0.read_channel_three()
            #    # amplitude_c = amplitude_c + self.phase_detector0.read_channel_zero()
            #    distance = distance + self.phase_detector0.read_channel_two()

            globals.prev_state_means = globals.curr_state_means
            globals.prev_covariances = globals.curr_covariances

            amplitude_a = amplitude_a + self.phase_detector0.read_channel_zero()
            distance = distance + self.phase_detector0.read_channel_two()

            globals.curr_state_means, globals.curr_covariances = (
                self.kf.filter_update(
                    globals.prev_state_means,
                    globals.prev_covariances,
                    [amplitude_a, distance]
                )
            )

            # from plot_online.py
            # globals.curr_state_means, globals.curr_covariances = (
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

            # PID Correction
            globals.error_a = 0
            globals.mutex.unlock()
            # print('Channel 0: {}'.format(self.phase_detector0.read_channel_zero()))
            # print('Channel 2: {}'.format(self.phase_detector0.read_channel_two()))
            time.sleep(0.001)


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
            num = -self.b - root
            return num/den
        else:
            return num/den
        # root = ((y-self.c)/self.a) + (pow(self.b, 2)/(4*pow(self.a, 2)))
        # result = -(self.b/(2 * self.a)) + sqrt(root)
        # return result

    def distance_quadratic(self, y):
        root = pow(self.b_distance, 2) + (4 * self.a_distance * (y - self.c_distance))
        num = -self.b_distance + root
        den = 2 * self.a_distance

        if num < 0:
            num = -self.b_distance - root
            return num/den
        else:
            return num/den
        # root = ((y-self.c)/self.a) + (pow(self.b, 2)/(4*pow(self.a, 2)))
        # result = -(self.b/(2 * self.a)) + sqrt(root)
        # return result

    def get_angle(self, x):
        return (self.a_angle * pow(x, 2)) + (self.b_angle * x) + self.c_angle

    def get_distance(self, x):
        # raw distance
        return_value = (self.a_distance * pow(x, 2)) + (self.b_distance * x) + self.c_distance
        return return_value * (180/470)
        # return (self.a_distance * pow(x, 2)) + (self.b_distance * x) + self.c_distance

    def update_globals(self, amplitude_reading, rho, reference_angle):
        # Phi Calculation
        voltage = (amplitude_reading * self.max_voltage) / self.resolution
        phi = reference_angle - self.quadratic(voltage)
        # phi = reference_angle - self.get_angle(voltage)

        # Rho Calculation
        # phi = reference_angle - self.get_angle(voltage)
        # max rho = 180
        # max distance = 120 cm
        distance_voltage = (rho * self.max_voltage) / self.resolution
        # rho_modified = self.distance_quadratic(distance_voltage)
        rho_modified = self.get_distance(distance_voltage)

        coordinates = self.polar_to_cartesian(rho_modified, phi)

        if self.min_valid_voltage < voltage < self.max_valid_voltage and .45 < distance_voltage < 1.48:
            globals.global_x = coordinates[0]
            globals.global_y = coordinates[1]
        else:
            globals.global_x = 0
            globals.global_y = 220

        # coordinates = self.polar_to_cartesian(rho, phi)
        # globals.global_x = coordinates[0]
        # globals.global_y = coordinates[1]

    def sectorA(self):
        # distance can be a max of 180, defined by plot size
        # globals.distance = 90
        # self.update_globals(globals.amplitudeA, globals.distance, 210)

        self.update_globals(globals.amplitudeA, globals.distance, 182)
        # self.update_globals(globals.amplitudeA, globals.distance, 90)

    def sectorB(self):
        self.update_globals(globals.amplitudeB, globals.distance, 90)

    def sectorC(self):
        self.update_globals(globals.amplitudeC, globals.distance, -30)

    def __init__(self):
        QThread.__init__(self)
        self.x = 0
        self.y = 0

        # angle coefficients
        self.a = -0.00001729241
        self.b = -0.00437652647
        self.c = 1.21484747253

        # new angle coefficients
        self.a_angle = -162.73642899330
        self.b_angle = 124.85705157978
        self.c_angle = 84.50020263516

        # distance coefficients
        # self.a_distance = -0.00002794598
        # self.b_distance = 0.00922729969
        # self.c_distance = 0.46038791573

        # new distance coefficients
        # self.a_distance = 110.61729632149
        # self.b_distance = -23.79392489033
        # self.c_distance = -9.91831557457

        self.a_distance = 503.50981468720
        self.b_distance = -513.30730438075
        self.c_distance = 132.01951515620

        self.max_voltage = 2.048
        self.resolution = 2048
        # self.max_valid_voltage = 1.92
        # self.min_valid_voltage = 0.5
        self.max_valid_voltage = 1.38
        self.min_valid_voltage = 0.38
        self.options = {
            Sector.A: self.sectorA,
            Sector.B: self.sectorB,
            Sector.C: self.sectorC
        }

    def get_sector(self):
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
            time.sleep(0.001)
            # mutex.unlock()
