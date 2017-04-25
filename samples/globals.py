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
    global error_a
    error_a = 0
    global previous_error
    previous_error = 0

    # 0 -> amplitude A
    # 1 -> amplitude B
    # 2 -> amplitude C
    # 3 -> distance
    #n_timesteps = 1
    #n_dim_state = 5
    #global prev_state_means
    #prev_state_means = np.zeros((n_timesteps, n_dim_state))
    #global prev_covariances
    #prev_covariances = np.zeros((n_timesteps, n_dim_state, n_dim_state))
    #global curr_state_means
    #curr_state_means = np.zeros((n_timesteps, n_dim_state))
    #global curr_covariances
    #curr_covariances = np.zeros((n_timesteps, n_dim_state, n_dim_state))

    n_timesteps = 2
    n_dim_state = 5
    global filtered_state_means
    filtered_state_means = np.zeros((n_timesteps, n_dim_state))
    global filtered_state_covariances
    filtered_state_covariances = np.zeros((n_timesteps, n_dim_state, n_dim_state))

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
