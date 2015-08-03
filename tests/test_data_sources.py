import unittest
from uncertainty.data_sources.model_data_sources import _transpose_tuple


class TransposeTuples(unittest.TestCase):
    def setUp(self):
        self.data = ((1, 2), (3, "c"))
        self.expected = ((1, 3), (2, "c"))

    def test_return_type(self):
        # assert we have a tuple of tuples, check that each row is a tuple
        x = _transpose_tuple(self.data)
        self.assertIs(type(x), tuple)
        for thing in x:
            self.assertIs(type(thing), tuple)

    def test_simple_case(self):
        x = _transpose_tuple(self.data)
        self.assertTrue(x == self.expected)
