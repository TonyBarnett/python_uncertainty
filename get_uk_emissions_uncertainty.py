import logging
import os

from math import log10
from data_sources import get_eu_emissions_error
from uncertainty_functions import *


if __name__ == '__main__':
    emissions = get_eu_emissions_error()
    x = list()
    y = list()
    ln_x = list()
    for value, error in sorted(emissions):
        if float(value) < 0 or float(error) < 0:
            continue
        x.append(float(value))
        ln_x.append(ln(float(value)))
        y.append(float(error))

    (a, b) = linear_regression(ln_x, y)
    print("y = {0} x + {1}".format(a, b))
    print("r^2 = {0}".format(get_r_squared(x, y)))
    lx, ly = get_lbf_from_regression_coefficients(a, b)

    plot(scatter_x=x, scatter_y=y, line_x=lx, line_y=ly)