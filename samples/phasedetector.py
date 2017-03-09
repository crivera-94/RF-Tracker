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

    def __init__(self, address=48, busnum=1):
        adc_string = "0x{}, busnum = {}".format(address, busnum)
        self.adc = Adafruit_ADS1x15.ADS1015(adc_string)
        self.GAIN = 2

    def read_amplitude(self):
        return self.adc.read_adc(0, gain=self.GAIN)

    def read_phase(self):
        return self.adc.read_adc(1, gain=self.GAIN)

    def read_third_value(self):
        return self.adc.read_adc(2, gain=self.GAIN)