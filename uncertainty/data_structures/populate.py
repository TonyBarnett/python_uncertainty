from utility_functions.data_sanitation import clean_value
from .data_structures import Data, ImportData, EmissionsData, BaseData, TotalsOnlyData
from ..data_sources.model_data_sources import get_source_matrix_of_type
from utility_functions.data_sanitation import _is_number


def check_only_one_classification_system(system: list):
    if len(set(system)) != 1:
        raise ValueError("{0} systems in file where there should exactly be one".format(len(set(system))))


def populate_source_data(source_data_item: Data):
    source_data = get_source_matrix_of_type(source_data_item.type_, source_data_item.region, source_data_item.year)

    # this is horrible and hacky but it's the only way I can think of without increasing the number of db hits
    # check there's only one classification system per input table, then assign it to the source_data_item
    check_only_one_classification_system([x[2] for x in source_data])
    source_data_item.system = source_data[0][2]
    data = list()
    for _, _, system, source_value, target_value, total in source_data:
        clean_source_values = clean_value(system, source_value)
        clean_target_values = clean_value(system, target_value)

        split_total = total / (len(clean_target_values) * len(clean_source_values))
        for source in clean_source_values:
            for target in clean_target_values:
                data.append((source, target, split_total))
    source_data_item.add_data_from_tuple(tuple(data))


def populate_import_source_data(source_data_item: ImportData):
    source_data = get_source_matrix_of_type(source_data_item.type_,
                                            source_data_item.region,
                                            source_data_item.year,
                                            target_region=source_data_item.target_region
                                            )

    # this is horrible and hacky but it's the only way I can think of without increasing the number of db hits
    # check there's only one classification system per input table, then assign it to the source_data_item
    check_only_one_classification_system([x[3] for x in source_data])
    source_data_item.system = source_data[0][3]
    data = list()
    for _, _, _, system, source_value, target_value, total in source_data:
        clean_source_values = clean_value(system, source_value)
        clean_target_values = clean_value(system, target_value)

        split_total = total / (len(clean_target_values) + len(clean_source_values))
        for source in clean_source_values:
            for target in clean_target_values:
                data.append((source, target, split_total))
    source_data_item.add_data_from_tuple(tuple(data))


def populate_emissions_source_data(source_data_item: EmissionsData):
    source_data = get_source_matrix_of_type(source_data_item.type_,
                                            source_data_item.region,
                                            source_data_item.year
                                            )

    # this is horrible and hacky but it's the only way I can think of without increasing the number of db hits
    # check there's only one classification system per input table, then assign it to the source_data_item
    check_only_one_classification_system([x[2] for x in source_data])
    source_data_item.system = source_data[0][2]
    data = list()
    for _, _, system, value, total in source_data:
        clean_source_values = clean_value(system, value)

        split_total = total / len(clean_source_values)

        for source in clean_source_values:
            data.append((source, split_total))
    source_data_item.add_data_from_tuple(data)


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


def populate_totals_only_source_data(source_data_item: TotalsOnlyData):
    data, row_totals, column_totals = get_source_matrix_of_type(source_data_item.type_,
                                                                source_data_item.region,
                                                                source_data_item.year)
    constraints = make_constraints(data)
    source_data_item.set_row_and_column_totals(row_totals, column_totals)
    source_data_item.set_constraints(constraints)


def populate_source_data_of_type(source_data_item: BaseData):
    if source_data_item.type_ == "production" and source_data_item.region == "UK":
        populate_totals_only_source_data(source_data_item)
    elif source_data_item.type_ == "emissions":
        populate_emissions_source_data(source_data_item)
    elif source_data_item.type_ == "import":
        populate_import_source_data(source_data_item)
    else:
        populate_source_data(source_data_item)
