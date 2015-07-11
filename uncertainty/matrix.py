from collections import OrderedDict
from numpy.matrixlib import matrix

class Matrix:
    def __init__(self):
        self.row_keys = list()
        self.column_keys = list()
        # indexed by row_key, column_key
        self.elements = Vector()

    @staticmethod
    def _add_key_to_list_and_sort(key_list: list, key: str):
        key_list.append(key)
        key_list = list(sorted(key_list))

    def _add_keys_to_row_column_lists(self, row_key, col_key):
        if row_key not in self.row_keys:
            self._add_key_to_list_and_sort(self.row_keys, row_key)
        if col_key not in self.column_keys:
            self._add_key_to_list_and_sort(self.column_keys, col_key)

    def __setitem__(self, row_key, col_key, value):
        if row_key not in self.row_keys:
            self.elements[row_key] = Vector()
        self._add_keys_to_row_column_lists(row_key=row_key, col_key=col_key)
        self.elements[row_key][col_key] = value

    def __getitem__(self, row_key, col_key):
        return self.elements[row_key][col_key]


class Vector:
    def __init__(self):
        self.keys = list()
        self.elements = dict()

    def _add_key_to_keys(self, key):
        if key not in self.keys:
            self.keys.append(key)
            self.keys = list(sorted(self.keys))

    def __getitem__(self, key):
        return self.elements[key]

    def __setitem__(self, key, value):
        self._add_key_to_keys(key)
        self.elements[key] = value


def create_matrix_keys_from_matrix(mat: Matrix) -> Matrix:
    new_matrix = Matrix()
    new_matrix.column_keys = mat.column_keys
    new_matrix.row_keys = mat.row_keys
    new_matrix.elements = {row: {column: 0 for column in new_matrix.column_keys} for row in new_matrix.row_keys}
    return new_matrix


def create_matrix_from_lists(row_keys, col_keys):
    """

    :param row_keys:
    :param col_keys:
    :return:
    """
    m = Matrix()
    for row in row_keys:
        for col in col_keys:
            m[row][col] = 0


def create_matrix_from_list_of_tuple(db_values: list) -> Matrix:
    """

    :param db_values: list of tuples(row_key, col_key, value)
    :return:
    """
    m = Matrix()
    for row, col, value in db_values:
        m[row, col] = value

    return m
