import unittest

import numpy
from numpy.matrixlib import matrix

from uncertainty.matrix import create_matrix_from_list_of_tuple, \
    Matrix


# import numpy.testing


class CreateMatrixFromTupleList(unittest.TestCase):
    def test_type(self):
        m = create_matrix_from_list_of_tuple((("x", "y", 1),))
        self.assertEqual(type(m), Matrix)

    def test_simple_case(self):
        m = create_matrix_from_list_of_tuple((("x", "y", 1),))
        self.assertDictEqual(m.row_keys, {"x": 0})
        self.assertDictEqual(m.column_keys, {"y": 0})
        self.assertTrue((m.elements == [[1]]).all())

    def test_add_multiple_keys(self):
        m = create_matrix_from_list_of_tuple((("x", "A", 1), ("y", "B", 100)))
        self.assertDictEqual(m.column_keys, {"A": 0, "B": 1})
        self.assertDictEqual(m.row_keys, {"x": 0, "y": 1})
        self.assertTrue((m.elements == matrix([[1, 0], [0, 100]])).all())

    def test_tuple_with_none(self):
        m = create_matrix_from_list_of_tuple(((None, "not_none", 1),))
        self.assertDictEqual(m.row_keys, {None: 0})
        self.assertDictEqual(m.column_keys, {"not_none": 0})
        self.assertTrue((m.elements == [[1]]).all())

    def test_non_string_keys(self):
        m = create_matrix_from_list_of_tuple(((1, 2, 3),))
        self.assertDictEqual(m.row_keys, {1: 0})
        self.assertDictEqual(m.column_keys, {2: 0})
        self.assertTrue((m.elements == [[3]]).all())

    def test_two_dimensional_matrix(self):
        m = create_matrix_from_list_of_tuple((("B", "x", 2), ("A", "x", 1), ("A", "y", 5), ("B", "y", 4)))
        self.assertDictEqual(m.row_keys, {"A": 0, "B": 1})
        self.assertDictEqual(m.column_keys, {"x": 0, "y": 1})
        self.assertTrue((m.elements == [[1, 5], [2, 4]]).all())

    def test_none_case(self):
        with self.assertRaises(TypeError):
            create_matrix_from_list_of_tuple(None)

    def test_bad_tuple(self):
        with self.assertRaises(ValueError):
            create_matrix_from_list_of_tuple((("too", "short"),))


class MatrixGet(unittest.TestCase):
    def _setup_matrix(self):
        return create_matrix_from_list_of_tuple((("B", "x", 2), ("A", "x", 1), ("A", "y", 5), ("B", "y", 4)))

    def test_type(self):
        m = self._setup_matrix()
        self.assertEqual(type(m[("A", "y")]), numpy.int32)

    def test_simple_get(self):
        m = self._setup_matrix()
        self.assertEqual(m[("A", "y")], 5)

    def test_missing_column_label(self):
        m = self._setup_matrix()
        with self.assertRaises(ValueError):
            m[("A",)]

    def test_wrong_keys(self):
        m = self._setup_matrix()
        with self.assertRaises(KeyError):
            m[("C", "z")]
