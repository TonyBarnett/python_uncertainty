import random


class Distribution:
    def __init__(self, mu: float, sigma: float):
        self.sigma = sigma
        self.mu = mu

    @classmethod
    def get_distribution(cls, mu, sigma):
        return cls(sigma=1, mu=1)

    def get_observation(self):
        raise NotImplementedError()


class LogNormalDistribution(Distribution):
    def __init__(self, mu, sigma):
        super().__init__(mu, sigma)

    # @classmethod
    # def get_distribution(cls ,mu, sigma):
    #     distribution = super(LogNormalDistribution, cls).get_distribution(mu, sigma)
    #     return distribution

    def get_observation(self):
        random.lognormvariate(self.mu, self.sigma)

    @classmethod
    def get_distribution_from_regression_coefficients(cls, a, b):
        """
        :param a:
        :param b:
        :return:
        """
        mu = 1
        sigma = 3
        distribution = super(LogNormalDistribution, cls).get_distribution(mu, sigma)
        return distribution
