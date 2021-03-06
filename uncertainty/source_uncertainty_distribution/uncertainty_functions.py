from matplotlib import pyplot
from math import log as ln
import multiprocessing
from numpy import polyfit, mean, std

from utility_functions.data_sanitation import clean_value
from utility_functions.range_operators import float_range


def get_ancestors_and_self(key: str) -> list:
    # we're assuming here that "key" is valid.
    ancestors = [key]
    for i in range(1, len(key)):
        k = key[:-i]
        if k[-1:] not in (".", "_", '/'):
            ancestors.append(k)
    return ancestors


def clean_totals(raw_totals: dict) -> dict:
    clean_total = dict()
    for key, total in raw_totals.items():
        keys = clean_value("SIC4", key)
        len_keys = len(keys)
        for k in keys:
            if total == "c":
                pass
                # clean_total[year][key] = "c"
            else:
                clean_total[k] = float(total) / len_keys

    return clean_total


def linear_regression(x: list, y: list) -> tuple:
    return polyfit(x, y, 1)


def show_plot():
    pyplot.show()


def plot(*_,
         line_x: list=None,
         line_y: list=None,
         xlabel: str="X",
         ylabel: str="Y",
         title: str="Title",
         save_location: str=None,
         scatter_x: list=None,
         scatter_y: list=None):
    pyplot.figure()
    params = list()
    if scatter_y and scatter_x:
        params += [scatter_x, scatter_y, 'k.']
    if line_x and line_y:
        params += [line_x, line_y, 'r-']

    pyplot.plot(*params, markersize=5)

    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    pyplot.title(title)

    pyplot.tight_layout(pad=0.1)

    if not save_location:
        plot_process = multiprocessing.Process(target=show_plot())
        plot_process.start()
    else:
        pyplot.savefig(save_location)


def get_log_lbf_from_regression_coefficients(a: float, b: float, max_x: float=130000)->tuple:
    x = list()
    y = list()
    for i in float_range(0.1, max_x, 0.5):
        x.append(i)
        y.append(a * ln(i) + b)
    return x, y


def get_lbf_from_regression_coefficients(a: float, b: float, max_x: float=130000)->tuple:
    x = list()
    y = list()
    for i in float_range(0.1, max_x, 0.5):
        x.append(i)
        y.append(a * i + b)
    return x, y


def get_mean(l: list) -> float:
    return float(mean(l))


def get_standard_deviation(l: list) -> float:
    return std(l)


def get_r_squared(x: list, y: list) -> float:
    # (largely) copied from r_squared.m
    a, b = polyfit(x, y, 1)
    y_minus_y_hat = 0
    for i, y_i in enumerate(y):
        y_minus_y_hat += (y_i - (a * x[i] + b)) ** 2

    y_bar = get_mean(y)

    y_minus_y_bar = 0

    for y_i in y:
        y_minus_y_bar += (y_i - y_bar) ** 2

    return 1 - (y_minus_y_hat / y_minus_y_bar)


def get_relative_errors(values: list, errors: list) -> list:
    """
    \Delta(x) / x
     x is the value and \Delta x is the error
    :param values:
    :param errors:
    :return:
    """
    relative_errors = list()
    for i, value in enumerate(values):
        relative_errors.append(errors[i] / value)
    return relative_errors
