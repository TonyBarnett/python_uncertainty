class Matrix:
    def __init__(self):
        self.row_keys = list()
        self.column_keys = list()
        # indexed by row_key, column_key
        self.elements = dict()

    def get_element(self, row_key, col_key):
        return self.elements[row_key][col_key]

    def set_element(self, row_key, col_key, value):
        if row_key not in self.elements:
            self.elements[row_key] = dict()
        self.elements[row_key][col_key] = value

    def get_row(self, row_key):
        return [x for x in self.elements[row_key]]

    def get_column(self, column_key):
        return {key: value
                for key, columns in self.elements.items()
                for col, value in columns.items()
                if col == column_key
                }


class Vector:
    def __init__(self):
        self.keys = list()
        self.elements = dict()

    def get_element(self, key):
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
