from math import log as ln
from matplotlib import pyplot
from numpy import mean, std as stdev
from uncertainty.data_sources.uncertainty_data_sources import get_uk_emissions_and_error
from uncertainty.source_uncertainty_distribution.uncertainty_functions import linear_regression
from useful_scripts.useful_functions.plot_functions import plot_x_y, plot, add_regression_lines_to_graph
from useful_scripts.useful_functions.regression_functions import get_upper_and_lower_stdev_regression_coefficients, \
    get_stdev_ln_y

if __name__ == '__main__':
    emissions_error = get_uk_emissions_and_error()
    x_y_counter = dict()
    x_y = [(float(x), float(y)) for x, y in emissions_error]
    plot_x_y(x_y)

    for e_i, f_i in emissions_error:
        x_i = float(e_i)
        y_i = float(f_i)
        if x_i > 0 and y_i > 0:
            if x_i not in x_y_counter:
                x_y_counter[x_i] = list()
            x_y_counter[x_i].append(1 + y_i)

    x_mean = {x: mean(y) for x, y in x_y_counter.items()}
    x_stdev = {x: stdev(y) for x, y in x_y_counter.items()}

    x = list()
    y = list()

    for a in x_y_counter.keys():
        if a > 0:
            x.append(a)
            y.append(ln(x_mean[a]))

    stdev_upper_a, stdev_upper_b, stdev_lower_a, stdev_lower_b = \
        get_upper_and_lower_stdev_regression_coefficients(x_y_counter, x_mean, x_stdev)

    st_dev_upper_y = get_stdev_ln_y(x_y_counter, x_mean, x_stdev, 1.96)
    st_dev_lower_y = get_stdev_ln_y(x_y_counter, x_mean, x_stdev, -1.96)

    mean_a, mean_b = linear_regression([ln(x_i) for x_i in x], y)

    plot((x, x, x),
         (y, st_dev_upper_y, st_dev_lower_y),
         ("kx", "r_", "g_"),
         True,
         "supply value",
         "ln((x + delta x) / x)"
         )

    add_regression_lines_to_graph(mean_a, mean_b, x, min_y=10**-10, multiplier=1.96)

    pyplot.show()
