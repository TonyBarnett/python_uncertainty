from uncertainty.matrix import Matrix, Vector


def get_perturbation_from_distribution(distribution) -> float:
    return distribution.get_observation()


def _get_log_normal_distribution(a, b):
    pass


def get_new_perturbed_vector(vec: Vector, distribution):
    perturbed_vector = Vector()

    for row_key in vec.keys:
        perturbed_value = vec[row_key] + get_perturbation_from_distribution(distribution)
        perturbed_vector[row_key] = perturbed_value

    return perturbed_vector


def get_new_perturbed_matrix(mat: Matrix, distribution) -> Matrix:
    # TODO add small value to each element in Matrix
    # work out logNormal distribution from y = a ln(x) + b,
    # then use it to add a random float to each element in Matrix
    perturbed_matrix = Matrix()

    for row_key in mat.row_keys:
        for column_key in mat.column_keys:
            perturbed_value = mat.get_element(row_key, column_key) + get_perturbation_from_distribution(distribution)
            perturbed_matrix.set_element(row_key=row_key, col_key=column_key, value=perturbed_value)
    return perturbed_matrix
