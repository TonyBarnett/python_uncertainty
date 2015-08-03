from collections import OrderedDict
import os

import pymongo

from .sql import read_from_sql, build_source_query, build_import_query
from .excel import _get_data_from_workbook, get_workbook


def get_map(map_collection: str='Plain_KNN_Without_Ancestors_k_3'):
    collection = pymongo.MongoClient('10.10.20.37').ClassificationMap[map_collection]
    mapping = dict()
    for map_ in collection.find():
        system = map_["_id"]["system"]
        value = map_["_id"]["value"]
        mapped_values = map_["map"]
        if system not in mapping:
            mapping[system] = dict()
        mapping[system][value] = mapped_values
    return mapping


def _build_consumption_query(region=None, year=None) -> str:
    query = "SELECT intYear, strRegion, strSystem, strSourceValue, strTargetValue, fltConsumption FROM sor.Consumption"
    return build_source_query(query, region, year)


def _build_production_query(region=None, year=None) -> str:
    query = "SELECT intYear, strRegion, strSystem, strSourceValue, strTargetValue, fltProduction FROM sor.production"
    return build_source_query(query, region, year)


def _build_emissions_query(region=None, year=None) -> str:
    query = "SELECT intYear, strRegion, strSystem, strValue, fltEmission FROM sor.Emission"
    return build_source_query(query, region, year)


def _build_imports_query(source_region=None, target_region=None, year=None) -> str:
    query = "SELECT intYear, strSourceRegion, strTargetRegion, strSystem, strSourceValue, strTargetValue, fltExport " \
            "FROM sor.Export"
    return build_import_query(query, source_region, target_region, year)


def _transpose_tuple(data: tuple) -> tuple:
    transposed = dict()
    for j, rows in enumerate(data):
        for i, value in enumerate(rows):
            if i not in transposed:
                transposed[i] = dict()
            transposed[i][j] = value

    output = list()
    for i in sorted(transposed.keys()):
        row = list()
        for j in sorted(transposed[i].keys()):
            row.append(transposed[i][j])
        output.append(tuple(row))
    return tuple(output)


def get_uk_supply(year) -> tuple:
    """

    :param year:
    :return: (data, row_totals, col_totals), where row and column totals are dicts
    """
    wb = get_workbook(os.environ["dropboxRoot"] +
                      "\\IO Model source data\\Source data\\Source data files\\UKSupply_source.xlsx")

    data = _get_data_from_workbook(wb, "sup{0}".format(str(year)[-2:]), "D8", "BO71")
    row_keys = _get_data_from_workbook(wb, "sup{0}".format(str(year)[-2:]), "B8", "B71")
    row_totals = _get_data_from_workbook(wb, "sup{0}".format(str(year)[-2:]), "BQ8", "BQ71")

    column_keys = _get_data_from_workbook(wb, "sup{0}".format(str(year)[-2:]), "D6", "BO6")
    col_totals = _get_data_from_workbook(wb, "sup{0}".format(str(year)[-2:]), "D73", "BO73")

    return _transpose_tuple(data), \
        OrderedDict(zip(column_keys, col_totals)), OrderedDict(zip(row_keys, row_totals)), \
        "SIC4"


def get_source_matrix_of_type(type_, region=None, year=None, target_region=None) -> tuple:
    if type_ == "consumption":
        return get_source_consumption(region, year)
    elif type_ == "production":
        return get_source_production(region, year)
    elif type_ == "emissions":
        return get_source_emissions(region, year)
    elif type_ == "import":
        return get_source_imports(region, target_region, year)
    else:
        raise ValueError("{0} type not recognised".format(type_))


def get_source_consumption(region=None, year=None) -> tuple:
    return read_from_sql(_build_consumption_query(region, year), db="IOModel")


def get_source_production(region=None, year=None) -> tuple:
    if region == "UK":
        return get_uk_supply(year)
    else:
        return read_from_sql(_build_production_query(region, year), db="IOModel")


def get_source_emissions(region=None, year=None) -> tuple:
    return read_from_sql(_build_emissions_query(region, year), db="IOModel")


def get_source_imports(source_region=None, target_region=None, year=None) -> tuple:
    return read_from_sql(_build_imports_query(source_region, target_region, year), db="IOModel")
