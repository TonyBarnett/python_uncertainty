from collections.abc import Iterable
from numpy import mean, std as stdev
from uncertainty.source_uncertainty_distribution import LinearDistributionFunction
from uncertainty.source_uncertainty_distribution.uncertainty_functions import linear_regression
from math import log as ln


def get_stdev_ln_y(x: Iterable, mean_: dict, st_dev: dict, multiplier: float=0.0) -> list:
    stdev_y = list()
    for a in x:
        stdev_y.append(ln(mean_[a] + multiplier * st_dev[a]))
    return stdev_y


def get_ln_line_from_regression_coefficients(a: float, b: float, x: list, min_y: float=0.0001) -> list:
    y = list()
    for x_i in x:
        y_i = a * ln(x_i) + b
        y.append(y_i if y_i > min_y else min_y)
    return y


def _get_regression_coefficients(x_y_counter, mean_: dict, st_dev: dict, multiplier: float=0.0) -> list:
    stdev_y = get_stdev_ln_y(x_y_counter, mean_, st_dev, multiplier)
    return linear_regression([ln(x_i) for x_i in x_y_counter.keys()], stdev_y)


def get_upper_and_lower_stdev_regression_coefficients(x_y_counter, mean_: dict, st_dev: dict, multiplier=1.96):
    stdev_upper_a, stdev_upper_b = _get_regression_coefficients(x_y_counter, mean_, st_dev, multiplier)
    stdev_lower_a, stdev_lower_b = _get_regression_coefficients(x_y_counter, mean_, st_dev, -multiplier)

    return stdev_upper_a, stdev_upper_b, stdev_lower_a, stdev_lower_b


def get_mean_stdev(x: list, y: list) -> tuple:
    x_y_counter = LinearDistributionFunction._convert_x_y_to_counter(x, y)
    st_dev = {x: stdev(y) for x, y in x_y_counter.items()}
    mean_ = {x: mean(y) for x, y in x_y_counter.items()}
    return mean_, st_dev


def get_x_mean_stdev_y(x: list, y: list) -> tuple:
    mean_, stdev_ = get_mean_stdev(x, y)
    xx = list()
    y_mean = list()
    y_stdev = list()
    for x_i in set(x):
        xx.append(x_i)
        y_mean.append(mean_[x_i])
        y_stdev.append(stdev_[x_i])
    return xx, y_mean, y_stdev
