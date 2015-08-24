from collections import OrderedDict
import unittest

from uncertainty.data_structures import DataSource
from uncertainty.data_structures.populate import TotalsOnlyDataSource
from uncertainty.source_uncertainty_distribution.distribution import NormalDistribution


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


class BaseDataGetNewEmptySourceDataItem(unittest.TestCase):
    def setUp(self):
        self.source = DataSource(2008, "UK", "consumption")
        self.source.system = "SIC4"
        self.source.add_data_from_tuple((("1", "1", 1), ("1", "2-3", 7), ("1", "4", 4),
                                         ("2-3", "1", 2), ("2-3", "4", 8), ("2-3", "2-3", 8),
                                         ("4", "1", 3), ("4", "2-3", 9), ("4", "4", 4)
                                         ))

    def test_simple_case(self):
        target = DataSource.get_new_empty_source_data_item(self.source)
        self.assertEqual(target.type_, self.source.type_)
        self.assertEqual(target.region, self.source.region)
        self.assertEqual(target.system, self.source.system)
        self.assertEqual(target.year, self.source.year)
