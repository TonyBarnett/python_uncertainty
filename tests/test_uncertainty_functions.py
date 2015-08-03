import unittest
from uncertainty.data_sources.uncertainty_data_sources import _is_number, _clean_uk_supply_error_value
from uncertainty.source_uncertainty_distribution.uncertainty_functions import get_mean, get_ancestors_and_self


class Mean(unittest.TestCase):
    def test_type(self):
        m = get_mean([1])
        self.assertEqual(float, type(m))

    def test_simple_case(self):
        m = get_mean([1, 2, 3, 4, 5])
        self.assertEqual(3, m)

    def test_none(self):
        with self.assertRaises(TypeError):
            get_mean(None)


class GetAncestorsAndSelf(unittest.TestCase):
    def test_type(self):
        foo = get_ancestors_and_self("12")
        self.assertEqual(type(foo), list)

    def test_no_ancestors(self):
        foo = get_ancestors_and_self("1")
        self.assertListEqual(foo, ["1"])

    def test_numeric_ancestors(self):
        foo = get_ancestors_and_self("123")
        self.assertListEqual(foo, ["123", "12", "1"])

    def test_separator(self):
        foo = get_ancestors_and_self("1.2")
        self.assertListEqual(foo, ["1.2", "1"])

    def test_none_type(self):
        with self.assertRaises(TypeError):
            get_ancestors_and_self(None)

    def test_value_with_string(self):
        foo = get_ancestors_and_self("1.a.4")
        self.assertListEqual(foo, ["1.a.4", "1.a", "1"])

    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            get_ancestors_and_self(123)

    def test_underscore(self):
        foo = get_ancestors_and_self("22_11")
        self.assertListEqual(foo, ["22_11", "22_1", "22", "2"])


class IsNumber(unittest.TestCase):
    def test_type(self):
        is_it = _is_number("2")
        self.assertIs(type(is_it), bool)

    def test_simple_case(self):
        is_it = _is_number("1")
        self.assertTrue(is_it)

    def test_none(self):
        is_it = _is_number(None)
        self.assertFalse(is_it)

    def test_nan(self):
        is_it = _is_number("Not a number")
        self.assertFalse(is_it)

    def test_alphanum(self):
        is_it = _is_number("1 number")
        self.assertFalse(is_it)

    def test_zero(self):
        is_it = _is_number("0")
        self.assertTrue(is_it)

    def test_float(self):
        is_it = _is_number("0.12")
        self.assertTrue(is_it)

    def test_too_many_dots(self):
        is_it = _is_number("0.5.1")
        self.assertFalse(is_it)

    def test_underscored(self):
        is_it = _is_number("0_5")
        self.assertTrue(is_it)

    def test_too_many_underscores(self):
        is_it = _is_number("0_5_4")
        self.assertFalse(is_it)

    def test_mixed_dot_underscore(self):
        is_it = _is_number("0.5_1")
        self.assertFalse(is_it)


class CleanUkSupplErrorValue(unittest.TestCase):
    def test_number(self):
        is_it = _clean_uk_supply_error_value(0.5)
        self.assertEqual(is_it, 0.5)

    def test_star(self):
        is_it = _clean_uk_supply_error_value("*")
        self.assertEqual(is_it, 0)

    def test_confidential_value(self):
        is_it = _clean_uk_supply_error_value("-")
        self.assertEqual(is_it, "c")
