import unittest

from uncertainty.data_sources.excel import _get_excel_column_labels


class TestGetCharsInRange(unittest.TestCase):

    def test_simple_range(self):
        result = _get_excel_column_labels("A", "F")
        self.assertListEqual(result, ["A", "B", "C", "D", "E", "F"])

    def test_start_equals_end(self):
        result = _get_excel_column_labels("C", "C")
        self.assertListEqual(result, ["C"])

    def test_single_to_double_char_range(self):
        result = _get_excel_column_labels("Y", "AB")
        self.assertListEqual(result, ["Y", "Z", "AA", "AB"])

    def test_end_before_start(self):
        with self.assertRaises(ValueError):
            _get_excel_column_labels ("C", "A")

    def test_double_end_before_start(self):
        with self.assertRaises(ValueError):
            _get_excel_column_labels ("AB", "AA")

    def test_int_range(self):
        with self.assertRaises(ValueError):
            _get_excel_column_labels ("1", "4")

    def test_lower_case(self):
        result = _get_excel_column_labels("a", "c")
        self.assertListEqual(result, ["A", "B", "C"])

    def test_empty_strings(self):
        with self.assertRaises(ValueError):
            _get_excel_column_labels("", "")

    def test_none(self):
        with self.assertRaises(ValueError):
            _get_excel_column_labels("A", None)
