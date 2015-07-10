import unittest
from uncertainty.source_uncertainty_distribution.uncertainty_functions import get_mean, get_ancestors_and_self


class Mean(unittest.TestCase):
    def test_type(self):
        m = get_mean([1])
        self.assertEqual(float, type(m))

    def test_simple_case(self):
        m = get_mean([1,2,3,4,5])
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
        self.assertListEqual(foo, ["123", "12", "1" ])

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