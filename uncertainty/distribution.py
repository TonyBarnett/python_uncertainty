import random

from .source_uncertainty.uncertainty_functions import get_mean, get_standard_deviation


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
    def get_distribution_from_coordinate_lists(cls, x: list, y: list):
        mu = get_mean(y)
        sigma = get_standard_deviation(y)
        return super(LogNormalDistribution, cls).get_distribution(mu, sigma)

    def get_pdf_line(self, x: list) -> list:
        pass


class NormalDistribution(Distribution):
    def __init__(self, mu, sigma):
        super().__init__(mu, sigma)

    def get_observation(self):
        return

    def get_pdf_line(self, x: list):
        pass

    @classmethod
    def get_distribution_from_coordinate_lists(cls, x: list, y: list):
        pass
