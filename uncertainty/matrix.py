from collections import OrderedDict


class Matrix:
    def __init__(self):
        self.row_keys = list()
        self.column_keys = list()
        # indexed by row_key, column_key
        self.elements = dict()

    def get_element(self, row_key, col_key):
        return self.elements[row_key][col_key]

    def _add_keys_to_row_column_lists(self, row_key, col_key):
        if row_key not in self.row_keys:
            self.row_keys.append(row_key)
            self.row_keys = list(sorted(self.row_keys))

        if col_key not in self.column_keys:
            self.column_keys.append(col_key)
            self.column_keys = list(sorted(self.column_keys))

    def set_element(self, row_key, col_key, value):
        if row_key not in self.row_keys:
            self.elements[row_key] = dict()
        self._add_keys_to_row_column_lists(row_key=row_key, col_key=col_key)

        self.elements[row_key][col_key] = value

    def get_row(self, row_key):
        return OrderedDict((x, self.elements[row_key][x]) for (x) in self.column_keys)

    def get_column(self, column_key):
        return OrderedDict(((x, self.elements[x][column_key]) for x in self.row_keys))


class Vector:
    def __init__(self):
        self.keys = list()
        self.elements = dict()

    def _add_key_to_keys(self, key):
        if key not in self.keys:
            self.keys.append(key)
            self.keys = list(sorted(self.keys))

    def get_element(self, key):
        self._add_key_to_keys()
        return self.elements[key]

    def set_element(self, key, value):
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
    for row_key in row_keys:
        for col_key in col_keys:
            m.set_element(row_key=row_key, col_key=col_key, value=0)


def create_matrix_from_list_of_tuple(db_values: list) -> Matrix:
    """

    :param db_values: list of tuples(row_key, col_key, value)
    :return:
    """
    m = Matrix()
    for row, col, value in db_values:
        m.set_element(row_key=row, col_key=col, value=value)

    return m
