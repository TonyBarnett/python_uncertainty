from data_structures.data_structures import Data, ImportData, EmissionsData


def create_source_class(year: int, region: str, type_: str) -> Data:
    return Data(year, region, type_)


def create_import_source_class(year: int, source_region: str, target_region: str, type_: str) -> Data:
    return ImportData(year, source_region, target_region, type_)


def create_emission_source_class(year: int, region: str, type_: str) -> Data:
    return EmissionsData(year, region, type_)
