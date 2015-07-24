from math import log as ln
from matplotlib import pyplot
from utility_functions import float_range


def plot(xs: tuple, ys: tuple, styles: tuple, hold: bool, xlabel: str="", ylabel: str=""):
    pyplot.figure()
    for i, x in enumerate(xs):
        pyplot.plot(x, ys[i], styles[i])
        pyplot.hold(True)

    pyplot.tight_layout(pad=0.5)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    if not hold:
        pyplot.hold(False)
        pyplot.show()


def add_regression_line_to_graph(a: float, b: float, x: list, colour: str="x", min_y: float=0.001):
    pyplot.hold(True)
    sorted_x = [i for i in float_range(min_y, max(x))]
    y = [a * ln(x_i) + b for x_i in sorted_x]
    y = [y_i if y_i > min_y else min_y for y_i in y]
    pyplot.plot(sorted_x, y, colour)


def plot_x_y(x_y: list, x_label: str="UK supply", y_label: str="(\Delta x + x) / x"):
    """
    will plot a list of tuples of x, y coordinates
    :param x_y: list of tuples [(x, y)]
    :param x_label:
    :param y_label:
    :return:
    """
    x = list()
    y = list()
    for x_i, y_i in x_y:
        x.append(x_i)
        y.append((y_i + x_i) / x_i)
    plot((x, ), (y,), ("kx", ), True, x_label, y_label)
