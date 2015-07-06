from mock import patch
import unittest
from uncertainty.distribution import Distribution, LogNormalDistribution


class FactoryTest(unittest.TestCase):
    def test_create(self):
        m = LogNormalDistribution.get_distribution(1, 2)
        self.assertEqual(type(m), LogNormalDistribution)

    def test_create_from_regression_coefficients_type(self):
        m = LogNormalDistribution.get_distribution_from_regression_coefficients(1, 2)
        self.assertEqual(type(m), LogNormalDistribution)

    def test_obeservation_type(self):
        m = LogNormalDistribution(1, 2)
        observation = m.get_observation()
        self.assertEqual(type(observation), float)

    def test_observation(self):
        m = LogNormalDistribution(0.1, 0.1)
        observation = m.get_observation()
        self.assertAlmostEqual(observation, 1, places=0)
