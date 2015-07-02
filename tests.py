import unittest

from data_sources import _get_chars_in_range


class TestGetCharsInRange(unittest.TestCase):

    def test_simple_range(self):
        result = _get_chars_in_range("A", "F")
        self.assertListEqual(result, ["A", "B", "C", "D", "E", "F"])

    def test_start_equals_end(self):
        result = _get_chars_in_range("C", "C")
        self.assertListEqual(result, ["C"])

    def test_single_to_double_char_range(self):
        result = _get_chars_in_range("Y", "AB")
        self.assertListEqual(result, ["Y", "Z", "AA", "AB"])

    def test_end_before_start(self):
        result = _get_chars_in_range("C", "A")
        self.assertListEqual(result, [])

    def test_int_range(self):
        result = _get_chars_in_range("1", "4")
        self.assertListEqual(result, [])

    def test_lower_case(self):
        result = _get_chars_in_range("a", "c")
        self.assertListEqual(result, ["A", "B", "C"])

    def test_empty_strings(self):
        result = _get_chars_in_range("", "")
        self.assertListEqual(result, [])