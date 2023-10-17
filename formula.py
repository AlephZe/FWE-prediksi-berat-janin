from scipy import integrate
from scipy.integrate import tplquad
import numpy as np
import math

scale = 0.02855   # Adjust this value according to your scale

def calculate_integrate_volume(points):
    x1, x2, y1, y2 = points
    X = np.array([x1, x2])
    Y = np.array([y1, y2])
    coefficients = np.polyfit(X, Y, 1)
    slope = coefficients[0]
    intercept = coefficients[1]

    def volume_function(x):
        return (slope * x + intercept)**2

    volume, _ = integrate.quad(volume_function, x1, x2)
    volume =( volume * np.pi) * 0.5
    return volume

# Function to calculate and display the distance between two points in physical units
def calculate_distance(point1, point2):
    # Calculate the Euclidean distance in physical units
    distance = float(math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2) * scale)
    # print real pixel distance
    return distance

def calculate_head_volume(diameter):
    r = diameter / 2
    # Batas integral
    r_lower = 0
    r_upper = r
    phi_lower = 0
    phi_upper = np.pi
    theta_lower = 0
    theta_upper = 2 * np.pi

    # Fungsi yang mengembalikan 1 (konstanta) karena kita menghitung volume kepala / asumssi mirip bola
    def volume_integral(r, phi, theta):
        return 1

    # Hitung integral menggunakan scipy.integrate.tplquad
    volume, _ = tplquad(volume_integral, r_lower, r_upper, phi_lower, phi_upper, theta_lower, theta_upper)
    return volume