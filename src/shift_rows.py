# The logic:
#   1st line: No movements
#   2nd line: Shift to the left 1 byte
#   3rd line: Shift to the left 2 bytes
#   4th line: Shift to the left 3 bytes
import numpy as np


def shift_rows(state):
    shifted_rows = state.copy()
    for i in range(4):
        shifted_rows[i] = np.roll(state[i], -i)
    return shifted_rows