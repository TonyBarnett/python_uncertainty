from collections import OrderedDict
from numpy import ndarray
from numpy.matrixlib import matrix


class MatrixVector:
    def __init__(self, data):
        self.row_keys = OrderedDict()
        self.column_keys = OrderedDict()
        self.elements = matrix(data)  # indexed by row_key, column_key

    @staticmethod
    def sort_list_alphabetically(unordered_list: list) -> list:
        return [x for x in sorted(unordered_list)]

    @classmethod
    def get_new_matrix(cls, data):
        """
        :param data: (source_system, target_system, value)
        """
        return cls(data)

    def __get__(self, instance, owner):
        return instance.elements


class Matrix(MatrixVector):
    def __init__(self, data):
        super().__init__(data)

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

        row_counter = 0

        row_keys = OrderedDict()
        col_keys = OrderedDict()

        mat = list()
        # make a list of lists of data,
        # make row and col key lookup,
        for row_key in rows:
            col_counter = 0
            row_keys[row_key] = row_counter

            mat_row = list()

            for col_key in columns:
                col_keys[col_key] = col_counter
                if col_key in data_dict[row_key]:
                    mat_row.append(data_dict[row_key][col_key])
                else:
                    mat_row.append(0)
                col_counter += 1
            mat.append(mat_row)
            row_counter += 1

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

        key_counter = 0
        for key in keys:
            col_keys[key] = key_counter
            data_as_list.append(data_as_dict[key])
            key_counter += 1

        super().get_new_matrix([data_as_list])

    def __getitem__(self, key):
        return self.elements[key]


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
