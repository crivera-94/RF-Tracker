import time
from PyQt5.QtCore import QThread
from phasedetector import PhaseDetector


class ADCThread(QThread):

    #def __init__(self):
    #    super().__init__()
    #    self.phase_detector0 = PhaseDetector(48)
    #    self.phase_detector1 = PhaseDetector(52)

    def __init__(self):
        QThread.__init__(self, parent)
        self.yourInit()

    def yourInit(self):
        self.phase_detector0 = PhaseDetector(48)
        self.phase_detector1 = PhaseDetector(52)

    @staticmethod
    def run():
        count = 0
        while count > -1:
            time.sleep(1)
            print("ADCThread Increasing")
            print('Channel 0: {}'.format(phase_detector0.read_amplitude()))
            count += 1


class FilterThread(QThread):
    @staticmethod
    def run():
        count = 0
        while count > -1:
            time.sleep(1)
            print("FilterThread Increasing")
            count += 1