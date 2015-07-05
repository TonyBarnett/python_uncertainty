class Matrix:
    def __init__(self):
        self.row_keys = list()
        self.column_keys = list()
        # indexed by row_key, column_key
        self.elements = dict()

    def get_element(self, row_key, col_key):
        return self.elements[row_key][col_key]

    def set_element(self, row_key, col_key, value):
        self.elements[row_key][col_key] = value


def create_matrix_keys_from_matrix(mat: Matrix) -> Matrix:
    new_matrix = Matrix()
    new_matrix.column_keys = mat.column_keys
    new_matrix.row_keys = mat.row_keys
    new_matrix.elements = {row: {column: 0 for column in new_matrix.column_keys} for row in new_matrix.row_keys}
    return new_matrix

def create_matrix_from_lists(row_keys, col_keys):