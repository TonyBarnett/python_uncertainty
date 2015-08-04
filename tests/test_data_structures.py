from collections import OrderedDict
import unittest
from unittest import mock
from unittest.mock import patch
import numpy
from uncertainty.data_structures.populate import TotalsOnlyDataSource, populate_totals_only_source_data
from uncertainty.matrix import Vector
from uncertainty.source_uncertainty_distribution.distribution import NormalDistribution
import uncertainty.source_uncertainty_distribution.distribution


class TotalsOnlyGetNewPerturbedMatrix(unittest.TestCase):
    def setUp(self):
        row_totals = OrderedDict((("1", 2), ("2", 5), ("3", 10)))
        column_totals = OrderedDict((("1", 1), ("2", 3), ("3", 5)))
        self.matrix = TotalsOnlyDataSource(2008, "UK", "production")
        self.matrix.add_data_from_tuple((
            ("1", "1", 1), ("1", "2", 2), ("1", "3", 1),
            ("2", "1", "c"), ("2", "2", 1), ("2", "3", "c"),
            ("3", "1", "c"), ("3", "2", "c"), ("3", "3", 2))
        )
        self.matrix.set_row_and_column_totals(row_totals, column_totals)
        self.matrix.distribution = NormalDistribution(0, 0)

    def _mock_observation(self):
        return 0

    # def test_rows_match_columns(self):
    #     with patch.object(NormalDistribution, "get_observation", return_value=0):
    #         # mock_observation.Distribution.get_observation = self._mock_observation
    #         new_row_totals, new_column_totals = self.matrix._get_new_totals_vector()
    #
    #         self.assertEqual(sum(x for x in new_row_totals.elements.A1), sum(x for x in new_column_totals.elements.A1))


class TotalsOnlyMakeVectorSumsEqual(unittest.TestCase):
    def setUp(self):
        self.vector1 = Vector([1, 2, 4])
        self.vector2 = Vector([3, 6, 12])

    def test_type(self):
        vector1, vector2 = TotalsOnlyDataSource._make_vector_sums_equal(self.vector1, self.vector2)
        self.assertIs(type(vector1), Vector)
        self.assertIs(type(vector2), Vector)

    def test_sums_match(self):
        vector1, vector2 = TotalsOnlyDataSource._make_vector_sums_equal(self.vector1, self.vector2)
        # Arbitrary number of places to get around floating point precision
        self.assertAlmostEqual(sum(x for x in vector1.elements.A1), sum(x for x in vector2.elements.A1), places=5)

    def test_different_length_vectors(self):
        self.vector2 = Vector([3, 6, 12, 18])
        vector1, vector2 = TotalsOnlyDataSource._make_vector_sums_equal(self.vector1, self.vector2)
        self.assertAlmostEqual(sum(x for x in vector1.elements.A1), sum(x for x in vector2.elements.A1), places=5)
