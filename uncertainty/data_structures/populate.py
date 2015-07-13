from data_sanitation import clean_value
from .data_structures import Data, ImportData, EmissionsData, BaseData
from ..data_sources.model_data_sources import get_source_matrix_of_type


def check_only_one_classification_system(system: list):
    if len(set(system)) != 1:
        raise ValueError("{0} systems in file where there should only be one".format(len(set(system))))


def populate_source_data(source_data_item: Data):
    data = get_source_matrix_of_type(source_data_item.type_, source_data_item.region, source_data_item.year)

    # this is horrible and hacky but it's the only way I can think of without increasing the number of db hits
    # check there's only one classification system per input table, then assign it to the source_data_item
    check_only_one_classification_system([x[2] for x in data])
    source_data_item.system = data[0][2]

    for _, _, system, source_value, target_value, total in data:
        clean_source_values = clean_value(system, source_value)
        clean_target_values = clean_value(system, target_value)

        split_total = total / (len(clean_target_values) + len(clean_source_values))

        for source in clean_source_values:
            for target in clean_target_values:
                source_data_item.add_item_to_data(source_key=source, target_key=target, value=split_total)


def populate_import_source_data(source_data_item: ImportData):
    data = get_source_matrix_of_type(source_data_item.type_,
                                     source_data_item.region,
                                     source_data_item.year,
                                     target_region=source_data_item.target_region
                                     )

    # this is horrible and hacky but it's the only way I can think of without increasing the number of db hits
    # check there's only one classification system per input table, then assign it to the source_data_item
    check_only_one_classification_system([x[3] for x in data])
    source_data_item.system = data[0][3]

    for _, _, _, system, source_value, target_value, total in data:
        clean_source_values = clean_value(system, source_value)
        clean_target_values = clean_value(system, target_value)

        split_total = total / (len(clean_target_values) + len(clean_source_values))

        for source in clean_source_values:
            for target in clean_target_values:
                source_data_item.add_item_to_data(source_key=source, target_key=target, value=split_total)


def populate_emissions_source_data(source_data_item: EmissionsData):
    data = get_source_matrix_of_type(source_data_item.type_,
                                     source_data_item.region,
                                     source_data_item.year
                                     )

    # this is horrible and hacky but it's the only way I can think of without increasing the number of db hits
    # check there's only one classification system per input table, then assign it to the source_data_item
    check_only_one_classification_system([x[2] for x in data])
    source_data_item.system = data[0][2]

    for _, _, system, value, total in data:
        clean_source_values = clean_value(system, value)

        split_total = total / len(clean_source_values)

        for source in clean_source_values:
            source_data_item.add_item_to_data(key=source, value=split_total)


def populate_source_data_of_type(source_data_item: BaseData):
    if source_data_item.type_ == "emissions":
        populate_emissions_source_data(source_data_item)
    elif source_data_item.type_ == "import":
        populate_import_source_data(source_data_item)
    else:
        populate_source_data(source_data_item)
