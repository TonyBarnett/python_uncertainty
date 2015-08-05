from uncertainty.source_uncertainty_distribution.get_eu_consumption_uncertainty_distribution \
    import get_eu_consumption_distribution_function
from uncertainty.source_uncertainty_distribution.get_eu_supply_uncertainty_distribution \
    import get_eu_supply_distribution_function
from uncertainty.source_uncertainty_distribution.get_imports_uncertainty_distribution \
    import get_imports_distribution_function
from uncertainty.source_uncertainty_distribution.get_uk_supply_uncertainty_distribution \
    import get_uk_supply_distribution_function
from uncertainty.source_uncertainty_distribution.get_uk_consumption_uncertainty_distribution \
    import get_uk_consumption_distribution_function
from uncertainty.source_uncertainty_distribution.get_uk_emissions_uncertainty_distribution \
    import get_uk_emissions_distribution_function

_distribution_region_type_functions = {
    "consumption": {
        "EU": get_eu_consumption_distribution_function,
        "UK": get_uk_consumption_distribution_function
    },
    "production": {
        "EU": get_eu_supply_distribution_function,
        "UK": get_uk_supply_distribution_function
    },
    "emissions": {
        "EU": None,
        "UK": get_uk_emissions_distribution_function
    },
    "import": {
        # Slight hack to get around the weird regioned imports thing
        None: get_imports_distribution_function
    },
}


def get_distribution_function_of_type_and_region(type_: str, region: str):
    return _distribution_region_type_functions[type_][region]()
