from uncertainty.source_uncertainty_distribution.distribution import LogNormalDistribution, \
    LogNormalDistributionFunction


def get_eu_supply_distribution() -> LogNormalDistribution:
    # TODO this is obviously just a placeholder, make some real numbers!
    return LogNormalDistribution(1, 2)


def get_eu_supply_distribution_function() -> LogNormalDistributionFunction:
    # TODO this is obviously just a placeholder, make some real numbers!
    return LogNormalDistributionFunction(1, 2, 3, 4)
