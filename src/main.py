"""Assignment 4 - Numerical Analysis

Nikolay Babkin - 321123242"""

import math
from scipy.misc import derivative
from src.userInput import read_polynomial, read_int, read_float

# the error margin
epsilon = 1e-6

# the test data
a = 2.75
b = 3.1
k = 19
x = 3
inters = [0, 3]
start = -1
end = 3.5
interval = 0.3


def f(x):
    return x**3 - 3*(x**2)


class BadInputException(TypeError):
    """an exception for bad input."""
    pass


class NoSolutionException(Exception):
    """an exception for when the method does not work."""
    pass


def find_k(a, b, error=epsilon):
    """Finds the number of attempts needed to find the point of intersection
using the bisection method.
    :param a:      The start of the section to check in.
    :param b:      The end of the section to check in.
    :param error:  The margin of error we allow.
    :return:       The number of iterations to reach a result.
    """
    x = math.log(error / (b - a))
    return math.ceil(x / math.log(2) * -1)


def find_k_test():
    """Tests that the find_k() function works.

    I'll be using a known result to see that the function works correctly."""
    error = epsilon
    print("calculated k: ", find_k(a, b, error))
    print("actual k: ", k)


def bisection_method_intersection(f, start, end, error=epsilon):
    """Finds the value of x for which f(x)=0 between start and end
for a polynomial f.
    :param f:       The polynomial.
    :param start:   The start of the section to check in.
    :param end:     The end of the section to check in.
    :param error:   The margin of error we allow.
    :return:        The value x for which f intersects with the X axis.
    """
    if not callable(f):
        # sanity check for f being a function and not something else
        raise BadInputException("Was not given a function.")

    # find the number of iterations to run based on the error margin
    k = find_k(start, end, error)

    # set prev to some arbitrary value
    for i in range(k):
        mid = abs(end - start) / 2 + start
        f_start = f(start)
        f_mid = f(mid)
        if f_start * f_mid > 0:
            # ignore the first half
            start = mid
        else:
            # ignore the second half
            end = mid
    return mid


def bisection_method_intersection_test():
    """Tests that the function can find an intersection point."""
    try:
        calc_x = bisection_method_intersection(f, a, b)
        print("calculated intersection: ", calc_x)
        print("actual intersection: ", x)
    except BadInputException:
        print("Bad input error.")
    except NoSolutionException:
        print("cannot find intersection for function with the method.")
    finally:
        return


def bisection_method_find_intersections(f, start, end, interval, error=epsilon):
    """
    :param f:           The polynomial.
    :param start:       The start of the section to check in.
    :param end:         The end of the section to check in.
    :param interval:    The size of the intervals in which to check for
     intersections.
    :param error:       The margin of error we allow.
    :return:            A tuple of the points of intersection with the X axis.
    """
    if start > end:
        # a quick check that the start is actually before the end
        start, end = end, start
    # calculate the number of intervals we need to test
    num_intervals = math.ceil((end - start) / interval)

    # setup for checking each interval
    a = start
    b = a + interval
    intersections = []

    for i in range(num_intervals):
        fa = f(a)
        fb = f(b)
        if f(a) * f(b) < 0:
            intersections.append(bisection_method_intersection(f, a, b))
        a = b
        b += interval

    return intersections


def bisection_method_find_intersections_test():
    print("Intervals are: " + str(inters))
    print("Calculated intervals in f(): " + str(bisection_method_find_intersections(f, start, end, interval)))


def find_intersections(f, start, end, interval):
    """Finds all of the intersections of the function in the given area.
    :param f:           The polynomial.
    :param start:       The start of the section to check in.
    :param end:         The end of the section to check in.
    :param interval:    The size of the intervals in which to check for
     intersections.
    :return:            A list of the intersection point values.
    """
    def df(x):
        return derivative(f, x, dx=epsilon)
    # regular intersection points
    intersections1 = bisection_method_find_intersections(f, start, end, interval)
    # intersections of derivative function
    intersections2 = bisection_method_find_intersections(df, start, end, interval)
    # check if extrema are also intersections
    for i in range(len(intersections2)):
        if f(intersections2[i]) <= epsilon and intersections2[i] not in intersections1:
            intersections1.append(intersections2[i])
    return intersections1


def find_intersections_test():
    print("Intervals are: " + str(inters))
    print("Calculated intervals: " + str(find_intersections(f, start, end, interval)))


def main():
    f = read_polynomial().get_func()
    a = read_int("Enter the lower bound of the area.")
    b = read_int("Enter the upper bound of the area.")
    inter = read_float("Enter the interval for looking for points.")
    pts = find_intersections(f, a, b, inter)
    print("The points of intersection are: " + str(pts))


main()
