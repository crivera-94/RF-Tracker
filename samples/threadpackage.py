import time
from PyQt5.QtCore import QThread
from phasedetector import PhaseDetector
from pykalman import KalmanFilter

# antenna 0 - 1
amplitude0 = 0
phase0 = 0

# antenna 1 - 2
amplitude1 = 0
phase1 = 0

# antenna 0 - 2
amplitude2 = 0
phase2 = 0


class ADCThread(QThread):

    def __init__(self):
        QThread.__init__(self)
        global amplitude0
        global phase0
        global amplitude1
        global phase1
        global amplitude2
        global phase2
        self.phase_detector0 = PhaseDetector(48)
        self.phase_detector1 = PhaseDetector(52)
        self.sample_size = 10

    def run(self):
        while True:
            for i in range(0, self.sample_size):
                # set amplitude_temp equal to self.phase_detector0.read_amplitude()
                amplitude_temp = 10
            global amplitude0
            amplitude0 = amplitude_temp/self.sample_size

            time.sleep(1)
            print("ADCThread Increasing: {}".format(amplitude0))
            # TODO: OSError: [Errno 5] Input/output error
            # print('Channel 0: {}'.format(self.phase_detector0.read_amplitude()))


class FilterThread(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.kf = KalmanFilter(initial_state_mean=0, n_dim_obs=2)

    def run(self):
        count = 0
        while count > -1:
            time.sleep(1)
            print("FilterThread Increasing")
            count += 1
