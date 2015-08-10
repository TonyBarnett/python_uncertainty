import unittest
from unittest.mock import patch
import numpy
from uncertainty.data_mapping.map_data import get_maps_from_list, map_data
from uncertainty.data_structures import DataSource

_map = {"SIC4": {"1": ["5"], "2": ["6"], "3": ["7", "8"], "4": ["8"]}}


class TestGetMapFromList(unittest.TestCase):
    def setUp(self):
        self.source = ["1", "2-3", "4"]
        self.target_map = {"1": ["5"], "2-3": ["6", "8", "7"], "4": ["8"]}

    def test_simple_case(self):
        with patch("uncertainty.data_mapping.map_data.Map.load") as mock_load:
            mock_load.return_value = _map
            m = get_maps_from_list(self.source, "SIC4")
            # self.assertDictEqual(m, self.target_map)

            # FIXME assert that a dict of lists is equal properly.
            for key, value in m.items():
                self.assertIn(key, self.target_map)
                self.assertListEqual(list(sorted(value)), list(sorted(self.target_map[key])))


class TestMapData(unittest.TestCase):
    def setUp(self):
        self.source = DataSource(2008, "UK", "consumption")
        self.source.system = "SIC4"
        self.target = DataSource.get_new_empty_source_data_item(self.source)

    def test_simple_case(self):
        self.source.add_data_from_tuple((("1", "1", 1), ("1", "2-3", 7), ("1", "4", 4),
                                         ("2-3", "1", 2), ("2-3", "2-3", 8), ("2-3", "4", 8),
                                         ("4", "1", 3), ("4", "2-3", 9), ("4", "4", 4)
                                         ))
        expected_output = numpy.matrix([[1, 7 / 3, 7 / 3, 19 / 3],
                                        [2 / 3, 8 / 9, 8 / 9, 32 / 9],
                                        [2 / 3, 8 / 9, 8 / 9, 32 / 9],
                                        [11 / 3, 35 / 9, 35 / 9, 95 / 9]])

        with patch("uncertainty.data_mapping.map_data.Map.load") as mock_load:
            mock_load.return_value = _map

            with patch("uncertainty.data_mapping.map_data.get_dict_of_dict_of_censa123") as mock_censa123:
                mock_censa123.return_value = {str(a): {str(b): 0 for b in range(5, 9)} for a in range(5, 9)}

                map_data(self.source, self.target)
                for i in range(4):
                    for j in range(4):
                        self.assertAlmostEqual(self.target.source_data.elements[i, j], expected_output[i, j])

    def test_with_zeros(self):
        self.source.add_data_from_tuple((("1", "1", 1), ("1", "2-3", 7), ("1", "4", 0),
                                         ("2-3", "1", 6), ("2-3", "4", 0), ("2-3", "2-3", 8),
                                         ("4", "1", 3), ("4", "2-3", 9), ("4", "4", 4)
                                         ))

        expected_output = numpy.matrix([[1, 7 / 3, 7 / 3, 7 / 3],
                                        [2, 8 / 9, 8 / 9, 8 / 9],
                                        [2, 8 / 9, 8 / 9, 8 / 9],
                                        [5, 35 / 9, 35 / 9, 71 / 9]])

        with patch("uncertainty.data_mapping.map_data.Map.load") as mock_load:
            mock_load.return_value = _map

            with patch("uncertainty.data_mapping.map_data.get_dict_of_dict_of_censa123") as mock_censa123:
                mock_censa123.return_value = {str(a): {str(b): 0 for b in range(5, 9)} for a in range(5, 9)}

                map_data(self.source, self.target)
                for i in range(4):
                    for j in range(4):
                        self.assertAlmostEqual(self.target.source_data.elements[i, j], expected_output[i, j])
