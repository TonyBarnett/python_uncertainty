import numpy
import random
from math import log as ln

from uncertainty.source_uncertainty_distribution.uncertainty_functions import get_mean, get_standard_deviation


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
        return

    def get_pdf_line(self, x: list):
        pdf = [(numpy.exp(-(x_i - self.mu) ** 2 / (2 * self.sigma ** 2))
                / (x_i * self.sigma * numpy.sqrt(2 * numpy.pi))) for x_i in x]
        return pdf

    @classmethod
    def get_distribution_from_coordinate_list(cls, x: list):
        mu = get_mean(x)
        sigma = get_standard_deviation(x)
        return super(NormalDistribution, cls).get_distribution(mu, sigma)
