# File: adc.py
#
# Name: Carlos Rivera
# Description:
#   The PhaseDetector class allows for easy reading of ADC output
#   and allows the phase and amplitude readings to be easily
#   distinguished and read. Each ADC should be setup in the
#   way described inside application.py. At the bare minimum,
#   the first address should correspond to the amplitude, the
#   second to the phase, and finally the last to the remaining
#   analog output from the additional phase detector.

import Adafruit_ADS1x15


class PhaseDetector:

    def __init__(self, addressin=0x48, busnumin=1):
        self.adc = Adafruit_ADS1x15.ADS1015(address=addressin, busnum=busnumin)
        self.GAIN = 2

    # read amplitude
    def read_channel_zero(self):
        return self.adc.read_adc(0, gain=self.GAIN)

    # read phase
    def read_channel_one(self):
        return self.adc.read_adc(1, gain=self.GAIN)

    # read amplitude or phase of remaining antenna
    def read_channel_two(self):
        return self.adc.read_adc(2, gain=self.GAIN)

    def read_channel_three(self):
        return self.adc.read_adc(3, gain=self.GAIN)