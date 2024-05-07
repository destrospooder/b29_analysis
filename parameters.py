#!/bin/env python

import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline


class Airfoil:
    def __init__(
        self,
        chord_length,
        max_thickness,
        max_thickness_loc,
        max_camber,
        max_camber_loc,
    ):
        self.chord_length = chord_length
        self.max_thickness = max_thickness  # t
        self.max_thickness_loc = max_thickness_loc
        self.max_camber = max_camber  # m
        self.max_camber_loc = max_camber_loc  # p

    def process_coords(self, filename):
        coords = np.loadtxt(filename, delimiter=",")
        self.x_coords = coords[:, 0]
        self.y_coords = coords[:, 1]

        self.xs = np.linspace(0, 1, 1000)
        self.top_curve = (CubicSpline(self.x_coords[:19], self.y_coords[:19]))(self.xs)
        self.bottom_curve = (CubicSpline(self.x_coords[19:], self.y_coords[19:]))(
            self.xs
        )
        self.mean_chord_line = 0.5 * (self.top_curve + self.bottom_curve)  # z-bar

    def thin_airfoil_theory(self, alpha, load="", save=""):
        x, phi = sp.symbols("x phi")

        # i sampled a cubic spline along a sequence of x's. to make differentiating easier in sympy, we're going to fit it to a 7th degree polynomial.

        self.zbar = (
            np.polyfit(self.xs, self.mean_chord_line, 7)
            @ np.vstack([x**7, x**6, x**5, x**4, x**3, x**2, x, 1])
        )[0]

        dzbar_dx = (sp.diff(self.zbar, x)).subs(
            x, (1 / 2) * (1 - sp.cos(phi))
        )

        if load == "":
            self.A0_minus_alpha = (-1 / np.pi) * sp.integrate(dzbar_dx, (phi, 0, np.pi))
            print("A0 calculated")
            self.A1 = (2 / np.pi) * sp.integrate(
                dzbar_dx * sp.cos(phi), (phi, 0, np.pi)
            )
            print("A1 calculated")
            self.A2 = (2 / np.pi) * sp.integrate(
                dzbar_dx * sp.cos(2 * phi), (phi, 0, np.pi)
            )
            print("A2 calculated")
            if save != "":
                print("Saving to data/fourier_coeffs/" + save)
                np.savez(
                    "data/fourier_coeffs/" + save,
                    A0_minus_alpha=self.A0_minus_alpha,
                    A1=self.A1,
                    A2=self.A2,
                )
                print("fourier coeffs saved to data/fourier_coeffs/" + save)
        else:
            print("Loading from data/fourier_coeffs/")
            data = np.load("data/fourier_coeffs/" + load + ".npz", allow_pickle=True)
            self.A0_minus_alpha = data["A0_minus_alpha"].astype(np.float64)
            self.A1 = data["A1"].astype(np.float64)
            self.A2 = data["A2"].astype(np.float64)

        self.Cl = np.pi * (2 * (self.A0_minus_alpha + alpha) + self.A1)
        self.Cm_LE = -(self.Cl / 4) + (np.pi / 4) * (self.A2 - self.A1)
        self.dCl_dalpha, self.Cl_0 = np.polyfit(alpha, self.Cl.astype(np.float64), 1)

        self.Fl = 0.5 * self.Cl * density * (cruise_speed**2) * wing.wing_area
        self.dFl_dalpha, self.Fl_0 = np.polyfit(alpha, self.Fl.astype(np.float64), 1)

        self.alpha_L0 = - self.A0_minus_alpha-0.5 * self.A1


class Wing:
    def __init__(
        self,
        root_airfoil,
        tip_airfoil,
        wingspan,
        wing_area,
        twist,
    ):
        self.root_airfoil = root_airfoil
        self.tip_airfoil = tip_airfoil
        self.taper_ratio = tip_airfoil.chord_length / root_airfoil.chord_length
        self.wingspan = wingspan
        self.wing_area = wing_area
        self.aspect_ratio = wingspan**2 / wing_area
        self.twist = twist

    def finite_wing_theory(self, alpha, n_coeffs):
        odd_indices = np.arange(1, n_coeffs * 2, step=2)
        theta_vals = np.linspace(0.01, np.pi / 2, n_coeffs)
        alpha_l_0 = np.linspace(self.tip_airfoil.alpha_L0, self.root_airfoil.alpha_L0, n_coeffs)
        m0 = self.root_airfoil.dCl_dalpha

        def find_constants(alpha):
            a = np.zeros((n_coeffs, n_coeffs))
            b = np.zeros((n_coeffs, 1))

            for n in range(n_coeffs):
                y = 0.5 * self.wingspan * np.cos(theta_vals[n])
                aoa = alpha - self.twist * y / (self.wingspan / 2)
                
                a[n:, ] = [(4 * self.wingspan / (m0 * (self.root_airfoil.chord_length - (self.root_airfoil.chord_length - self.tip_airfoil.chord_length) * y / (self.wingspan / 2)))) * np.sin(odd_indices[i] * theta_vals[n]) + odd_indices[i] * np.sin(odd_indices[i] * theta_vals[n]) / np.sin(theta_vals[n]) for i in range(n_coeffs)]
                b[n] = aoa - alpha_l_0[n]
                
            coeffs = np.linalg.solve(a, b)
            cl = coeffs[0] * np.pi * self.aspect_ratio
            delta = sum(odd_indices[i] * (coeffs[i] / coeffs[0]) ** 2 for i in range(n_coeffs)) - odd_indices[0]
            e = 1 / (1 + delta)
            cd = cl ** 2 / (np.pi * self.aspect_ratio * e)
            induced_aoa = sum(odd_indices[i] * coeffs[i] * np.sin(odd_indices[i] * theta_vals[i]) / np.sin(theta_vals[i]) for i in range(n_coeffs))
            return cl, cd
        
        self.Cl, self.Cd = [], []
        for k in alpha:
            constants = find_constants(k)
            self.Cl.append(constants[0])
            self.Cd.append(constants[1])
            
    def skin_friction(self, n = int(1e4), Re_crit = 3e5):
        section_points = self.wingspan / (2 * np.linspace(1, n, n))

        chord_per_point = self.root_airfoil.chord_length - (self.root_airfoil.chord_length - self.tip_airfoil.chord_length) * section_points / (self.wingspan / 2)
        l_crit = Re_crit * dyn_viscosity / (density * cruise_speed)

        # assume laminar, here's some blasius
        turbulent_drag = 0.027 * density * (cruise_speed ** 2) * chord_per_point * section_points / (((density * cruise_speed * chord_per_point / dyn_viscosity)) ** 1/7)
        overlap = 0.027 * density * (cruise_speed ** 2) * l_crit * section_points / (Re_crit ** 1/7)
        laminar_drag = 0.664 * density * (cruise_speed ** 2) * chord_per_point * section_points / (Re_crit ** 0.5)

        self.skin_friction_drag = sum(2 * (turbulent_drag - overlap + laminar_drag))
        self.Cd_skin = self.skin_friction_drag / (1/2 * density * (cruise_speed ** 2) * (self.wingspan / 2) * self.root_airfoil.chord_length)



# chord lengths were estimated using a three-view pic of the b29
b29_root = Airfoil(5.5, 0.22, 0.302, 0.017, 0.302)
b29_tip = Airfoil(2.2, 0.09, 0.30, 0.022, 0.30)
wing = Wing(b29_root, b29_tip, 43.05, 161.3, -1 * np.pi / 180)

max_takeoff_weight = 133500 * 4.44822  # N
cruise_speed = 220 * 0.44704  # m/s
density = 0.387  # kg/m^3, at 10000 m up
dyn_viscosity = 1.78e-5 # kg/(ms), sutherland's law can suck my-

b29_root.process_coords("data/b29_root.csv")
b29_tip.process_coords("data/b29_tip.csv")
