from numpy import std as stdev, mean
import numpy
import random
from math import log as ln

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


class DistributionFunction:
    def __init__(self, mean_a: float=None, mean_b: float=None, stdev_a: float=None, stdev_b: float=None):
        self.mean_a = mean_a
        self.mean_b = mean_b
        self.stdev_a = stdev_a
        self.stdev_b = stdev_b

    def __getitem__(self, item):
        raise NotImplementedError()


class NormalDistributionFunction(DistributionFunction):
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

    @classmethod
    def create_from_x_y_coordinates(cls, x, y):
        x_y_counter = NormalDistributionFunction._convert_x_y_to_counter(x, y)
        st_dev = {x: stdev(y) for x, y in x_y_counter.items()}
        mean_ = {x: mean(y) for x, y in x_y_counter.items()}
        x_, y_mean, y_std = NormalDistributionFunction._get_mean_stdev_for_x(x_y_counter, st_dev, mean_)
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
        d = NormalDistribution(mean_x, stdev_x)
        return d.get_observation()


class LogNormalDistributionFunction(NormalDistributionFunction):
    @classmethod
    def create_from_x_y_coordinates(cls, x, y):
        return super().create_from_x_y_coordinates([ln(x_i) for x_i in x], y)

    def __getitem__(self, item: float) -> float:
        # we assume that if something has a value of 0 then it has an error of 0 as well
        if item <= 0:
            return item
        return super().__getitem__(ln(item))
