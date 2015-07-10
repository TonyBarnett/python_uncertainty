from uncertainty.data_sources.uncertainty_data_sources import get_eu_emissions_error
from uncertainty.source_uncertainty_distribution.uncertainty_functions import \
    get_mean, \
    get_standard_deviation, \
    ln
from uncertainty.source_uncertainty_distribution.distribution import LogNormalDistribution


def get_uk_emissions_distribution(plot=None) -> LogNormalDistribution:
    emissions = get_eu_emissions_error()
    x = list()
    y = list()
    ln_x = list()
    for value, error in sorted(emissions):
        if float(value) < 0 or float(error) < 0 or float(value) > 160000:
            continue
        x.append(float(value))
        ln_x.append(ln(float(value)))
        y.append(float(error))

    mu = get_mean(ln_x)
    sigma = get_standard_deviation(ln_x)

    return LogNormalDistribution(mu, sigma)


if __name__ == '__main__':
    get_uk_emissions_distribution(plot=True)
