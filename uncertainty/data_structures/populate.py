from utility_functions.data_sanitation import _is_number


def check_only_one_classification_system(system: list):
    if len(set(system)) != 1:
        raise ValueError("{0} systems in file where there should exactly be one".format(len(set(system))))


def make_constraints(data) -> dict:
    """
    for each known cell, make a constraint such that cell(row_index, col_index) == total
    :param data:
    :return:
    """
    conditions = dict()
    for row_index, row_data in enumerate(data):
        for col_index, value in enumerate(row_data):
            if value and _is_number(value):
                conditions[(row_index, col_index)] = value
    return conditions
