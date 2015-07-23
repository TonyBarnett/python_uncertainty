from uncertainty.source_uncertainty_distribution.uncertainty_functions import linear_regression
from math import log as ln


def get_stdev_y(x_y_counter, mean_: dict, st_dev: dict, multiplier: float=0.0) -> list:
    stdev_y = list()
    for a in x_y_counter.keys():
        stdev_y.append(ln(mean_[a] + multiplier * st_dev[a]))
    return stdev_y


def _get_regression_coefficients(x_y_counter, mean_: dict, st_dev: dict, multiplier: float=0.0) -> list:
    stdev_y = get_stdev_y(x_y_counter, mean_, st_dev, multiplier)
    return linear_regression([ln(x_i) for x_i in x_y_counter.keys()], stdev_y)


def get_upper_and_lower_stdev_regression_coefficients(x_y_counter, mean_: dict, st_dev: dict):
    stdev_upper_a, stdev_upper_b = _get_regression_coefficients(x_y_counter, mean_, st_dev, 1.96)
    stdev_lower_a, stdev_lower_b = _get_regression_coefficients(x_y_counter, mean_, st_dev, -1.96)

    return stdev_upper_a, stdev_upper_b, stdev_lower_a, stdev_lower_b
