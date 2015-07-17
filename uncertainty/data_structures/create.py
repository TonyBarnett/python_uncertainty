from .data_structures import Data, ImportData, EmissionsData, TotalsOnlyData


def create_source_class(year: int, region: str, type_: str) -> Data:
    return Data(year, region, type_)


def create_import_source_class(year: int, source_region: str, target_region: str, type_: str) -> Data:
    return ImportData(year, source_region, target_region, type_)


def create_emission_source_class(year: int, region: str, type_: str) -> Data:
    return EmissionsData(year, region, type_)


def create_totals_only_source_class(year, region, type_):
    return TotalsOnlyData(year, region, type_)
