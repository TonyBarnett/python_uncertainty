import logging
from math import log10

from uncertainty.distribution import LogNormalDistribution
from uncertainty.data_sources.uncertainty_data_sources import get_uk_supply, get_uk_supply_error
from uncertainty.source_uncertainty.uncertainty_functions import linear_regression, \
    get_lbf_from_regression_coefficients, \
    get_r_squared, \
    ln, \
    get_ancestors_and_self, clean_totals
    # plot, \
from uncertainty.plot_builder import PlotBuilder, ScatterPlot

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
    # (a, b) = linear_regression([ln(x_i) for x_i in x], y_relative_error)
    #
    # (x_line, y_line) = get_lbf_from_regression_coefficients(a, b)

    distribution = LogNormalDistribution.get_distribution_from_coordinate_lists(x, y_relative_error)
    y = distribution.get_pdf_line(x)
    p = ScatterPlot(x, y)

    pb = PlotBuilder()
    pb.add_plot_type(p)
    pb.plot()


if __name__ == '__main__':
    get_uk_supply_uncertainty_distribution()
    # logging.basicConfig(format='%(message)s - %(asctime)-15s', level=logging.INFO)
    # logging.info("starting")
    # get_uk_supply_uncertainty_distribution()
    #
    # plot(scatter_x=x,
    #      scatter_y=y_relative_error,
    #      line_x=x_line,
    #      line_y=y_line,
    #      # save_location=os.getenv("dropboxRoot") + r"\Thesis\Images\supply_relative_error.pdf",
    #      xlabel="Supply quantity.",
    #      ylabel="Relative error in supply.",
    #      title="Relative error in supply.")
    #
    # print("r^2: {0}".format(get_r_squared(x, y)))
    #
    # logging.info("done")
