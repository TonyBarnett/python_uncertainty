from collections import Counter

from .distribution import LogNormalDistribution, LogLinearDistributionFunction
from ..data_sources import get_uk_supply, get_uk_supply_error
from .uncertainty_functions import get_ancestors_and_self, clean_totals, get_relative_errors

# plot, \
from uncertainty.plot_builder import PlotBuilder, ScatterPlot, LinePlot

YEAR_RANGE = (2008, 2009, 2010)


def map_supply_to_error(supply_totals: dict, error_totals: dict) -> dict:
    map_ = {x: [] for x in supply_totals.keys()}

    # pick the ancestor that makes the most sense
    for key in error_totals.keys():
        for ancestor in get_ancestors_and_self(key):
            if ancestor in map_:
                map_[ancestor].append(key)
    return map_


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
        if yi:
            x.append(xi)
            y.append(yi)
    y_relative_error = get_relative_errors(x, y)

    distribution = LogNormalDistribution.get_distribution_from_coordinate_list(y_relative_error)

    return distribution


def get_uk_supply_distribution_function() -> LogLinearDistributionFunction:
    x = list()
    y = list()
    for year in YEAR_RANGE:
        supply_data = clean_totals(get_uk_supply(year))
        supply_error = clean_totals(get_uk_supply_error(year))
        map_ = map_supply_to_error(supply_data, supply_error)
        for supply, errors in map_.items():
            for error in errors:
                if supply_data[supply] is not 0:
                    x.append(supply_data[supply])
                    y.append(supply_error[error])

    return LogLinearDistributionFunction.create_from_x_y_coordinates(x, y)


if __name__ == '__main__':
    d = get_uk_supply_uncertainty_distribution()
