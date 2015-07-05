from uncertainty import matrix


def get_purturbation_from_distribution(distribution) -> float:
    pass

def _get_log_normal_distribution(a, b):
    pass


def get_new_perturbed_matrix(mat: matrix.Matrix, a: float, b: float) -> matrix.Matrix:
    # TODO add small value to each element in Matrix
    # work out logNormal distribution from y = a ln(x) + b,
    # then use it to add a random float to each element in Matrix
    distribution = _get_log_normal_distribution(a, b)
    purturbed_matrix = matrix.create_matrix_keys_from_matrix(mat)

    for row_key in mat.row_keys:
        for column_key in mat.column_keys:
            purturbed_matrix.set_element(row_key,
                                         column_key,
                                         mat.get_element(row_key,column_key) +
                                         get_purturbation_from_distribution(distribution)
                                         )
    return purturbed_matrix
