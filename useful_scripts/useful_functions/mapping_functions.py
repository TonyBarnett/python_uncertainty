from uncertainty.source_uncertainty_distribution.uncertainty_functions import get_ancestors_and_self


def map_thing2_to_thing1_together(thing1: dict, thing2: dict) -> list:
    """
    thing1's keys must be ancestor or selfs of thing2's keys
    :param thing1:
    :param thing2:
    :return: list of tuples
    """
    x_y = list()
    error_key_map = {error_key: get_ancestors_and_self(error_key) for error_key in thing2.keys()}
    for error_key, error in thing2.items():
        for ancestor in error_key_map[error_key]:
            if ancestor in thing1.keys():
                x_y.append((thing1[ancestor], error))
    return sorted(x_y)
