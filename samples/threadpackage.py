import time
from PyQt5.QtCore import QThread, QMutex
from phasedetector import PhaseDetector
from pykalman import KalmanFilter
from enum import Enum


class Sector(Enum):
    A = 0
    B = 1
    C = 2

# antenna 0 - 1
amplitude0 = 0
phase0 = 0

# antenna 1 - 2
amplitude1 = 0
phase1 = 0

# antenna 0 - 2
amplitude2 = 0
phase2 = 0

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
            global amplitude0
            amplitude0 = amplitude_temp0/self.sample_size
            mutex.unlock()

            time.sleep(0.5)
            print("ADCThread -> Amplitude0: {}".format(amplitude0))
            # TODO: OSError: [Errno 5] Input/output error
            # print('Channel 0: {}'.format(self.phase_detector0.read_amplitude()))


class FilterThread(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.kf = KalmanFilter(initial_state_mean=0, n_dim_obs=2)

    def get_sector(self):
        if amplitude0 > amplitude1:
            if amplitude0 > amplitude2:
                return Sector.A
            else:
                return Sector.C
        else:
            if amplitude1 > amplitude2:
                return Sector.B
            else:
                return Sector.C

    def run(self):
        while True:
            sector = get_sector()

            # mutex.lock()
            time.sleep(0.5)
            print("FilterThread Increasing")
            # mutex.unlock()