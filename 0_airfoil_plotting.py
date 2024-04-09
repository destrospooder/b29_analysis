#!/bin/env python

import numpy as np
import scipy as sci
import matplotlib.pyplot as plt
from parameters import *

# chord lengths were estimated using a three-view pic of the b29
b29_root = Airfoil(5.5, 0.22, 0.302, 0.017, 0.302)
b29_tip = Airfoil(2.2, 0.09, 0.30, 0.022, 0.30)

b29_root.process_coords('b29_root.csv')
b29_tip.process_coords('b29_tip.csv')

fig, ax = plt.subplots(2, 1, figsize=(12, 6))

ax1 = ax[0]
ax1.scatter(b29_root.x_coords, b29_root.y_coords, marker = 'o', label = 'airfoil points')
ax1.plot(b29_root.xs, b29_root.top_curve, color = 'k')
ax1.plot(b29_root.xs, b29_root.bottom_curve, color = 'k')
ax1.plot(b29_root.xs, b29_root.mean_chord_line, color = 'r', label = 'mean camber line')
ax1.legend()
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title('b29 root airfoil')

ax2 = ax[1]
ax2.scatter(b29_tip.x_coords, b29_tip.y_coords, marker = 'o', label = 'airfoil points')
ax2.plot(b29_tip.xs, b29_tip.top_curve, color = 'k')
ax2.plot(b29_tip.xs, b29_tip.bottom_curve, color = 'k')
ax2.plot(b29_tip.xs, b29_tip.mean_chord_line, color = 'r', label = 'mean camber line')
ax2.legend()
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_title('b29 tip airfoil')
plt.tight_layout()
plt.savefig('airfoil_plots.png')
plt.show()
