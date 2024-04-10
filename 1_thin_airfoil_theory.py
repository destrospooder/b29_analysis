#!/bin/env python

# Roughly analogous to HW 4 Problem 4

import numpy as np
import sympy as sp
import math as math
import matplotlib.pyplot as plt
from parameters import *

alpha = np.linspace(-np.deg2rad(10), np.deg2rad(10), 100)
b29_root.thin_airfoil_theory(alpha, load = 'b29_root')
b29_tip.thin_airfoil_theory(alpha, load = 'b29_tip')

# to redo fourier coeff integration, uncomment
# b29_root.thin_airfoil_theory(alpha, save = 'b29_root')
# b29_tip.thin_airfoil_theory(alpha, save = 'b29_tip')

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('Cl and Cm_LE for b29 root airfoil')

ax1 = ax[0]
ax1.plot(alpha, b29_root.Cl, color = 'k')
ax1.plot(-(b29_root.Cl[0] - ((b29_root.Cl[-1] - b29_root.Cl[0])/(alpha[-1] - alpha[0])) * alpha[0]) /  ((b29_root.Cl[-1] - b29_root.Cl[0])/(alpha[-1] - alpha[0])), 0, 'ro', label = 'alpha_L0 =' + str(math.degrees(-(b29_root.Cl[0] - ((b29_root.Cl[-1] - b29_root.Cl[0])/(alpha[-1] - alpha[0])) * alpha[0]) /  ((b29_root.Cl[-1] - b29_root.Cl[0])/(alpha[-1] - alpha[0])))) + ' degrees')
ax1.set_xlabel('alpha [rad]')
ax1.set_ylabel('Cl')
ax1.legend()
ax1.set_title('Cl vs. alpha')

ax2 = ax[1]
ax2.plot(alpha, b29_root.Cm_LE, color = 'k')
ax2.set_xlabel('alpha [rad]')
ax2.set_ylabel('Cm_LE')
ax2.set_title('Cm_LE vs. alpha')
plt.tight_layout()
plt.savefig('plots/b29_root_2d_airfoil_behavior.png')
plt.show()

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('Cl and Cm_LE for b29 tip airfoil')

ax1 = ax[0]
ax1.plot(alpha, b29_tip.Cl, color = 'k')
ax1.plot(-(b29_tip.Cl[0] - ((b29_tip.Cl[-1] - b29_tip.Cl[0])/(alpha[-1] - alpha[0])) * alpha[0]) /  ((b29_tip.Cl[-1] - b29_tip.Cl[0])/(alpha[-1] - alpha[0])), 0, 'ro', label = 'alpha_L0 =' + str(math.degrees(-(b29_tip.Cl[0] - ((b29_tip.Cl[-1] - b29_tip.Cl[0])/(alpha[-1] - alpha[0])) * alpha[0]) /  ((b29_tip.Cl[-1] - b29_tip.Cl[0])/(alpha[-1] - alpha[0])))) + ' degrees')
ax1.set_xlabel('alpha [rad]')
ax1.set_ylabel('Cl')
ax1.legend()
ax1.set_title('Cl vs. alpha')

ax2 = ax[1]
ax2.plot(alpha, b29_tip.Cm_LE, color = 'k')
ax2.set_xlabel('alpha [rad]')
ax2.set_ylabel('Cm_LE')
ax2.set_title('Cm_LE vs. alpha')
plt.tight_layout()
plt.savefig('plots/b29_tip_2d_airfoil_behavior.png')
plt.show()

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('Fl for b29 root, b29 tip')

ax1 = ax[0]
ax1.plot(alpha, 1/2 * b29_root.Cl * density * (plane.cruise_speed**2) * wing.wing_area, color = 'k')
ax1.set_xlabel('alpha [rad]')
ax1.set_ylabel('Fl [N]')
ax1.legend()
ax1.set_title('Fl vs. alpha, b29_root')

ax2 = ax[1]
ax2.plot(alpha, 1/2 * b29_tip.Cl * density * (plane.cruise_speed**2) * wing.wing_area, color = 'k')
ax2.set_xlabel('alpha [rad]')
ax2.set_ylabel('Fl [N]')
ax2.set_title('Fl vs. alpha, b29_tip')
plt.tight_layout()
plt.savefig('plots/lift_force_comparison.png')
plt.show()
