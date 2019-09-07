from math import sqrt

import linearize


radius = 16


def half_circle_function(x):
    return radius - sqrt(radius**2 - x**2)


def circle_derivative_function(x):
    return x / sqrt((radius ** 2) - (x ** 2))


def linearize_circle():
    linear_representation = linearize.Linearization(half_circle_function, circle_derivative_function, segments=10, start=-10, end=10)
    linear_representation.print_linearization_parameters()
    linear_representation.set_plot_window(-16, 16)
    linear_representation.plot_piecewise_representation()
    linear_representation.print_agree_node()


if __name__ == "__main__":
    linearize_circle()

