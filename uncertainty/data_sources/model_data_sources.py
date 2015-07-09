import pymongo
from .sql import _read_from_sql, _build_source_query


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
    return _build_source_query(query, region, year)


def _build_production_query(region=None, year=None) -> str:
    query = "SELECT intYear, strRegion, strSystem, strSourceValue, strTargetValue, fltProduction FROM sor.production"
    return _build_source_query(query, region, year)


def _build_emissions_query(region=None, year=None) -> str:
    query = "SELECT intYear, strRegion, strSystem, strValue, fltEmissions FROM sor.Emissions"
    return _build_source_query(query, region, year)


def get_source_consumption(region=None, year=None) -> dict():
    return _read_from_sql(_build_consumption_query(region, year), db="IOModel")


def get_source_production(region=None, year=None) -> dict():
    return _read_from_sql(_build_production_query(region, year), db="IOModel")


def get_source_emissions(region=None, year=None) -> dict():
    return _read_from_sql(_build_emissions_query(region, year), db="IOModel")