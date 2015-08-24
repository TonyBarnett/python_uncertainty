from .distribution import LogNormalDistribution
from uncertainty.source_uncertainty_distribution import LogLinearDistributionFunction


def get_eu_consumption_distribution() -> LogNormalDistribution:
    # TODO this is obviously just a placeholder, make some real numbers!
    return LogNormalDistribution(1, 2)


def get_eu_consumption_distribution_function() -> LogLinearDistributionFunction:
    # TODO this is obviously just a placeholder, make some real numbers!
    return LogLinearDistributionFunction(1, 2, 3, 4)
