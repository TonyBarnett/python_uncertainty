import pymongo
from .sql import read_from_sql, build_source_query, build_import_query


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
    return read_from_sql(_build_production_query(region, year), db="IOModel")


def get_source_emissions(region=None, year=None) -> tuple:
    return read_from_sql(_build_emissions_query(region, year), db="IOModel")


def get_source_imports(source_region=None, target_region=None, year=None) -> tuple:
    return read_from_sql(_build_imports_query(source_region, target_region, year), db="IOModel")
