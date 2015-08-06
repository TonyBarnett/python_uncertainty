from .create import create_emission_source_class, \
    create_import_source_class, \
    create_source_class, \
    create_totals_only_source_class


def get_data_source_of_type(year: int, region: str, type_: str, target_region: str=None):
    if type_ == "production" and region == "UK":
        return create_totals_only_source_class(year, region, type_)
    elif type_ == "emissions":
        return create_emission_source_class(year, region, type_)
    elif type_ == "import":
        return create_import_source_class(year, region, target_region, type_)
    else:
        return create_source_class(year, region, type_)
