from collections import OrderedDict
import logging
from matplotlib import pyplot
from numpy import mean, std as stdev
from utility_functions import clean_value, float_range
from uncertainty.data_sources.model_data_sources import get_source_matrix_of_type
from uncertainty.data_sources.uncertainty_data_sources import get_uk_supply_error, get_uk_supply
from uncertainty.data_structures.data_structures import DataSource
from uncertainty.source_uncertainty_distribution.uncertainty_functions import get_ancestors_and_self, linear_regression
from math import log as ln


def get_cleaned_thing(system: str, dictionary_of_thing: dict) -> dict:
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


def map_things_together(thing1: dict, thing2: dict) -> list:
    """
    thing1's keys must be ancestor or selfs of thing2's keys
    :param thing1:
    :param thing2:
    :return: list of tuples
    """
    x_y = list()
    error_key_map = {error_key: get_ancestors_and_self(error_key) for error_key in thing2.keys()}
    for error_key, error in thing2.items():
        for ancestor in error_key_map[error_key]:
            if ancestor in thing1.keys():
                x_y.append((thing1[ancestor], error))
    return sorted(x_y)


def add_regression_line_to_graph(a: float, b: float, x: list, colour: str="x"):
    pyplot.hold(True)
    sorted_x = [i for i in float_range(0.001, max(x))]
    y = [a * ln(x_i) + b for x_i in sorted_x]
    y = [y_i if y_i > 0.001 else 0.001 for y_i in y]
    pyplot.plot(sorted_x, y, colour)


if __name__ == '__main__':
    # TODO get uk supply and relative error and plot
    logging.basicConfig(format='%(message)s - %(asctime)-15s', level=logging.DEBUG)
    uk_supply = get_uk_supply(2008)
    uk_error = get_uk_supply_error()
    source_data_item = DataSource(2008, "UK", "consumption")

    system = "SIC3"
    clean_supply = get_cleaned_thing(system, uk_supply)
    clean_error = get_cleaned_thing(system, uk_error)

    x_y = map_things_together(clean_supply, clean_error)

    x_y_counter = dict()
    for x, y in x_y:
        if x not in x_y_counter:
            x_y_counter[x] = list()
        x_y_counter[x].append((y + x) / x)

    x_mean = {x: mean(y) for x, y in x_y_counter.items()}
    x_stdev = {x: stdev(y) for x, y in x_y_counter.items()}

    x = list()
    y1 = list()
    y2 = list()
    y3 = list()
    st_dev = list()
    for a in x_y_counter.keys():
        x.append(a)
        y1.append(ln(x_mean[a]))
        y2.append(ln(x_mean[a] + x_stdev[a]))
        y3.append(ln(x_mean[a] - x_stdev[a]))
        st_dev.append(x_stdev[a])

    mean_a, mean_b = linear_regression([ln(x_i) for x_i in x], y1)
    stdev_upper_a, stdev_upper_b = linear_regression([ln(x_i) for x_i in x], y2)
    stdev_lower_a, stdev_lower_b = linear_regression([ln(x_i) for x_i in x], y3)
    pyplot.plot(x, y1, "kx", x, y2, "r_", x, y3, "g_")
    add_regression_line_to_graph(mean_a, mean_b, x, colour="b")
    add_regression_line_to_graph(stdev_upper_a, stdev_upper_b, x, colour="r")
    add_regression_line_to_graph(stdev_lower_a, stdev_lower_b, x, colour="g")
    pyplot.ylabel("ln((x + delta x) / x)")
    pyplot.xlabel("supply value")
    pyplot.show()
    pyplot.tight_layout()
    # if "c" in x or "c" in y:
    #     raise ValueError("c")
    # pyplot.scatter(x, y, marker="x")
    # pyplot.show()
