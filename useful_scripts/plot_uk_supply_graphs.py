import logging

from math import log as ln

from matplotlib import pyplot

from numpy import mean, std as stdev

from utility_functions import clean_value

from uncertainty.data_sources.uncertainty_data_sources import get_uk_supply_error, get_uk_supply
from uncertainty.data_structures.data_structures import DataSource
from uncertainty.source_uncertainty_distribution.uncertainty_functions import linear_regression
from useful_scripts.useful_functions.plot_functions import plot, plot_x_y, add_regression_lines_to_graph, \
    PRESENTATION_LOCATION
from useful_scripts.useful_functions.regression_functions import \
    get_upper_and_lower_stdev_regression_coefficients, \
    get_stdev_ln_y
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

    # plot_x_y(x_y)

    x_y_counter = dict()
    for x, y in x_y:
        if x not in x_y_counter:
            x_y_counter[x] = list()
        x_y_counter[x].append((y + x) / x)

    x_mean = {x: mean(y) for x, y in x_y_counter.items()}
    x_stdev = {x: stdev(y) for x, y in x_y_counter.items()}

    x = list()
    y = list()
    st_dev = list()
    for a in x_y_counter.keys():
        x.append(a)
        y.append(ln(x_mean[a]))
        st_dev.append(x_stdev[a])

    stdev_upper_a, stdev_upper_b, stdev_lower_a, stdev_lower_b = \
        get_upper_and_lower_stdev_regression_coefficients(x_y_counter, x_mean, x_stdev)

    st_dev_upper_y = get_stdev_ln_y(x_y_counter.keys(), x_mean, x_stdev, 1.96)
    st_dev_lower_y = get_stdev_ln_y(x_y_counter.keys(), x_mean, x_stdev, -1.96)

    mean_a, mean_b = linear_regression([ln(x_i) for x_i in x], y)

    plot((x, ),
         (y, ),
         ("kx", ),
         hold=True,
         xlabel="supply value",
         ylabel="ln((x + delta x) / x)",
         title="UK supply"
          )
    # plot((x, x, x),
    #      (y, st_dev_upper_y, st_dev_lower_y),
    #      ("kx", "r_", "g_"),
    #      hold=True,
    #      xlabel="supply value",
    #      ylabel="ln((x + delta x) / x)",
    #      title="UK supply"
    #      )

    add_regression_lines_to_graph(mean_a, mean_b, x, multiplier=1.96)

    pyplot.savefig(PRESENTATION_LOCATION + "uk_supply.pdf")
