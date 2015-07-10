from ..data_sources.model_data_sources import get_map


_MAP = get_map(map_collection="Other_NB_Without_Ancestors_multinomial_10")


def map_value(system: str, value: str) -> list:
    return _MAP[system][value]
