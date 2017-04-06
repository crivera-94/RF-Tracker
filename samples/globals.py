from PyQt5.QtCore import QMutex
from enum import Enum
import numpy as np


class Sector(Enum):
    A = 0
    B = 1
    C = 2


def init():
    global amplitudeA
    amplitudeA = 0
    global amplitudeB
    amplitudeB = 0
    global amplitudeC
    amplitudeC = 0
    global pAmplitudeA
    amplitudeA = 0
    global pAmplitudeB
    amplitudeB = 0
    global pAmplitudeC
    amplitudeC = 0
    global distance
    distance = 0

    # 0 -> amplitude A
    # 1 -> amplitude B
    # 2 -> amplitude C
    # 3 -> distance
    global prev_state_means
    prev_state_means = np.zeros(4)
    global prev_covariances
    prev_covariances = np.zeros((4, 4))
    global curr_state_means
    curr_state_means = np.zeros(4)
    global curr_covariances
    curr_covariances = np.zeros((4, 4))

    # 0 -> amplitude A
    # 1 -> amplitude B
    # 2 -> amplitude C
    # 3 -> distance
    global observation
    observation = np.zeros(4)

    global mutex
    mutex = QMutex()
    global global_x
    global_x = 0
    global global_y
    global_y = 0


def set_amplitude_a(num):
    observation[0] = num


def set_amplitude_b(num):
    observation[1] = num


def set_amplitude_c(num):
    observation[2] = num


def set_distance(num):
    observation[3] = num


def amplitude_a():
    return observation[0]


def amplitude_b():
    return observation[1]


def amplitude_c():
    return observation[2]


def distance():
    return observation[3]
