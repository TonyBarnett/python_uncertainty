import logging

from matplotlib import pyplot
from utility_functions import clean_value
from utility_functions.cartesian_plot_functions import get_r_squared
from math import log as ln

from uncertainty.data_sources.uncertainty_data_sources import get_uk_supply_error, get_uk_supply
from uncertainty.data_structures.data_structures import DataSource
from uncertainty.source_uncertainty_distribution import LogNormalDistributionFunction
from useful_scripts.useful_functions.plot_functions import plot, add_regression_lines_to_graph, \
    PRESENTATION_LOCATION, THESIS_LOCATION
from useful_scripts.useful_functions.mapping_functions import map_thing2_to_thing1_together


def clean_supply_and_supply_error_keys(system: str, dictionary_of_thing: dict) -> dict:
    clean_source_values = {source_value: clean_value(system, source_value) for source_value in dictionary_of_thing}

    clean_thing = dict()
    for key, supplies in clean_source_values.items():
        len_supplies = len(supplies)
        for clean_key in supplies:
            if dictionary_of_thing[key] == "c":
                len_supplies -= 1
                continue
            clean_thing[clean_key] = float(dictionary_of_thing[key]) / len_supplies
    return clean_thing


if __name__ == '__main__':
    # TODO get uk supply and relative error and plot
    logging.basicConfig(format='%(message)s - %(asctime)-15s', level=logging.DEBUG)
    uk_supply = get_uk_supply(2008)
    uk_error = get_uk_supply_error()
    source_data_item = DataSource(2008, "UK", "consumption")

    system = "SIC3"
    clean_supply = clean_supply_and_supply_error_keys(system, uk_supply)
    clean_error = clean_supply_and_supply_error_keys(system, uk_error)

    x_y = map_thing2_to_thing1_together(clean_supply, clean_error)

    x = list()
    y = list()

    for x_i, y_i in x_y:
        x.append(x_i)
        y.append(y_i)
    distribution_function = LogNormalDistributionFunction.create_from_x_y_coordinates(x, y)

    plot((x,),
         ([y_i / x[i] for i, y_i in enumerate(y)],),
         ("kx",),
         hold=True,
         xlabel="Supply value",
         ylabel="$\Delta x / x$",
         title="UK supply"
         )

    # add_regression_lines_to_graph(distribution_function.mean_a, distribution_function.mean_b, x, multiplier=1.96)
    add_regression_lines_to_graph(distribution_function.mean_a, distribution_function.mean_b, x, multiplier=1)
    print("\\mu = {0:.4f} ln(x) + {1:.4f}".format(distribution_function.mean_a, distribution_function.mean_b))
    print("\\sigma = {0:.4f} ln(x) + {1:.4f}".format(distribution_function.stdev_a, distribution_function.stdev_b))

    print("r_squared = {0:.4f}".format(get_r_squared([ln(x_i) for x_i in x],
                                                     [y_i / x[i] for i, y_i in enumerate(y)],
                                                     distribution_function.mean_a,
                                                     distribution_function.mean_b)))

    pyplot.savefig(THESIS_LOCATION + "uk_supply_input_distribution.pdf")
    pyplot.savefig(PRESENTATION_LOCATION + "uk_supply_input_distribution.pdf")
