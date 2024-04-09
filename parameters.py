#!/bin/env python

import numpy as np
import scipy as sci

class Airfoil:
    def __init__(self, chord_length, max_thickness, max_thickness_loc, max_camber, max_camber_loc,):
        self.chord_length = chord_length
        self.max_thickness = max_thickness # t
        self.max_thickness_loc = max_thickness_loc
        self.max_camber = max_camber # m
        self.max_camber_loc = max_camber_loc # p

    def process_coords(self, filename):
        coords = np.loadtxt(filename, delimiter = ',')
        self.x_coords = self.chord_length * coords[:, 0]
        self.y_coords = self.chord_length * coords[:, 1]
        self.top_curve = sci.interpolate.CubicSpline(self.x_coords[:19], self.y_coords[:19], extrapolate = False)
        self.bottom_curve = sci.interpolate.CubicSpline(self.x_coords[19:], self.y_coords[19:], extrapolate = False)


class Wing:
    def __init__(self, root_airfoil, tip_airfoil, wingspan, wing_area, twist,):
        self.root_airfoil = root_airfoil
        self.tip_airfoil = tip_airfoil
        self.taper_ratio = tip_airfoil.chord_length / root_airfoil.chord_length
        self.wingspan = wingspan
        self.wing_area = wing_area
        self.aspect_ratio = wingspan ** 2 / wing_area
        self.twist = twist

# b29_root_chord = 5.5 # m
# b29_tip_chord = 2.2 # m

# b29_root_max_thickness = 0.22
# b29_root_max_thickness

# wingspan = 43.05 # m
# wing_area = 161.3 # m
# aspect_ratio = 11.5

# max_takeoff_weight = 133500 * 4.44822 # N
# cruise_speed = 220 * 0.44704 # m/s

# twist = -1 * np.pi/180 # deg