import logging
from math import log10
import numpy
from collections import Counter

from uncertainty.distribution import LogNormalDistribution, NormalDistribution
from uncertainty.data_sources.uncertainty_data_sources import get_uk_supply, get_uk_supply_error
from uncertainty.source_uncertainty.uncertainty_functions import linear_regression, \
    get_log_lbf_from_regression_coefficients, \
    get_r_squared, \
    ln, \
    get_ancestors_and_self, clean_totals, \
    get_lbf_from_regression_coefficients
# plot, \
from uncertainty.plot_builder import PlotBuilder, ScatterPlot, LinePlot

YEAR_RANGE = (2008, 2009, 2010)


def get_relative_errors(values: list, errors: list) -> list:
    """
    log10((x + \Delta(x)) / x)
     x is the value and \Delta x is the error
    :param values:
    :param errors:
    :return:
    """
    relative_errors = list()
    for i, value in enumerate(values):
        relative_errors.append(log10(value + errors[i]) - log10(value))
    return relative_errors


def map_supply_to_error(supply_totals: dict, error_totals: dict) -> dict:
    map_ = {x: [] for x in supply_totals.keys()}

    # pick the ancestor that makes the most sense
    for key in error_totals.keys():
        for ancestor in get_ancestors_and_self(key):
            if ancestor in map_:
                map_[ancestor].append(key)
    return map_


def _plot(line_x, line_y, scatter_x, scatter_y):
    linear_line = LinePlot(line_x, line_y)
    scatter = ScatterPlot(scatter_x, scatter_y)
    builder = PlotBuilder()
    builder.add_plot_type(linear_line)
    builder.add_plot_type(scatter)
    builder.plot()


def get_pdf_from_points(y: list):
    return Counter(y)


def get_uk_supply_uncertainty_distribution() -> LogNormalDistribution:
    x_y = list()
    for year in YEAR_RANGE:
        supply_data = clean_totals(get_uk_supply(year))
        supply_error = clean_totals(get_uk_supply_error(year))
        map_ = map_supply_to_error(supply_data, supply_error)
        for supply, errors in map_.items():
            for error in errors:
                x_y.append((supply_data[supply], supply_error[error]))
    sorted_x_y = sorted(x_y)

    x = list()
    y = list()

    for xi, yi in sorted_x_y:
        x.append(xi)
        y.append(yi)
    y_relative_error = get_relative_errors(x, y)

    distribution = LogNormalDistribution.get_distribution_from_coordinate_list(y_relative_error)

    return distribution

if __name__ == '__main__':
    distribution = get_uk_supply_uncertainty_distribution()

