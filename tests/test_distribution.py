import unittest
from unittest.mock import patch, call

from uncertainty.source_uncertainty_distribution.distribution import Distribution, LogNormalDistribution, \
    NormalDistributionFunction, LogNormalDistributionFunction, ExponentialDistributionFunction
from math import log as ln, exp


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
        self.x = [1, 1, 1, 2, 2, 2, 4, 4, 5]
        self.y = [3, 5, 6, 4, 0, 5, 10, 1, 2]

    def test_linear_regression(self):
        m = LogNormalDistributionFunction.create_from_x_y_coordinates(self.x, self.y)
        # y is converted to y_i/x_i \forall i \in y
        self.assertAlmostEqual(m.mean_a, -0.35207701, places=3)
        self.assertAlmostEqual(m.mean_b, 4.25277049, places=3)
        self.assertAlmostEqual(m.stdev_a, -1.4427, places=3)
        self.assertAlmostEqual(m.stdev_b, 1, places=3)


class ExponentialFunctionFactoryTest(unittest.TestCase):
    def setUp(self):
        self.x = [1, 1, 1, 2, 2, 2, 4, 4, 5]
        self.y = [3, 5, 6, 4, 5, 5, 10, 1, 2]

    def test_type(self):
        dist = ExponentialDistributionFunction.create_from_x_y_coordinates(self.x, self.y)
        self.assertIs(type(dist), ExponentialDistributionFunction)

    def test_simple_case(self):
        """
        A horrible example, but c'est la vie, the y values are supposed to be logged (hence the horrible numbers)
        :return:
        """
        with patch("uncertainty.source_uncertainty_distribution.distribution.linear_regression", return_value=(1, 2)) \
                as mock_linear_regression:
            ExponentialDistributionFunction.create_from_x_y_coordinates(self.x, self.y)
            calls = [call([1, 2, 4, 5], [1.499936556776755, 1.535056728662697, 1.151292546497023, 0.6931471805599453]),
                     call([1, 2, 4, 5], [0.29337821283302279, 0.10519087887488401, 1.151292546497023, 0.0])]
            self.assertIs(mock_linear_regression.call_count, 2)
            mock_linear_regression.assert_has_calls(calls=calls, any_order=False)


class XYCounterNormalDistributionFunction(unittest.TestCase):
    def setUp(self):
        self.x = [0, 0, 1, 1, 1, 2, 2, 3, 4]
        self.y = [20, 20, 1, 2, 3, 10, 20, 9, 0]
        self.expected_result = {0: [20, 20], 1: [1, 2, 3], 2: [10, 20], 3: [9], 4: [0]}

    def test_type(self):
        m = NormalDistributionFunction._convert_x_y_to_counter(self.x, self.y)
        self.assertIs(type(m), dict)

    def test_simple_case(self):
        m = NormalDistributionFunction._convert_x_y_to_counter(self.x, self.y)
        # self.assertDictEqual(m, {1: [2, 3, 4], 2: [6, 11], 3: [4], 4: [1]})
        self.assertDictEqual(m, self.expected_result)


class NormalFunctionTest(unittest.TestCase):
    def setUp(self):
        self.distribution_function = NormalDistributionFunction(2, 2, -1, 2)

    def test_simple_case(self):
        with patch("random.normalvariate") as mock_normalvariate:
            _ = self.distribution_function[1]
            mock_normalvariate.assert_called_with(4, 1)


class LogNormalFunctionTest(unittest.TestCase):
    def setUp(self):
        self.distribution_function = LogNormalDistributionFunction(-0.00370761, 0.04383424,
                                                                   -0.0029355627894458156, 0.0350757971517967)
        self.input_value = 2132

    def test_simple_case(self):
        self.distribution_function = LogNormalDistributionFunction(1, 2, 3, 4)
        with patch("random.normalvariate") as mock_normalvariate:
            _ = self.distribution_function[1]
            mock_normalvariate.assert_called_with(2, 4)

    def test_get_mean(self):
        m = self.distribution_function._get_mean_value(ln(self.input_value))
        self.assertAlmostEqual(m, 0.015115, 3)

    def test_get_stdev(self):
        m = self.distribution_function._get_stdev_value(ln(self.input_value))
        self.assertAlmostEqual(m, 0.012337315, 3)
