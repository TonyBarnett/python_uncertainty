from math import log as ln
from matplotlib import pyplot
from utility_functions import float_range


def _add_to_plot(xs: tuple, ys: tuple, styles: tuple, hold: bool=False, xlabel: str="", ylabel: str=""):
    for i, x in enumerate(xs):
        pyplot.plot(x, ys[i], styles[i])
        pyplot.hold(True)

    pyplot.tight_layout(pad=0.5)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    if not hold:
        pyplot.hold(False)
        pyplot.show()


def plot(xs: tuple, ys: tuple, styles: tuple, hold: bool=False, xlabel: str="", ylabel: str=""):
    pyplot.figure()
    _add_to_plot(xs, ys, styles, hold, xlabel, ylabel)


def add_regression_lines_to_graph(a: float,
                                  b: float,
                                  x: list,
                                  colour: tuple=("k", "r", "g"),
                                  min_y: float=0.001,
                                  multiplier: float=1):
    pyplot.hold(True)
    sorted_x = [i for i in float_range(min_y, max(x))]
    mean_y = list()
    stdev_lower = list()
    stdev_upper = list()
    for x_i in sorted_x:
        y_i = a * ln(x_i) + b
        if y_i < min_y:
            y_i = min_y
        mean_y.append(y_i)
        stdev_lower.append(y_i - multiplier * y_i)
        stdev_upper.append(y_i + multiplier * y_i)

    _add_to_plot((sorted_x, sorted_x, sorted_x), (mean_y, stdev_lower, stdev_upper), colour, hold=True)


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
    plot((x, ), (y, ), ("kx", ), True, x_label, y_label)
