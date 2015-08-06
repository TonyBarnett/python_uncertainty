from . import DataSource, ImportDataSource, EmissionsDataSource, TotalsOnlyDataSource


def create_source_class(year: int, region: str, type_: str) -> DataSource:
    return DataSource(year, region, type_)


def create_import_source_class(year: int, source_region: str, target_region: str, type_: str) -> DataSource:
    return ImportDataSource(year, source_region, target_region, type_)


def create_emission_source_class(year: int, region: str, type_: str) -> DataSource:
    return EmissionsDataSource(year, region, type_)


def create_totals_only_source_class(year, region, type_):
    return TotalsOnlyDataSource(year, region, type_)
