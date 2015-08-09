import unittest
from unittest.mock import patch

from uncertainty.source_uncertainty_distribution.distribution import Distribution, LogNormalDistribution, \
    NormalDistributionFunction, LogNormalDistributionFunction


class FactoryTest(unittest.TestCase):
    def test_create(self):
        m = LogNormalDistribution.get_distribution(1, 2)
        self.assertEqual(type(m), LogNormalDistribution)

    def test_create_from_regression_coefficients_type(self):
        m = LogNormalDistribution.get_distribution_from_regression_coefficients(1, 2)
        self.assertEqual(type(m), LogNormalDistribution)

    def test_observation_type(self):
        m = LogNormalDistribution(1, 2)
        observation = m.get_observation()
        self.assertEqual(type(observation), float)

    def test_observation(self):
        m = LogNormalDistribution(0.1, 0.1)
        observation = m.get_observation()
        self.assertAlmostEqual(observation, 1, places=0)

    def test_base_observation_error(self):
        m = Distribution(1, 1)
        with self.assertRaises(NotImplementedError):
            m.get_observation()


class NormalFunctionFactoryTest(unittest.TestCase):
    def setUp(self):
        self.x = [1, 1, 2]
        self.y = [3, 5, 6]

    def test_type(self):
        m = NormalDistributionFunction.create_from_x_y_coordinates(self.x, self.y)
        self.assertIs(type(m), NormalDistributionFunction)

    def test_simple_case(self):
        with patch("uncertainty.source_uncertainty_distribution.distribution.linear_regression", return_value=(1, 2)) \
                as mock_linear_regression:
            m = NormalDistributionFunction.create_from_x_y_coordinates(self.x, self.y)
            self.assertTrue(mock_linear_regression.called)
            self.assertEqual(m.mean_a, 1)
            self.assertEqual(m.mean_b, 2)
            self.assertEqual(m.stdev_a, 1)
            self.assertEqual(m.stdev_b, 2)

    def test_linear_regression(self):
        m = NormalDistributionFunction.create_from_x_y_coordinates(self.x, self.y)

        self.assertAlmostEqual(m.mean_a, 2)
        self.assertAlmostEqual(m.mean_b, 2)
        self.assertAlmostEqual(m.stdev_a, -1)
        self.assertAlmostEqual(m.stdev_b, 2)


class LogNormalFunctionFactorTest(unittest.TestCase):
    def setUp(self):
        self.x = [1, 1, 2]
        self.y = [3, 5, 6]

    def test_linear_regression(self):
        m = LogNormalDistributionFunction.create_from_x_y_coordinates(self.x, self.y)

        self.assertAlmostEqual(m.mean_a, 2.8853, places=3)
        self.assertAlmostEqual(m.mean_b, 4, places=3)
        self.assertAlmostEqual(m.stdev_a, -1.4427, places=3)
        self.assertAlmostEqual(m.stdev_b, 1, places=3)


class XYCounterNormalDistributionFunction(unittest.TestCase):
    def setUp(self):
        self.x = [0, 0, 1, 1, 1, 2, 2, 3, 4]
        self.y = [20, 20, 1, 2, 3, 10, 20, 9, 0]

    def test_type(self):
        m = NormalDistributionFunction._convert_x_y_to_counter(self.x, self.y)
        self.assertIs(type(m), dict)

    def test_simple_case(self):
        m = NormalDistributionFunction._convert_x_y_to_counter(self.x, self.y)
        self.assertDictEqual(m, {1: [2, 3, 4], 2: [6, 11], 3: [4], 4: [1]})


class NormalFunctionTest(unittest.TestCase):
    def setUp(self):
        self.distribution_function = NormalDistributionFunction(2, 2, -1, 2)

    def test_simple_case(self):
        with patch("random.normalvariate") as mock_normalvariate:
            _ = self.distribution_function[1]
            mock_normalvariate.assert_called_with(4, 1)


class LogNormalFunctionTest(unittest.TestCase):
    def setUp(self):
        self.distribution_function = LogNormalDistributionFunction(2.8853, 4, -1.4427, 1)

    def test_simple_case(self):
        with patch("random.normalvariate") as mock_normalvariate:
            _ = self.distribution_function[1]
            mock_normalvariate.assert_called_with(4, 1)
