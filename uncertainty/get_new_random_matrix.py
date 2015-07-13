from uncertainty.matrix import Matrix, Vector


def get_perturbation_from_distribution(distribution) -> float:
    return distribution.get_observation()


def _get_log_normal_distribution(a, b):
    pass


def get_new_perturbed_vector(vec: Vector, distribution):
    data = list()
    for row_key in vec.keys:
        perturbed_value = vec[row_key] + get_perturbation_from_distribution(distribution)
        data.append((row_key, perturbed_value))

    perturbed_vector = Vector(tuple(data))
    return perturbed_vector


def get_new_perturbed_matrix(mat: Matrix, distribution) -> Matrix:
    # TODO add small value to each element in Matrix
    # work out logNormal distribution from y = a ln(x) + b,
    # then use it to add a random float to each element in Matrix
    values = list()
    for row_key in mat.row_keys:
        for column_key in mat.column_keys:
            perturbed_value = mat[(row_key, column_key)] + get_perturbation_from_distribution(distribution)
            values.append((row_key, column_key, perturbed_value))

    perturbed_matrix = Matrix.create_matrix_from_tuple(tuple(values))
    return perturbed_matrix
