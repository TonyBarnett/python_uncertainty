from .sql import _build_query, _read_from_sql


def get_classification_systems_data(system_id: str=None, value_id: str=None, used: bool=None):
    """ I'm sorry, this is really badly made but I can't be bothered to make it any better
    :param system_id:
    :param value_id:
    :param used:
    :return:
    """
    query = _build_query(system_id, value_id, used)
    class_sys_data = dict()
    for sys_id, val_id, description in _read_from_sql(query, tuple([system_id, value_id]), db="ClassificationSystems"):
        if sys_id not in class_sys_data:
            class_sys_data[sys_id] = dict()

        class_sys_data[sys_id][val_id] = description
    return class_sys_data