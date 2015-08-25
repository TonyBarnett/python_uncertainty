from matplotlib import pyplot
from utility_functions.cartesian_plot_functions import get_r_squared

from uncertainty.data_sources.uncertainty_data_sources import get_uk_emissions_and_error
from uncertainty.source_uncertainty_distribution import LogLinearDistributionFunction, LinearDistributionFunction
from uncertainty.source_uncertainty_distribution.distribution_function import ExponentialDistributionFunction
from useful_scripts.useful_functions.plot_functions import plot, add_regression_lines_to_graph, \
    PRESENTATION_LOCATION, THESIS_LOCATION
from math import log as ln
from useful_scripts.useful_functions.regression_functions import get_x_mean_stdev_y

if __name__ == '__main__':
    emissions_error = get_uk_emissions_and_error()
    x_y_counter = dict()
    x_y = [(float(x), float(y)) for x, y in emissions_error]
    # plot_x_y(x_y)

    x = list()
    y = list()

    for x_i, y_i in x_y:
        if x_i > 0 and y_i > 0:
            x.append(x_i)
            y.append(y_i)

    distribution_functions = dict()
    distribution_functions["LogLinear"] = \
        LogLinearDistributionFunction.create_from_x_y_coordinates(x, y)

    distribution_functions["Linear"] = \
        LinearDistributionFunction.create_from_x_y_coordinates(x, y)

    distribution_functions["Exponential"] = \
        ExponentialDistributionFunction.create_from_x_y_coordinates(x, y)

    for name, distribution_function in distribution_functions.items():
        plot((x,),
             ([y_i / x[i] for i, y_i in enumerate(y)],),
             ("kx",),
             hold=True,
             xlabel="Emissions value",
             ylabel="$\Delta x / x$",
             title="UK Emissions"
             )
        # add_regression_lines_to_graph(distribution_function.mean_a, distribution_function.mean_b, x, multiplier=1.96)
        add_regression_lines_to_graph(x, distribution_function, multiplier=1)

        print("{0} - {1}".format(name, distribution_function))

        mu, sigma = distribution_function.get_mean_stdev_r_squared(x, [y_i / x[i] for i, y_i in enumerate(y)])
        print("{1} - mean r_squared  = {0:.4f}".format(mu, name))
        print("{1} - stdev r_squared = {0:.4f}".format(sigma, name))

        pyplot.savefig(THESIS_LOCATION + "uk_emissions_input_distribution_{0}.pdf".format(name))
        pyplot.savefig(PRESENTATION_LOCATION + "uk_emissions_input_distribution_{0}.pdf".format(name))
    
