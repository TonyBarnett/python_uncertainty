from ..data_sources.model_data_sources import get_map
from ..data_structures.data_structures import Data, EmissionsData, ImportData

_MAP = get_map(map_collection="Other_NB_Without_Ancestors_multinomial_10")


def map_value(system: str, value: str) -> list:
    return _MAP[system][value]


def map_emissions_data(source: EmissionsData, target: EmissionsData):
    # Hard-code Censa 123 values
    totals = {str(i): 0 for i in range(1, 124)}

    map_ = {key: map_value(source.system, key) for key in source.source_data.keys}
    map_length = {key: len(map_[key]) for key in source.source_data.keys}

    for key in source.source_data.keys:
        for target in map_[key]:
            totals[target] += source.source_data.get_element(key) / map_length[key]
    data = [(key, total) for key, total in totals.items()]
    target.add_data_from_tuple(data)


def get_maps_from_list(source: list, system_id: str) -> dict:
    return {row_key: map_value(system_id, row_key) for row_key in source}


def get_map_len_from_map(map_: dict) -> dict:
    return {key: len(value) for key, value in map_.items()}


def get_maps_and_map_len_from_list(source: list, system_id: str) -> tuple:
    map_ = get_maps_from_list(source, system_id)
    map_len = get_map_len_from_map(map_)
    return map_, map_len


def map_data(source: Data, target: Data):

    # Hard-code Censa 123 values
    totals = {str(i): {str(j): 0 for j in range(1, 124)} for i in range(1, 124)}

    row_map = get_maps_from_list(source.source_data.row_keys, source.system)
    row_map_len = get_map_len_from_map(row_map)

    col_map = get_maps_from_list(source.source_data.column_keys, source.system)
    col_map_len = get_map_len_from_map(col_map)

    # this probably needs tidying, row_map[key] is a list, as is col_map[key] so loop over each of these lists and
    # assign totals, split the totals row_map_len[key] * col_map_len[key] times
    for row_key in source.source_data.row_keys:
        for col_key in source.source_data.column_keys:
            for row_target in row_map[row_key]:
                for col_target in col_map[col_key]:
                    totals[row_target][col_target] += \
                        source[(row_key, col_key)] / (row_map_len[row_key] * col_map_len[col_key])

    data = [(row_key, col_key, total) for row_key, columns in totals.items() for col_key, total in columns.items()]
    target.add_data_from_tuple(data)


def map_imports_data(source: ImportData, target: ImportData):
    map_data(source, target)


def add_item_to_mapped_data(data, mapped_data):
    """
    Add data to mapped_data.
    :param data:
    :param mapped_data:
    :return:
    """
    type_ = data.type_
    region = data.region
    if type_ not in mapped_data:
        mapped_data[type_] = dict()
    mapped_data[type_][region] = data


def map_data_of_type(source_data_item, mapped):
    """
    Determine which type of item source_data_item is, then map it
    :param source_data_item:
    :param mapped:
    :return:
    """
    if mapped.type_ == "emissions":
        map_emissions_data(source_data_item, mapped)
    elif mapped.type_ == "import":
        map_imports_data(source_data_item, mapped)
    else:
        map_data(source_data_item, mapped)


def map_source_data_matrix(source_data: list):
    mapped_data = dict()
    for source_data_item in source_data:
        mapped = type(source_data_item).get_new_empty_source_data_item(source_data_item)
        map_data_of_type(source_data_item, mapped)
        add_item_to_mapped_data(mapped, mapped_data)
    return mapped_data
