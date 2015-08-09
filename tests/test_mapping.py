import unittest
from unittest.mock import patch
from uncertainty.data_mapping.map_data import get_maps_from_list

_map = {"SIC4": {"1": ["A"], "2": ["B"], "3": ["D", "C"], "4": ["C"]}}

class TestGetMapFromList(unittest.TestCase):
    def setUp(self):
        self.source = ["1", "2-3", "4"]
        self.target_map = {"1": ["A"], "2-3": ["B", "C", "D"], "4": ["C"]}

    def test_simple_case(self):
        with patch("uncertainty.data_mapping.map_data.map_.load") as mock_load:
            mock_load.return_value = _map
            m = get_maps_from_list(self.source, "SIC4")
            # self.assertDictEqual(m, self.target_map)

            for key, value in m.items():
                self.assertIn(key, self.target_map)
                self.assertListEqual(list(sorted(value)), list(sorted(self.target_map[key])))
