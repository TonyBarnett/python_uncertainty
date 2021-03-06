from .matrix import Matrix, Vector
from uncertainty.source_uncertainty_distribution.distribution_function import DistributionFunction


def get_perturbation_from_distribution(distribution: DistributionFunction, value) -> float:
    return distribution[value]


def get_perturbed_value(value: float, perturbation: float) -> float:
    return value + (perturbation * value)


def get_new_perturbed_vector(vec: Vector, distribution):
    data = list()
    for row_key in vec.keys:
        if vec[row_key]:
            perturbation = get_perturbation_from_distribution(distribution, vec[row_key])
        elif vec[row_key] == 0:
            perturbation = 0
        else:
            raise ValueError("Element shouldn't be null.")
        perturbed_value = get_perturbed_value(vec[row_key], perturbation)
        data.append((row_key, perturbed_value))

    perturbed_vector = Vector.create_vector_from_tuple(tuple(data))
    return perturbed_vector


def get_new_perturbed_matrix(mat: Matrix, distribution) -> Matrix:
    # TODO add small value to each element in Matrix
    # work out logNormal distribution from y = a ln(x) + b,
    # then use it to add a random float to each element in Matrix
    values = list()
    for row_key in mat.row_keys:
        for column_key in mat.column_keys:
            if mat[(row_key, column_key)]:
                perturbation = get_perturbation_from_distribution(distribution, mat[(row_key, column_key)])
            elif mat[(row_key, column_key)] == 0:
                perturbation = 0
            else:
                raise ValueError("Element shouldn't be null.")
            if perturbation < -1:
                print("mean (in theory) is {0} ln(x) + {1}".format(distribution.mean_a, distribution.mean_b))
                print("stdev (in theory) is {0} ln(x) + {1}".format(distribution.stdev_a, distribution.stdev_b))
                raise ValueError("for {0}, {1}, value: {2}, perturbation was {3}".format(
                    row_key, column_key, mat[(row_key, column_key)], perturbation
                ))
            perturbed_value = get_perturbed_value(mat[(row_key, column_key)], perturbation)
            values.append((row_key, column_key, perturbed_value))

    perturbed_matrix = Matrix.create_matrix_from_tuple(tuple(values))
    return perturbed_matrix
