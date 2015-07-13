from ..data_sources.model_data_sources import get_map
from run_uncertainty_model import EmissionsData, ImportData, MAPPED_DATA, SOURCE_DATA
from data_structures.data_structures import Data, ImportData, EmissionsData

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

    for key, total in totals.items():
        target.source_data.set_element(key, total)


def get_maps_from_list(source: list, system_id: str) -> dict:
    return {row_key: map_value(system_id, row_key) for row_key in source}


def get_map_len_from_map(map_: dict) -> dict:
    return {key: len(value) for key, value in map_.items()}


def get_maps_and_map_len_from_list(source: list, system_id: str) -> tuple:
    map_ = get_maps_from_list(source, system_id)
    map_len = get_map_len_from_map(map_)
    return (map_, map_len)


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
                        source.source_data.elements[row_key][col_key] / (row_map_len[row_key] * col_map_len[col_key])

    for row_key, columns in totals.items():
        for col_key, total in columns.items():
            target.source_data.set_element(row_key, col_key, total)


def map_imports_data(source: ImportData, target: ImportData):
    map_data(source, target)


def add_mapped_data_to_global(mapped_data):
        type_ = mapped_data.type_
        region = mapped_data.region
        if type_ not in MAPPED_DATA:
            MAPPED_DATA[type_] = dict()
        MAPPED_DATA[type_][region] = mapped_data


def map_source_data_matrix():
    for source_data_item in SOURCE_DATA:
        mapped_data = type(source_data_item).get_new_empty_source_data_item(source_data_item)
        add_mapped_data_to_global(mapped_data)

        if mapped_data.type_ == "emissions":
            map_emissions_data(source_data_item, mapped_data)
        elif mapped_data.type_ == "import":
            map_imports_data(source_data_item, mapped_data)
        else:
            map_data(source_data_item, mapped_data)
