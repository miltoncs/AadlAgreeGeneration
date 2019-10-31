# Given some constant params, return a piecewise function that estimates the kinematics equation
# d(a, t, v0, d0) = (1/2) * a * (t^2) + v0 * t + d0
# Using the Tangent Line Approximation process

# We want to know when the curve does not intersect y=0, indicating that the maneuver was successful in avoiding the
# ground.
import sys
import linearize

# Curve Parameters
given_acceleration = 40
given_initial_velocity = -150
given_initial_altitude = 500


# local optima (min/max point) is at -b / 2a
def local_optima():
    t = -given_initial_velocity / (2.0 * given_acceleration)
    return distance_via_kinematic(t)


# 1/2 * a * (t**2) + v_0 * t + y
def distance_via_kinematic(time):
    return 0.5 * given_acceleration * (time ** 2) + given_initial_velocity * time + given_initial_altitude


# Derivative of the kinematic function
def velocity_via_kinematic(time):
    return given_acceleration * time + given_initial_velocity


def linearize_quadratic():

    linear_representation = linearize.Linearization(distance_via_kinematic, velocity_via_kinematic, segments=5, start=0, end=12)

    linear_representation.print_linearization_parameters()
    print("Clearance:       ", min([p[1] for p in linear_representation.segment_start_points]))

    linear_representation.print_agree_node()
    sys.stdout.flush()

    linear_representation.plot_piecewise_representation()


if __name__ == "__main__":
    linearize_quadratic()
