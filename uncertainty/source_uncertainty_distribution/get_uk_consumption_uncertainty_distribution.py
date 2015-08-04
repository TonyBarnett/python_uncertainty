from uncertainty.source_uncertainty_distribution.distribution import LogNormalDistribution, \
    LogNormalDistributionFunction
from .get_uk_supply_uncertainty_distribution import get_uk_supply_uncertainty_distribution, \
    get_uk_supply_distribution_function


def get_uk_consumption_uncertainty_distribution() -> LogNormalDistribution:
    """
    Let's be cheeky, we assume the error in consumption is the same as that of supply
    :return:
    """
    # TODO Check this is a valid assumption or change it!
    return get_uk_supply_uncertainty_distribution()


def get_uk_consumption_distribution_function() -> LogNormalDistributionFunction:
    """
    Let's be cheeky, we assume the error in consumption is the same as that of supply
    :return:
    """
    # TODO Check this is a valid assumption or change it!
    return get_uk_supply_distribution_function()
