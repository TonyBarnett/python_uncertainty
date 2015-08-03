import os

from matplotlib import pyplot
from utility_functions import float_range

from useful_scripts.useful_functions.regression_functions import get_ln_line_from_regression_coefficients

PRESENTATION_LOCATION = os.environ["dropboxRoot"] + r"\Meeting notes\Presentation files\resources" + "\\"
THESIS_LOCATION = os.environ["dropboxRoot"] + r"\Thesis\Images" + "\\"


def _add_labels_to_graph(xlabel: str="", ylabel: str="", title: str=""):
    # it could be the case that you've already added these labels so don't override them with empty values
    if xlabel:
        pyplot.xlabel(xlabel)
    if ylabel:
        pyplot.ylabel(ylabel)
    if title:
        pyplot.title(title)


def _add_to_plot(xs: tuple, ys: tuple, styles: tuple, hold: bool=False, xlabel: str="", ylabel: str="", title: str=""):
    for i, x in enumerate(xs):
        pyplot.plot(x, ys[i], styles[i])
        pyplot.hold(True)

    _add_labels_to_graph(xlabel, ylabel, title)
    pyplot.tight_layout(pad=0.5)
    if not hold:
        pyplot.hold(False)
        pyplot.show()


def plot(xs: tuple, ys: tuple, styles: tuple, hold: bool=False, xlabel: str="", ylabel: str="", title: str=""):
    pyplot.figure()
    _add_to_plot(xs, ys, styles, hold, xlabel, ylabel, title)


def add_regression_lines_to_graph(a: float,
                                  b: float,
                                  x: list,
                                  colour: tuple=("k", "r", "g"),
                                  min_y: float=0.001,
                                  multiplier: float=1):
    pyplot.hold(True)
    sorted_x = [i for i in float_range(min_y, max(x) + 1)]
    stdev_lower = list()
    stdev_upper = list()
    mean_y = get_ln_line_from_regression_coefficients(a, b, sorted_x, min_y)
    for y_i in mean_y:
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
