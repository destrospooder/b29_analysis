#!/bin/env python

# Roughly analogous to HW 5 Problem 3

import numpy as np
from parameters import *

wing.skin_friction()
print('Cd Wing: ' + str(wing.Cd_skin))
print('Skin Friction Drag: ' + str(wing.skin_friction_drag) + ' N')