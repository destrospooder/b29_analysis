#!/bin/env python

# Roughly analogous to HW 5 Problem 3

import numpy as np
import matplotlib.pyplot as plt
from parameters import *

plt.rcParams["axes.grid"] = True 

alpha = np.linspace(-np.deg2rad(20), np.deg2rad(20), 200)
b29_root.thin_airfoil_theory(alpha, load="b29_root")
b29_tip.thin_airfoil_theory(alpha, load="b29_tip")

wing.finite_wing_theory(alpha, 20)

wing.skin_friction()
print('Cd Wing: ' + str(wing.Cd_skin))
print('Skin Friction Drag: ' + str(wing.skin_friction_drag) + ' N')

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle("CL and CD for b29 wing")

ax1 = ax[0]
ax1.plot(alpha, wing.Cl, color="k", label='finite wing estimate')
ax1.plot(alpha, b29_root.cl, color="r", label='2d')
ax1.set_xlabel("alpha [rad]")
ax1.set_ylabel("Cl")
ax1.set_title("Cl vs. alpha")
ax1.legend()

ax1 = ax[1]
ax1.plot(alpha, wing.Cd + wing.Cd_skin, color="k")
ax1.set_xlabel("alpha [rad]")
ax1.set_ylabel("Cd")
ax1.set_title("Cd vs. alpha")

plt.tight_layout()
plt.savefig("plots/lift_totaldrag.png")
plt.show()

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle("CL vs CD for b29 wing")

ax1 = ax[0]
ax1.plot(wing.Cd + wing.Cd_skin, wing.Cl, color="k")
ax1.set_xlabel("Cd")
ax1.set_ylabel("Cl")
ax1.set_title("Cl vs. Cd")

ax1 = ax[1]
ax1.plot(alpha, np.divide(wing.Cl,wing.Cd + wing.Cd_skin), color="k")
ax1.set_xlabel("alpha [rad]")
ax1.set_ylabel("Cl/Cd")
ax1.set_title("Cl/Cd vs. alpha")

plt.tight_layout()
plt.savefig("plots/lifttotaldragratio.png")
plt.show()