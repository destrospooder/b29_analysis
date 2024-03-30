#!/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from parameters import *

def coords_parse(filename, chord_length):
    coords = np.loadtxt(filename, delimiter = ',')
    x = chord_length * coords[:, 0]
    y = chord_length * coords[:, 1]
    return x, y

b29_root_x, b29_root_y = coords_parse('b29_root.csv', b29_root_chord)
b29_tip_x, b29_tip_y = coords_parse('b29_tip.csv', b29_tip_chord)

plt.scatter(b29_root_x, b29_root_y, label = 'root airfoil coordinates')
plt.scatter(b29_root_x[1:19], ((b29_root_y[:19] + b29_root_y[21:]) / 2)[1:19] , label = 'root airfoil mac')
# this isn't exactly correct for the mean camber line, but it's close enough that i'm not concerned
plt.legend()
plt.show()

plt.scatter(b29_tip_x, b29_tip_y, label = 'tip airfoil coordinates')
plt.scatter(b29_tip_x[1:19], ((b29_tip_y[:19] + b29_tip_y[21:]) / 2)[1:19] , label = 'tip airfoil mac')
plt.legend()
plt.show()
