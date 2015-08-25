from math import log as ln, exp
from numpy import std as stdev, mean
from utility_functions.cartesian_plot_functions import get_r_squared
from uncertainty.source_uncertainty_distribution import NormalDistribution
from uncertainty.source_uncertainty_distribution.distribution import Distribution
from uncertainty.source_uncertainty_distribution.uncertainty_functions import linear_regression


class DistributionFunction:
    def __init__(self, mean_a: float=None,
                 mean_b: float=None,
                 stdev_a: float=None,
                 stdev_b: float=None,
                 distribution_type: type(Distribution)=NormalDistribution):
        self.mean_a = mean_a
        self.mean_b = mean_b
        self.stdev_a = stdev_a
        self.stdev_b = stdev_b
        self.distribution_type = distribution_type

    @staticmethod
    def _remove_non_positive_values(key_list: list, value_list: list) -> tuple:
        keys = list()
        values = list()
        for i, x_i in enumerate(key_list):
            if x_i > 0:
                keys.append(x_i)
                values.append(value_list[i])
        return keys, values

    def __getitem__(self, item):
        raise NotImplementedError()

    @classmethod
    def create_from_x_y_coordinates(cls, x, y, distribution_type: type(Distribution)=NormalDistribution):
        raise NotImplementedError()

    @staticmethod
    def _convert_x_y_to_counter(x: list, y: list) -> dict:
        x_y_counter = dict()
        for x, y in zip(x, y):
            if x not in x_y_counter:
                x_y_counter[x] = list()
            x_y_counter[x].append(y)
        return x_y_counter

    @staticmethod
    def _get_mean_stdev_from_counter(x_y_counter, st_dev, mean_):
        x_ = list()
        y_ = list()
        y_std = list()
        for t in x_y_counter.keys():
            x_.append(t)
            y_.append(mean_[t])
            y_std.append(st_dev[t])
        return x_, y_, y_std

    @classmethod
    def _get_means_stdevs(cls, x, y):
        x_y_counter = cls._convert_x_y_to_counter(x, y)
        st_dev = {x: stdev(y) for x, y in x_y_counter.items()}
        mean_ = {x: mean(y) for x, y in x_y_counter.items()}
        return cls._get_mean_stdev_from_counter(x_y_counter, st_dev, mean_)

    def _get_mean_value(self, item):
        raise NotImplementedError()

    def _get_stdev_value(self, item):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def get_mean_stdev_r_squared(self, x, y):
        raise NotImplementedError()


class LinearDistributionFunction(DistributionFunction):
    @classmethod
    def create_from_x_y_coordinates(cls, x, y, distribution_type: type(Distribution)=NormalDistribution):
        x_, y_mean, y_std = LinearDistributionFunction._get_means_stdevs(x, [y_i / x[i] for i, y_i in enumerate(y)])
        mean_a, mean_b = linear_regression(x_, y_mean)
        stdev_a, stdev_b = linear_regression(x_, y_std)

        return cls(mean_a, mean_b, stdev_a, stdev_b)

    def _get_mean_value(self, value):
        return self.mean_a * value + self.mean_b

    def _get_stdev_value(self, value):
        return self.stdev_a * value + self.stdev_b

    def __getitem__(self, item: float) -> float:
        mean_x = self._get_mean_value(item)
        stdev_x = self._get_stdev_value(item)
        d = self.distribution_type(mean_x, stdev_x)
        return d.get_observation()

    def __str__(self):
        return "\\mu = {0} x + {1}, " \
               "\\sigma = {2} x + {3}".format(self.mean_a, self.mean_b,
                                              self.stdev_a, self.stdev_b)

    def get_mean_stdev_r_squared(self, x, y):
        x_, y_mean, y_std = LinearDistributionFunction._get_means_stdevs(x, y)
        mu = get_r_squared(x_, y_mean, self.mean_a, self.mean_b)
        sigma = get_r_squared(x_, y_std, self.stdev_a, self.stdev_b)
        return mu, sigma


class LogLinearDistributionFunction(LinearDistributionFunction):
    @classmethod
    def create_from_x_y_coordinates(cls, x, y, distribution_type: type(Distribution)=NormalDistribution):
        xx, yy = LogLinearDistributionFunction._remove_non_positive_values(x, y)
        x_, y_mean, y_std = LogLinearDistributionFunction._get_means_stdevs([ln(x_i) for x_i in xx],
                                                                            [y_i / xx[i] for i, y_i in enumerate(yy)])
        mean_a, mean_b = linear_regression(x_, y_mean)
        stdev_a, stdev_b = linear_regression(x_, y_std)
        return cls(mean_a, mean_b, stdev_a, stdev_b)

    def _get_mean_value(self, value):
        return super()._get_mean_value(ln(value))

    def _get_stdev_value(self, value):
        return super()._get_stdev_value(ln(value))

    def __getitem__(self, item: float) -> float:
        # we assume that if something has a value of 0 then it has an error of 0 as well
        if item <= 0:
            return item

        mean_x = self._get_mean_value(item)
        stdev_x = self._get_stdev_value(item)

        if mean_x > 1:
            print("for value: {0}".format(item))
            print("a: {0}".format(self.mean_a))
            print("b: {0}".format(self.mean_b))
            # raise ValueError("mean value of {0}".format(mean_x))
            print("mean: {0}".format(mean_x))
        if stdev_x > 1:
            print("for value: {0}".format(item))
            print("a: {0}".format(self.stdev_a))
            print("b: {0}".format(self.stdev_b))
            print("stdev: {0}".format(stdev_x))
            # raise ValueError("standard deviation value of {0}".format(stdev_x))

        if stdev_x < 0.01:
            stdev_x = 0.01
        d = self.distribution_type(mean_x, stdev_x)
        return d.get_observation()

    def __str__(self):
        return "\\mu = {0} \\text{{ln }} x + {1}, " \
               "\\sigma = {2} \\text{{ln }} x + {3}".format(self.mean_a, self.mean_b,
                                                            self.stdev_a, self.stdev_b)

    def get_mean_stdev_r_squared(self, x, y):
        return super().get_mean_stdev_r_squared([ln(x_i) for x_i in x], y)


class ExponentialDistributionFunction(DistributionFunction):
    @classmethod
    def _get_means_stdevs(cls, x, y):
        x_y_counter_lin = cls._convert_x_y_to_counter(x, y)
        x_y_counter = cls._convert_x_y_to_counter(x, [ln(y_i) for y_i in y])

        st_dev = {x: ln(stdev(y) if stdev(y) > 0 else 1 ** -10) for x, y in x_y_counter_lin.items()}
        mean_ = {x: mean(y) for x, y in x_y_counter.items()}
        return cls._get_mean_stdev_from_counter(x_y_counter, st_dev, mean_)

    @classmethod
    def create_from_x_y_coordinates(cls, x, y, distribution_type: type(Distribution)=NormalDistribution):
        x_, y_mean, y_std = ExponentialDistributionFunction._get_means_stdevs(x, [y_i / x[i]
                                                                                  for i, y_i in enumerate(y)
                                                                                  if y_i > 0])

        mean_a, mean_b = linear_regression(x_, y_mean)
        stdev_a, stdev_b = linear_regression(x_, y_std)

        # we currently have the form ln(y) = bx + ln(a), therefore mean_b becomes a, and exp(mean_a) becomes b
        return ExponentialDistributionFunction(mean_a=exp(mean_b),
                                               mean_b=mean_a,
                                               stdev_a=exp(stdev_b),
                                               stdev_b=stdev_a,
                                               distribution_type=distribution_type)

    def _get_mean_value(self, value):
        return self.mean_a * exp(self.mean_b * value)

    def _get_stdev_value(self, value):
        return self.stdev_a * exp(self.stdev_b * value)

    def __getitem__(self, item):
        if item == 0:
            return item

        mean_x = self._get_mean_value(exp(-item))
        stdev_x = self._get_stdev_value(exp(-item))

        d = self.distribution_type(mean_x, stdev_x)
        return d.get_observation()

    def __str__(self):
        return "\\mu = {0} \\text{{e}}^{{{1} x}}, " \
               "\\sigma  = {2} \\text{{e}}^{{{3} x}}".format(self.mean_a, self.mean_b,
                                                             self.stdev_a, self.stdev_b)

    def get_mean_stdev_r_squared(self, x, y):
        # remove all x,y's if y is less than or equal to 0
        yy, xx = ExponentialDistributionFunction._remove_non_positive_values(y, x)

        x_, y_mean, y_std = ExponentialDistributionFunction._get_means_stdevs(x, [y_i for y_i in yy])
        # these have to be of the form y = c x + d, therefore we use ln(y) = b x + ln(a)
        # which (in theory) is equivalent to y = a e^(bx)
        mu = get_r_squared(x_, y_mean, self.mean_b, ln(self.mean_a))
        sigma = get_r_squared(x_, y_std, self.stdev_b, ln(self.stdev_a))
        return mu, sigma
