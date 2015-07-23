from math import log as ln
from matplotlib import pyplot
from utility_functions import float_range


def plot(xs: tuple, ys: tuple, styles: tuple, xlabel: str, ylabel: str, hold:bool):
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


def add_regression_line_to_graph(a: float, b: float, x: list, colour: str="x"):
    pyplot.hold(True)
    sorted_x = [i for i in float_range(0.001, max(x))]
    y = [a * ln(x_i) + b for x_i in sorted_x]
    y = [y_i if y_i > 0.001 else 0.001 for y_i in y]
    pyplot.plot(sorted_x, y, colour)


def plot_x_y(x_y: list):
    pyplot.figure()
    x = list()
    y = list()
    for x_i, y_i in x_y:
        x.append(x_i)
        y.append((y_i + x_i) / x_i)

    pyplot.plot(x, y, "kx")
    pyplot.xlabel("UK supply")
    pyplot.ylabel("(\Delta x + x) / x")
    pyplot.tight_layout(pad=0.5)
