import matplotlib.pyplot as plt
import numpy as np
import sys


class Linearization:

    # Plotting points per unit distance
    plot_precision = 10

    def __init__(self, underlying_function, derivative_function, segments=10, start=-10, end=10):

        self.underlying_function = underlying_function
        self.derivative_function = derivative_function
        self.approx_segments = segments
        self.plot_start_x = start
        self.plot_end_x = end

        self.segment_width = ((self.plot_end_x - self.plot_start_x) / self.approx_segments)
        self.cutoffs = np.arange(self.plot_start_x, self.plot_end_x, self.segment_width)
        self.dx = 0.5 * self.segment_width
        self.slopes = [self.derivative_function(x + self.dx) for x in self.cutoffs]
        self.y_ints = [linear_y_intercept(x + self.dx, self.underlying_function(x + self.dx), self.derivative_function(x + self.dx)) for x in self.cutoffs]
        self.segment_start_points = [(self.cutoffs[x], self.cutoffs[x] * self.slopes[x] + self.y_ints[x]) for x in range(self.approx_segments)]
        self.approximation_function = self.get_approximation_function()

    def check_plot_params(self):
        assert self.plot_end_x > self.plot_start_x
        assert self.plot_precision > 0

    def get_approximation_function(self):

        def piecewise_function(t):

            if t < self.cutoffs[0]:
                return self.slopes[0] * t + self.y_ints[0]

            if t >= self.cutoffs[-1]:
                return self.slopes[-1] * t + self.y_ints[-1]

            for piece in range(self.approx_segments - 1):
                if self.cutoffs[piece] <= t < self.cutoffs[piece + 1]:
                    return self.slopes[piece] * t + self.y_ints[piece]

            raise Exception("For some reason, I couldn't match the input value: %f" % t)

        return piecewise_function

    def get_approximation_params(self):

        return self.approx_segments, self.segment_width, self.cutoffs, self.segment_start_points, self.slopes, self.y_ints

    def print_linearization_parameters(self):
        print("cutoffs          ", " ".join(["%9.2f" % round(num, 2) for num in self.cutoffs]))
        print("slopes           ", " ".join(["%9.2f" % round(num, 2) for num in self.slopes]))
        print("y-intercepts     ", " ".join(["%9.2f" % round(num, 2) for num in self.y_ints]))
        print("Points:          ", " ".join(["(%.2f,%.2f)" % (round(num[0], 2), round(num[1], 2)) for num in self.segment_start_points]))

    def print_agree_node(self):
        print("aadl expression: \n")
        print("node linearization(t: real) returns(y: real);")
        print("let")
        print("\ty = if t <= %.2f then %.2f*t + %.2f" % (self.cutoffs[0], self.slopes[0], self.y_ints[0]))
        for i in range(self.approx_segments - 1):
            print("\t\telse if t > %.2f and t <= %.2f then %.2f*t + %.2f" % (
                self.cutoffs[i], self.cutoffs[i+1], self.slopes[i], self.y_ints[i]))
        print("\telse %.2f*t + %.2f;" % (self.slopes[-1], self.y_ints[-1]))
        print("tel;")

    def plot_piecewise_representation(self):
        self.check_plot_params()
        x_values = [i / self.plot_precision for i in range(self.plot_start_x * self.plot_precision, self.plot_end_x * self.plot_precision, 1)]
        approx_y_values = [self.approximation_function(x) for x in x_values]
        real_y_values = [self.underlying_function(x) for x in x_values]
        plt.plot(x_values, approx_y_values, 'r')
        plt.plot(x_values, real_y_values, 'b')
        plt.show()

    def set_plot_window(self, start, end):
        self.plot_start_x = start
        self.plot_end_x = end
        self.check_plot_params()


def linear_y_intercept(x_coord, y_coord, slope):
    return y_coord - (slope * x_coord)
