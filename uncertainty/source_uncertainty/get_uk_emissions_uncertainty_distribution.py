from uncertainty.data_sources.uncertainty_data_sources import get_eu_emissions_error
from uncertainty.source_uncertainty.uncertainty_functions import \
    linear_regression, \
    get_lbf_from_regression_coefficients, \
    get_r_squared, \
    get_mean, \
    get_standard_deviation, \
    ln, \
    plot
from uncertainty.distribution import LogNormalDistribution


def get_uk_emissions_distribution() -> LogNormalDistribution:
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

    (a, b) = linear_regression(ln_x, y)
    print("y = {0} x + {1}".format(a, b))
    print("r^2 = {0}".format(get_r_squared(x, y)))
    lx, ly = get_lbf_from_regression_coefficients(a, b)

    plot(scatter_x=x, scatter_y=y, line_x=lx, line_y=ly)

    mu = get_mean(ln_x)
    sigma = get_standard_deviation(ln_x)

    return LogNormalDistribution(mu, sigma)

if __name__ == '__main__':
    get_uk_emissions_distribution()
