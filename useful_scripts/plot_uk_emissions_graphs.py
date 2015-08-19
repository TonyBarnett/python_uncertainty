from matplotlib import pyplot
from utility_functions.cartesian_plot_functions import get_r_squared

from uncertainty.data_sources.uncertainty_data_sources import get_uk_emissions_and_error
from uncertainty.source_uncertainty_distribution import LogNormalDistributionFunction
from useful_scripts.useful_functions.plot_functions import plot, add_regression_lines_to_graph, \
    PRESENTATION_LOCATION, THESIS_LOCATION
from math import log as ln

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
    distribution_function = LogNormalDistributionFunction.create_from_x_y_coordinates(x, y)

    plot((x,),
         ([y_i / x[i] for i, y_i in enumerate(y)],),
         ("kx",),
         hold=True,
         xlabel="Emissions value",
         ylabel="$\Delta x / x$",
         title="UK Emissions"
         )

    # add_regression_lines_to_graph(distribution_function.mean_a,
    #                               distribution_function.mean_b,
    #                               x,
    #                               min_y=10 ** -10,
    #                               multiplier=1.96)

    add_regression_lines_to_graph(distribution_function.mean_a,
                                  distribution_function.mean_b,
                                  x,
                                  min_y=10 ** -10,
                                  multiplier=1
                                  )

    print("\\mu = {0:.4f} \\text{{ln }} x + {1:.4f}".format(distribution_function.mean_a, distribution_function.mean_b))
    print("\\sigma = {0:.4f} \\text{{ln }} x + {1:.4f}".format(distribution_function.stdev_a,
                                                               distribution_function.stdev_b))

    print("r_squared = {0:.4f}".format(get_r_squared([ln(x_i) for x_i in x],
                                                     [y_i / x[i] for i, y_i in enumerate(y)],
                                                     distribution_function.mean_a,
                                                     distribution_function.mean_b)))

    pyplot.savefig(THESIS_LOCATION + "uk_emissions_input_distribution.pdf")
    pyplot.savefig(PRESENTATION_LOCATION + "uk_emissions_input_distribution.pdf")
