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
        "eu": get_eu_consumption_uncertainty_distribution,
        "uk": get_uk_consumption_uncertainty_distribution
    },
    "production": {
        "eu": get_eu_supply_uncertainty_distribution,
        "uk": get_uk_supply_uncertainty_distribution
    },
    "emissions": {
        "eu": None,
        "uk": get_uk_emissions_distribution
    },
    "import":  get_imports_uncertainty_distribution,
}


def get_distribution_of_type_and_region(type_: str, region: str):
    return _distribution_region_type_functions[type_][region]()
