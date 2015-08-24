import unittest

from uncertainty.data_sources.excel import _get_excel_column_labels, _get_cell_in_range, _get_data_from_worksheet


class Cell:
    def __init__(self, value):
        self.value = value


class Worksheet:
    def __init__(self, cells: dict):
        self.values = {i: Cell(c) for i, c in cells.items()}

    def __getitem__(self, item):
        return self.values[item]


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
            _get_excel_column_labels("C", "A")

    def test_double_end_before_start(self):
        with self.assertRaises(ValueError):
            _get_excel_column_labels("AB", "AA")

    def test_int_range(self):
        with self.assertRaises(ValueError):
            _get_excel_column_labels("1", "4")

    def test_lower_case(self):
        result = _get_excel_column_labels("a", "c")
        self.assertListEqual(result, ["A", "B", "C"])

    def test_empty_strings(self):
        with self.assertRaises(ValueError):
            _get_excel_column_labels("", "")

    def test_none(self):
        with self.assertRaises(ValueError):
            _get_excel_column_labels("A", None)


class TestGetCellsInRange(unittest.TestCase):
    def setUp(self):
        self.start = "X8"
        self.end = "AB11"
        self.expected_output = ["X8", "X9", "X10", "X11",
                                "Y8", "Y9", "Y10", "Y11",
                                "Z8", "Z9", "Z10", "Z11",
                                "AA8", "AA9", "AA10", "AA11",
                                "AB8", "AB9", "AB10", "AB11"]

    def test_simple_case(self):
        r = _get_cell_in_range(self.start, self.end)
        self.assertListEqual([x for x in r], self.expected_output)

    def test_end_char_before_start(self):
        with self.assertRaises(ValueError):
            _get_cell_in_range(self.start, "W9")

    def test_end_int_before_start(self):
        with self.assertRaises(ValueError):
            _get_cell_in_range(self.start, "Z2")

    def test_end_int_and_char_before_start(self):
        with self.assertRaises(ValueError):
            _get_cell_in_range(self.start, "W2")

    def test_end_equals_start_cell(self):
        r = _get_cell_in_range(self.start, self.start)
        self.assertListEqual([x for x in r], [self.start])


class TestGetDataFromWorksheet(unittest.TestCase):
    def setUp(self):
        self.ws = Worksheet({j: i for i, j in enumerate(_get_cell_in_range("A1", "C5"))})

    def test_type(self):
        m = _get_data_from_worksheet(self.ws, "A1", "A2")
        self.assertIs(type(m), tuple)

    def test_simple_case(self):
        m = _get_data_from_worksheet(self.ws, "A2", "A5")
        self.assertTupleEqual(m, ("1", "2", "3", "4"))

    def test_two_columns(self):
        m = _get_data_from_worksheet(self.ws, "A1", "B2")
        self.assertTupleEqual(m, (("0", "5"), ("1", "6")))
