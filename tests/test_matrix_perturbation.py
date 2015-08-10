import unittest
from unittest.mock import patch
from uncertainty.get_new_random_matrix import get_new_perturbed_matrix, get_new_perturbed_vector
from uncertainty.matrix import Matrix, create_matrix_from_list_of_tuple, Vector
from uncertainty.source_uncertainty_distribution.distribution import NormalDistribution, NormalDistributionFunction


class PerturbMatrix(unittest.TestCase):
    def setUp(self):
        self.matrix = create_matrix_from_list_of_tuple((("1", "1", 1),
                                                        ("2", "2", 2),
                                                        ("1", "2", 3),
                                                        ("2", "1", 4)))

        self.output_matrix = create_matrix_from_list_of_tuple((("1", "1", 2),
                                                               ("2", "2", 3),
                                                               ("1", "2", 4),
                                                               ("2", "1", 5)))
        self.distribution = NormalDistributionFunction(1, 1, 1, 1)

    def test_type(self):
        m = get_new_perturbed_matrix(self.matrix, self.distribution)
        self.assertIs(type(m), Matrix)

    def test_simple_case(self):
        with patch("uncertainty.get_new_random_matrix.get_perturbation_from_distribution", return_value=1) as \
                mock_get_perturbation_from_distribution:
            m = get_new_perturbed_matrix(self.matrix, self.distribution)
            self.assertTrue((m.elements == self.output_matrix.elements).all())

    def test_matrix_contains_zero(self):
        with patch("uncertainty.get_new_random_matrix.get_perturbation_from_distribution", return_value=1) as \
                mock_get_perturbation_from_distribution:
            self.matrix = create_matrix_from_list_of_tuple((("1", "1", 1),
                                                            ("2", "2", 0),
                                                            ("1", "2", 3),
                                                            ("2", "1", 4)))

            self.output_matrix = create_matrix_from_list_of_tuple((("1", "1", 2),
                                                                   ("2", "2", 0),
                                                                   ("1", "2", 4),
                                                                   ("2", "1", 5)))

            m = get_new_perturbed_matrix(self.matrix, self.distribution)

            self.assertTrue((m.elements == self.output_matrix.elements).all())


class PerturbVector(unittest.TestCase):
    def setUp(self):
        self.matrix = Vector.create_vector_from_tuple((("1", 1),
                                                       ("2", 2.2),
                                                       ("3", 4.5)))

        self.output_matrix = Vector.create_vector_from_tuple((("1", 2),
                                                              ("2", 3.2),
                                                              ("3", 5.5)))
        self.distribution = NormalDistributionFunction(1, 1, 1, 1)

    def test_type(self):
        m = get_new_perturbed_vector(self.matrix, self.distribution)
        self.assertIs(type(m), Vector)

    def test_simple_case(self):
        with patch("uncertainty.get_new_random_matrix.get_perturbation_from_distribution", return_value=1) as \
                mock_get_perturbation_from_distribution:
            m = get_new_perturbed_vector(self.matrix, self.distribution)
            self.assertTrue((m.elements == self.output_matrix.elements).all())
