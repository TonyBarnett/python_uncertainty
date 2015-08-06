from ..data_sources import get_uk_emissions_and_error
from .uncertainty_functions import get_mean, get_standard_deviation, ln, get_relative_errors
from .distribution import LogNormalDistribution, LogNormalDistributionFunction


def get_uk_emissions_distribution() -> LogNormalDistribution:
    emissions = get_uk_emissions_and_error()
    x = list()
    y = list()
    ln_x = list()
    for value, error in sorted(emissions):
        if float(value) < 0 or float(error) < 0 or float(value) > 160000:
            continue
        x.append(float(value))
        ln_x.append(ln(float(value)))
        y.append(float(error))
    y_relative_error = get_relative_errors(x, y)

    mu = get_mean(y_relative_error)
    sigma = get_standard_deviation(y_relative_error)

    return LogNormalDistribution(mu, sigma)


def get_uk_emissions_distribution_function() -> LogNormalDistributionFunction:
    x = list()
    y = list()
    emissions_error = get_uk_emissions_and_error()

    for value, error in sorted(emissions_error):
        if float(value) < 0 or float(error) < 0 or float(value) > 160000:
            continue
        x.append(float(value))
        y.append(float(error))

    return LogNormalDistributionFunction.create_from_x_y_coordinates(x, y)
