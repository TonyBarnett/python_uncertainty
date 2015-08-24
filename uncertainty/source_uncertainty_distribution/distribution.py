from numpy import std as stdev, mean
import numpy
import random
from math import log as ln, exp

from .uncertainty_functions import get_mean, get_standard_deviation, linear_regression


class Distribution:
    def __init__(self, mu: float, sigma: float):
        self.sigma = sigma
        self.mu = mu

    @classmethod
    def get_distribution(cls, mu, sigma):
        return cls(mu=mu, sigma=sigma)

    def get_observation(self):
        raise NotImplementedError()

    def get_pdf_line(self, x: list) -> list:
        raise NotImplementedError()


class NormalDistribution(Distribution):
    def __init__(self, mu, sigma):
        super().__init__(mu, sigma)

    def get_observation(self):
        return random.normalvariate(self.mu, self.sigma)

    def get_pdf_line(self, x: list):
        pdf = [(numpy.exp(-(x_i - self.mu) ** 2 / (2 * self.sigma ** 2))
                / (x_i * self.sigma * numpy.sqrt(2 * numpy.pi))) for x_i in x]
        return pdf

    @classmethod
    def get_distribution_from_coordinate_list(cls, x: list):
        mu = get_mean(x)
        sigma = get_standard_deviation(x)
        return super(NormalDistribution, cls).get_distribution(mu, sigma)


class LogNormalDistribution(Distribution):
    def __init__(self, mu, sigma):
        super().__init__(mu, sigma)

    def get_observation(self):
        return random.lognormvariate(self.mu, self.sigma)

    @classmethod
    def get_distribution_from_regression_coefficients(cls, a, b):
        """
        :param a:
        :param b:
        :return:
        """
        mu = 1
        sigma = 3
        return super(LogNormalDistribution, cls).get_distribution(mu, sigma)

    @classmethod
    def get_distribution_from_coordinate_list(cls, x: list):
        ln_x = [ln(x_i) for x_i in x]
        mu = get_mean(ln_x)
        sigma = get_standard_deviation(ln_x)
        return super(LogNormalDistribution, cls).get_distribution(mu, sigma)

    def get_pdf_line(self, x: list) -> list:
        pdf = [(numpy.exp(-(numpy.log(x_i) - self.mu) ** 2 / (2 * self.sigma ** 2))
                / (x_i * self.sigma * numpy.sqrt(2 * numpy.pi))) for x_i in x]
        return pdf


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
    def _get_mean_stdev_for_x(x_y_counter, st_dev, mean_):
        x_ = list()
        y_ = list()
        y_std = list()
        for t in x_y_counter.keys():
            x_.append(t)
            y_.append(mean_[t])
            y_std.append(st_dev[t])
        return x_, y_, y_std

    def _get_mean_value(self, item):
        raise NotImplementedError()

    def _get_stdev_value(self, item):
        raise NotImplementedError()


class LinearDistributionFunction(DistributionFunction):
    @classmethod
    def create_from_x_y_coordinates(cls, x, y, distribution_type: type(Distribution)=NormalDistribution):
        x_y_counter = LinearDistributionFunction._convert_x_y_to_counter(x, y)
        st_dev = {x: stdev(y) for x, y in x_y_counter.items()}
        mean_ = {x: mean(y) for x, y in x_y_counter.items()}
        x_, y_mean, y_std = LinearDistributionFunction._get_mean_stdev_for_x(x_y_counter, st_dev, mean_)
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


class LogLinearDistributionFunction(LinearDistributionFunction):
    @staticmethod
    def _remove_non_positive_values(x: list, y: list) -> tuple:
        xx = list()
        yy = list()
        for i, x_i in enumerate(x):
            if x_i > 0:
                xx.append(x_i)
                yy.append(y[i])
        return xx, yy

    @classmethod
    def create_from_x_y_coordinates(cls, x, y, distribution_type: type(Distribution)=NormalDistribution):
        # return super().create_from_x_y_coordinates(x, [y_i / x[i] for i, y_i in enumerate(y)])
        xx, yy = LogLinearDistributionFunction._remove_non_positive_values(x, y)
        return super().create_from_x_y_coordinates([ln(x_i) for x_i in xx],
                                                   [y_i / xx[i] for i, y_i in enumerate(yy)],
                                                   distribution_type)

    def __getitem__(self, item: float) -> float:
        # we assume that if something has a value of 0 then it has an error of 0 as well
        if item <= 0:
            return item
        mean_x = self._get_mean_value(ln(item))
        stdev_x = self._get_stdev_value(ln(item))
        # mean_x = self._get_mean_value(ln(item))
        # stdev_x = self._get_stdev_value(ln(item))

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


class ExponentialDistributionFunction(DistributionFunction):
    @classmethod
    def create_from_x_y_coordinates(cls, x, y, distribution_type: type(Distribution)=NormalDistribution):
        x_y_counter = ExponentialDistributionFunction._convert_x_y_to_counter(x, [ln(y_i) for y_i in y])
        st_dev = {x: stdev(y) for x, y in x_y_counter.items()}
        mean_ = {x: mean(y) for x, y in x_y_counter.items()}
        x_, y_mean, y_std = LinearDistributionFunction._get_mean_stdev_for_x(x_y_counter, st_dev, mean_)

        mean_a, mean_b = linear_regression(x_, y_mean)
        stdev_a, stdev_b = linear_regression(x_, y_std)

        # we currently have the form ln(y) = bx + ln(a), therefore b becomes a, and exp(a) becomes b
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
        if item <= 0:
            return item

        mean_x = self._get_mean_value(exp(-item))
        stdev_x = self._get_stdev_value(exp(-item))

        d = self.distribution_type(mean_x, stdev_x)
        return d.get_observation()
