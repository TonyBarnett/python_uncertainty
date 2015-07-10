from .distribution import LogNormalDistribution


def get_eu_consumption_uncertainty_distribution() -> LogNormalDistribution:
    # TODO this is obviously just a placeholder, make some real numbers!
    return LogNormalDistribution(1, 2)
