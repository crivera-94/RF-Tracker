import time
from PyQt5.QtCore import QThread

class AThread(QThread):

    @staticmethod
    def run():
        count = 0
        while count > -1:
            time.sleep(1)
            print("A Increasing")
            count += 1