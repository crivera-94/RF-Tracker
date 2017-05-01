import time
from PyQt5.QtCore import QThread, QMutex
from phasedetector import PhaseDetector
from pykalman import KalmanFilter
from math import sqrt, pow, sin, cos, pi, radians
from enum import Enum

from scipy.stats import norm
import numpy as np

# testing imports
from firebase import firebase

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


class DatabaseThread(QThread):
    def __init__(self, email):
        # only instantiated when an internet connection is detected
        QThread.__init__(self)
        self.email = email
        # create JSON object to push to database
        self.data = {
            'amplitude': 0,
            'distance': 0
        }
        self.setup = False
        self.isOnline = True

    def run(self):
        while True:
            if self.setup:
                globals.database.child("users")\
                    .child("coordinates")\
                    .update({"amplitude": globals.amplitudeA}, globals.user_token)
                globals.database.child("users")\
                    .child("coordinates")\
                    .update({"distance": globals.distance}, globals.user_token)
                # print("Posting...")
                # self.data['amplitude'] = globals.global_amplitude
                # self.data['distance'] = globals.global_distance
                # globals.database.update(self.data, globals.user_token)
            else:
                self.data['amplitude'] = globals.global_amplitude
                self.data['distance'] = globals.global_distance
                globals.database.child("users").child("coordinates").set(self.data, globals.user_token)
                # globals.database.push(self.data, globals.user_token)
                # globals.database.child("users").push(self.data, globals.user_token)
                # globals.database.child("coordinates").child("Lana").set(self.data, globals.user_token)
                self.setup = True
            time.sleep(0.01)


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

        n_timesteps = 2
        n_dim_state = 5
        filtered_state_means = np.zeros((n_timesteps, n_dim_state))
        filtered_state_covariances = np.zeros((n_timesteps, n_dim_state, n_dim_state))
        print(filtered_state_means)
        print(filtered_state_covariances)

        observations = np.zeros((3, 2))
        transition_offset = np.zeros((2, 5))

        for t in range(n_timesteps - 1):
            if t == 0:
                # filtered_state_means[t] = data.initial_state_mean
                # filtered_state_covariances[t] = data.initial_state_covariance
                print("initialize means and covariances...")
            filtered_state_means[t + 1], filtered_state_covariances[t + 1] = (
                self.kf.filter_update(
                    filtered_state_means[t],
                    filtered_state_covariances[t],
                    observations[t + 1],
                    transition_offset,
                )
            )

        # measurements = [[1, 0], [0, 0], [0, 1]]
        # print(self.kf.em(measurements).smooth([[2, 0], [2, 1], [2, 2]])[0])

    def run(self):
        counter = 0
        while True:
            globals.mutex.lock()

            # update previous globals
            globals.pAmplitudeA = globals.amplitudeA
            globals.pAmplitudeB = globals.amplitudeB
            globals.pAmplitudeC = globals.amplitudeC
            #globals.prev_state_means = globals.curr_state_means
            #globals.prev_covariances = globals.curr_covariances

            amplitude_a = 0
            amplitude_b = 0
            amplitude_c = 0
            distance = 0

            # tolerable range: +/- 5 value

            for i in range(0, self.sample_size):
                # set amplitude buffers using readings from phase detectors
                amplitude_a = amplitude_a + self.phase_detector0.read_channel_zero()
                # amplitude_b = amplitude_b + self.phase_detector0.read_channel_three()
                # amplitude_c = amplitude_c + self.phase_detector0.read_channel_zero()
                distance = distance + self.phase_detector0.read_channel_two()


            #globals.prev_state_means = globals.curr_state_means
            #globals.prev_covariances = globals.curr_covariances
            #
            # amplitude_a = self.phase_detector0.read_channel_zero()
            # distance = self.phase_detector0.read_channel_two()

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

            globals.mutex.unlock()
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
        # raw angle
        return_value = (self.a_angle * pow(x, 2)) + (self.b_angle * x) + self.c_angle
        # factor = (max_plot_angle/maximum_observable_reading)
        return return_value * (120/1400)

    def get_distance(self, x):
        # raw distance
        return_value = (self.a_distance * pow(x, 2)) + (self.b_distance * x) + self.c_distance
        # factor = (max_plot_distance/maximum_observable_reading)
        return return_value * (180/470)

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
        rho_modified = self.get_distance(distance_voltage)

        coordinates = self.polar_to_cartesian(rho_modified, phi)

        if self.min_valid_voltage < voltage < self.max_valid_voltage and .45 < distance_voltage < 1.48:
            # valid point
            globals.global_x = coordinates[0]
            globals.global_y = coordinates[1]
        else:
            # invalid point
            globals.global_x = 0
            globals.global_y = 220

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

        # uses quadratic function
        # angle coefficients
        self.a = -0.00001729241
        self.b = -0.00437652647
        self.c = 1.21484747253

        # new angle coefficients
        self.a_angle = -162.73642899330
        self.b_angle = 124.85705157978
        self.c_angle = 84.50020263516

        # TODO: Save values
        #self.a_angle = .23616
        #self.b_angle = -179.0777
        #self.c_angle = 218.48212

        # distance coefficients
        self.a_distance = 503.50981468720
        self.b_distance = -513.30730438075
        self.c_distance = 132.01951515620

        self.max_voltage = 2.048
        self.resolution = 2048
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
