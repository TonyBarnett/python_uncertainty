import unittest
from mock import patch
from uncertainty.get_new_random_matrix import get_new_perturbed_matrix, get_new_perturbed_vector
from uncertainty.matrix import Matrix, create_matrix_from_list_of_tuple, Vector
from uncertainty.source_uncertainty_distribution.distribution import NormalDistribution


class PerturbMatrix(unittest.TestCase):
    def setUp(self):
        self.matrix = create_matrix_from_list_of_tuple((("1", "1", 1),
                                                        ("2", "2", 2),
                                                        ("1", "2", 3),
                                                        ("2", "1", 4)))

        self.output_matrix = create_matrix_from_list_of_tuple((("1", "1", 2),
                                                               ("2", "2", 4),
                                                               ("1", "2", 6),
                                                               ("2", "1", 8)))
        self.distribution = NormalDistribution(1, 1)

    def test_type(self):
        m = get_new_perturbed_matrix(self.matrix, self.distribution)
        self.assertIs(type(m), Matrix)

    @patch("uncertainty.get_new_random_matrix.get_perturbation_from_distribution")
    def test_simple_case(self, mock_get_perturbation_from_distribution):
        mock_get_perturbation_from_distribution.return_value = 1
        m = get_new_perturbed_matrix(self.matrix, self.distribution)
        self.assertTrue((m.elements == self.output_matrix.elements).all())


class PerturbVector(unittest.TestCase):
    def setUp(self):
        self.matrix = Vector.create_vector_from_tuple((("1", 1),
                                                      ("2", 2.2),
                                                      ("3", 4.5)))

        self.output_matrix = Vector.create_vector_from_tuple((("1", 2),
                                                              ("2", 4.4),
                                                              ("3", 9)))
        self.distribution = NormalDistribution(1, 1)

    def test_type(self):
        m = get_new_perturbed_vector(self.matrix, self.distribution)
        self.assertIs(type(m), Vector)

    @patch("uncertainty.get_new_random_matrix.get_perturbation_from_distribution")
    def test_simple_case(self, mock_get_perturbation_from_distribution):
        mock_get_perturbation_from_distribution.return_value = 1
        m = get_new_perturbed_vector(self.matrix, self.distribution)
        self.assertTrue((m.elements == self.output_matrix.elements).all())
