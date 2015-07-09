import unittest
from uncertainty.matrix import create_matrix_from_list_of_tuple, \
    create_matrix_from_lists,\
    create_matrix_keys_from_matrix, \
    Matrix


class CreateMatrixFromTupleList(unittest.TestCase):
    def test_type(self):
        m = create_matrix_from_list_of_tuple([("x", "y", 1),])
        self.assertEqual(type(m), Matrix)

    def test_simple_case(self):
        m = create_matrix_from_list_of_tuple([("x", "y", 1),])
        self.assertDictEqual(m.elements, {"x": {"y": 1}})

    def test_add_multiple_keys(self):
        m = create_matrix_from_list_of_tuple([("x", "y", 1), ("A", "B", 100)])
        self.assertDictEqual(m.elements, {"x": {"y": 1}, "A": {"B": 100}})

    def test_none_case(self):
        with self.assertRaises(TypeError):
            create_matrix_from_list_of_tuple(None)

    def test_bad_tuple(self):
        with self.assertRaises(ValueError):
            create_matrix_from_list_of_tuple([("too", "short"), ])

    def test_tuple_with_none(self):
        m = create_matrix_from_list_of_tuple([(None, "not_none", 1)])
        self.assertDictEqual(m.elements, {None: {"not_none": 1}})

    def test_non_string_keys(self):
        m = create_matrix_from_list_of_tuple([(1, 2, 3)])
        self.assertDictEqual(m.elements, {1: {2: 3}})