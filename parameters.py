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

        self.xs = np.linspace(0, self.chord_length, 1000)
        self.top_curve = (sci.interpolate.CubicSpline(self.x_coords[:19], self.y_coords[:19]))(self.xs)
        self.bottom_curve = (sci.interpolate.CubicSpline(self.x_coords[19:], self.y_coords[19:]))(self.xs)
        self.mean_chord_line = 0.5 * (self.top_curve + self.bottom_curve) # z-bar

class Wing:
    def __init__(self, root_airfoil, tip_airfoil, wingspan, wing_area, twist,):
        self.root_airfoil = root_airfoil
        self.tip_airfoil = tip_airfoil
        self.taper_ratio = tip_airfoil.chord_length / root_airfoil.chord_length
        self.wingspan = wingspan
        self.wing_area = wing_area
        self.aspect_ratio = wingspan ** 2 / wing_area
        self.twist = twist

# chord lengths were estimated using a three-view pic of the b29
b29_root = Airfoil(5.5, 0.22, 0.302, 0.017, 0.302)
b29_tip = Airfoil(2.2, 0.09, 0.30, 0.022, 0.30)

b29_root.process_coords('data/b29_root.csv')
b29_tip.process_coords('data/b29_tip.csv')

# wingspan = 43.05 # m
# wing_area = 161.3 # m
# aspect_ratio = 11.5

# max_takeoff_weight = 133500 * 4.44822 # N
# cruise_speed = 220 * 0.44704 # m/s

# twist = -1 * np.pi/180 # deg