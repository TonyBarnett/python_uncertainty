from uncertainty.source_uncertainty_distribution.get_eu_consumption_uncertainty_distribution \
    import get_eu_consumption_uncertainty_distribution
from uncertainty.source_uncertainty_distribution.get_eu_supply_uncertainty_distribution \
    import get_eu_supply_uncertainty_distribution
from uncertainty.source_uncertainty_distribution.get_imports_uncertainty_distribution \
    import get_imports_uncertainty_distribution
from uncertainty.source_uncertainty_distribution.get_uk_supply_uncertainty_distribution \
    import get_uk_supply_uncertainty_distribution
from uncertainty.source_uncertainty_distribution.get_uk_consumption_uncertainty_distribution \
    import get_uk_consumption_uncertainty_distribution
from uncertainty.source_uncertainty_distribution.get_uk_emissions_uncertainty_distribution \
    import get_uk_emissions_distribution


_distribution_region_type_functions = {
    "consumption": {
        "EU": get_eu_consumption_uncertainty_distribution,
        "UK": get_uk_consumption_uncertainty_distribution
    },
    "production": {
        "EU": get_eu_supply_uncertainty_distribution,
        "UK": get_uk_supply_uncertainty_distribution
    },
    "emissions": {
        "EU": None,
        "UK": get_uk_emissions_distribution
    },
    "import":  {
        # Slight hack to get around the weird regioned imports thing
        None: get_imports_uncertainty_distribution
    },
}


def get_distribution_of_type_and_region(type_: str, region: str):
    return _distribution_region_type_functions[type_][region]()
