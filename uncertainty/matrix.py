from collections.abc import Iterable
from collections import OrderedDict

from numpy import matrix
import numpy


class MatrixVector:
    def __init__(self, data):
        self.row_keys = OrderedDict()
        self.column_keys = OrderedDict()
        self.elements = matrix(data)  # indexed by row_key, column_key

    @staticmethod
    def sort_list_alphabetically(unordered_list: Iterable) -> list:
        return [x for x in sorted(unordered_list)]

    @classmethod
    def get_new_matrix(cls, data):
        """
        :param data: (source_system, target_system, value)
        """
        return cls(data)

    def __get__(self, instance, owner):
        return instance.elements

    @classmethod
    def deep_copy(cls, m):
        """

        :param m: type(MatrixVector)
        :return:
        """
        m = cls(m.elements)
        m.row_keys = m.row_keys
        m.column_keys = m.column_keys
        return m

    @staticmethod
    def sum_matrices(a, b) -> numpy.matrix:
        try:
            return a + b
        except TypeError:
            x = list()

            for foo in range(a.shape[0]):
                y = list()
                x.append(y)
                for bar in range(a.shape[1]):
                    try:
                        y.append(a[(foo, bar)].astype(float) + b[(foo, bar)])
                    except ValueError:
                        y.append('c')
        return numpy.matrix(x)


class Matrix(MatrixVector):
    @staticmethod
    def get_row_col_list_from_tuple(data: tuple) -> tuple:
        rows = list()
        cols = list()
        for row, column, _ in data:
            rows.append(row)
            cols.append(column)

        rows = MatrixVector.sort_list_alphabetically(list(set(rows)))
        cols = MatrixVector.sort_list_alphabetically(list(set(cols)))
        return rows, cols

    @staticmethod
    def get_data_as_dict(data):
        data_dict = dict()
        for source_key, target_key, value in data:
            if source_key not in data_dict:
                data_dict[source_key] = dict()
            data_dict[source_key][target_key] = value
        return data_dict

    # TODO at some point, make this function follow SRP
    @classmethod
    def create_matrix_from_tuple(cls, data: tuple):
        """
        Make a Matrix from a tuple.
        The tuple is of the form (source_key, target_key, value)
        TODO:
            get data as a dict,
            get an ordered list of rows and columns,
            make a list of lists of data,
            make row and col key lookup,
            make new matrix, pass it the data, row lookup, and key lookup
        :param data (source_key, target_key, value)
        """
        data_dict = Matrix.get_data_as_dict(data)
        rows, columns = Matrix.get_row_col_list_from_tuple(data)

        row_keys = OrderedDict()
        col_keys = OrderedDict()

        mat = list()
        # make a list of lists of data,
        # make row and col key lookup,
        for row_counter, row_key in enumerate(rows):
            row_keys[row_key] = row_counter

            mat_row = list()

            for col_counter, col_key in enumerate(columns):
                col_keys[col_key] = col_counter
                if col_key in data_dict[row_key]:
                    mat_row.append(data_dict[row_key][col_key])
                else:
                    mat_row.append(0)
            mat.append(mat_row)

        matrix_ = cls.get_new_matrix(mat)
        matrix_.row_keys = row_keys
        matrix_.column_keys = col_keys
        return matrix_

    def __getitem__(self, item: tuple) -> float:
        """

        :param item: (row_key, col_key)
        :return:
        """
        (row_key, col_key) = item
        return self.elements[self.row_keys[row_key], self.column_keys[col_key]]


class Vector(MatrixVector):
    def __init__(self, data):
        super().__init__(data)
        self.keys = list()

    def _add_key_to_keys(self, key):
        if key not in self.keys:
            self.keys.append(key)
            self.keys = list(sorted(self.keys))

    @staticmethod
    def get_data_as_dict(data: tuple) -> dict:
        return {key: value for key, value in data}

    # TODO at some point, make this function follow SRP
    @classmethod
    def create_vector_from_tuple(cls, data: tuple):
        """
        :param data: (key, value)
        """
        data_as_dict = Vector.get_data_as_dict(data)
        keys = MatrixVector.sort_list_alphabetically([x[0] for x in data])

        col_keys = OrderedDict()

        data_as_list = list()

        for key_counter, key in enumerate(keys):
            col_keys[key] = key_counter
            data_as_list.append(data_as_dict[key])

        vec = super().get_new_matrix([data_as_list])
        vec.keys = col_keys
        return vec

    @classmethod
    def create_vector_from_dict(cls, data: dict):
        source_keys = MatrixVector.sort_list_alphabetically(data.keys())
        keys = OrderedDict()
        data_as_list = list()
        for key_counter, key in enumerate(source_keys):
            keys[key] = key_counter
            if data[key] == "c":
                data_as_list.append("c")
            else:
                data_as_list.append(float(data[key]))

        vec = super().get_new_matrix([data_as_list])
        vec.keys = keys
        return vec

    def __getitem__(self, key):
        # elements is a (1, n) matrix so is indexed (0, i)
        return self.elements[0, self.keys[key]]

    def __len__(self):
        return len(self.keys)


def create_matrix_from_lists(row_keys, col_keys):
    """

    :param row_keys:
    :param col_keys:
    :return:
    """
    data = tuple([(r, c, 0) for r in row_keys for c in col_keys])
    return Matrix.create_matrix_from_tuple(data)


def create_matrix_from_list_of_tuple(db_values: tuple) -> Matrix:
    """

    :param db_values: list of tuples(row_key, col_key, value)
    :return:
    """
    m = Matrix.create_matrix_from_tuple(db_values)

    return m
