import unittest

from uncertainty.plot_builder import sort_axes_by_x


class AxesSorting(unittest.TestCase):
    def test_no_rearrange(self):
        x = [1, 2]
        y = [3, 6]
        a, b = sort_axes_by_x(x, y)
        self.assertListEqual(a, x, msg="a and x do not match")
        self.assertListEqual(b, y, msg="b and y do not match")

    def test_simple_rearrange(self):
        x = [6, 2]
        y = [3, 6]
        a, b = sort_axes_by_x(x, y)
        self.assertListEqual(a, [2, 6], msg="a and x do not match")
        self.assertListEqual(b, [6, 3], msg="b and y do not match")

    def test_inconsistent_lengths(self):
        x=[1, 3, 2]
        y=[4, 5]
        a, b = sort_axes_by_x(x, y)
        self.assertListEqual(a, [1, 2, 3], msg="a and x do not match")
        self.assertListEqual(b, [4, 5], msg="b and y do not match")

    # decide whether this is an error or not.
    def test_strings(self):
        x = "hello!"
        y = "badstr"
        a, b = sort_axes_by_x(x, y)
        self.assertListEqual(a, ["!", "e", "h", "l", "l", "o"], msg="a and x do not match")
        self.assertListEqual(b, ["r", "a", "b", "d", "s", "t"], msg="b and y do not match")

    def test_nones(self):
        with self.assertRaises(TypeError):
            sort_axes_by_x(None, None)
