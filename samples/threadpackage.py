import time
from PyQt5.QtCore import QThread
from phasedetector import PhaseDetector


class ADCThread(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.phase_detector0 = PhaseDetector(48)
        self.phase_detector1 = PhaseDetector(52)

    def run(self):
        print('Channel 0: {0}'.format(self.phase_detector0.read_amplitude()))
        time.sleep(1)

        #count = 0
        #while count > -1:
            #time.sleep(1)
            #print("ADCThread Increasing")
            # TODO: OSError: [Errno 5] Input/output error
            # print('Channel 0: {}'.format(self.phase_detector0.read_amplitude()))
            #count += 1


class FilterThread(QThread):
    @staticmethod
    def run():
        count = 0
        while count > -1:
            time.sleep(1)
            print("FilterThread Increasing")
            count += 1