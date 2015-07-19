from collections import OrderedDict
import unittest
import numpy
from uncertainty.data_structures.populate import TotalsOnlyData, populate_totals_only_source_data
from mock import patch


class PopulateTotalsOnly(unittest.TestCase):
    def setUp(self):
        self.matrix = (1, 2, "c", 4)
        self.row_totals = OrderedDict((("1-2", 3), ("B", 7)))
        self.column_totals = OrderedDict((("1-2", 4), ("B", 6)))

    @patch("uncertainty.data_structures.populate.get_source_matrix_of_type")
    def test_simple_case(self, mock_get_source_matrix_type):
        mock_get_source_matrix_type.return_value = self.matrix, self.row_totals, self.column_totals, "don't care"

        blah = TotalsOnlyData(2008, "UK", "production", "don't care")
        populate_totals_only_source_data(blah)
        self.assertEqual(mock_get_source_matrix_type.call_count, 1)