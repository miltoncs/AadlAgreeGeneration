# Distance from geofence as a function of time is described by R -R*cos(t)

from math import sqrt, cos, sin, pi, ceil

import linearize

turning_velocity = 100  # ft/sec
turning_radius = 100  # ft
turning_circumference = (2 * pi * turning_radius)  # ft

interval = turning_circumference / turning_velocity  # seconds per revolution
frequency = (2 * pi) / interval

offset = (pi / 2)
coefficient = turning_radius


def neg_cos(t):
    return coefficient * cos((t * frequency) + offset) + turning_radius


def neg_cos_derivative_function(t):
    return -coefficient * frequency * sin((t * frequency) + offset)


def linearize_circle():
    print("Turn Circle -- Radius: %f  Circumference: %f  Interval: %f" % (turning_radius, turning_circumference, interval))

    linear_representation = linearize.Linearization(neg_cos, neg_cos_derivative_function, segments=10, start=0, end=(ceil(interval/2)))
    linear_representation.print_linearization_parameters()
    linear_representation.plot_piecewise_representation()
    linear_representation.print_agree_node()


if __name__ == "__main__":
    linearize_circle()

