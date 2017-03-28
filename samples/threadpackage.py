import time
from PyQt5.QtCore import QThread
from phasedetector import PhaseDetector
from pykalman import KalmanFilter

amplitude = 0
phase = 0


class ADCThread(QThread):

    def __init__(self):
        QThread.__init__(self)
        global amplitude
        global phase
        self.phase_detector0 = PhaseDetector(48)
        self.phase_detector1 = PhaseDetector(52)

    def run(self):
        count = 0
        while count > -1:
            time.sleep(1)
            print("ADCThread Increasing")
            # TODO: OSError: [Errno 5] Input/output error
            # print('Channel 0: {}'.format(self.phase_detector0.read_amplitude()))
            count += 1


class FilterThread(QThread):

    def __init__(self):
        QThread.__init__(self)
        # self.ADCThread = ADCThread
        # self.kf = KalmanFilter(initial_state_mean=0, n_dim_obs=2)

    def run(self):
        count = 0
        while count > -1:
            time.sleep(1)
            print("FilterThread Increasing")
            count += 1