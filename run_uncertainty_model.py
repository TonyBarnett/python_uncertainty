import logging
from uncertainty.data_sources.model_data_sources import get_source_matrix_of_type
from uncertainty.source_uncertainty_distribution.distribution import Distribution
from uncertainty.matrix import Matrix, Vector
from uncertainty.get_new_random_matrix import get_new_perturbed_matrix, get_new_perturbed_vector
from uncertainty.source_uncertainty_distribution import get_distribution_of_type_and_region
from uncertainty.data_mapping.map_data import map_value

from data_sanitation import clean_value

INPUT_YEARS = (2008,)
INPUT_MATRICES = ("consumption", "production", "emissions")
INPUT_REGIONS = ("UK", "EU")
SOURCE_DATA = list()
MAPPED_DATA = list()
NUMBER_OF_ITERATIONS = 1
# NUMBER_OF_ITERATIONS = 10000


class SourceDataBase:
    def __init__(self, year, region, type_, system=None):
        self.year = year
        self.region = region
        self.distribution = None
        self.type_ = type_
        self.system = system

    def set_perturbed_matrix(self):
        raise NotImplementedError()

    @classmethod
    def get_new_empty_source_data_item(cls, source_data_item):
        """
        :param source_data_item:
        :type source_data_item: SourceDataBase
        :return:
        """
        return cls(source_data_item.year, source_data_item.region, source_data_item.type_)


class SourceData(SourceDataBase):
    def __init__(self, year, region, type_):
        super().__init__(year, region, type_)
        self.source_data = Matrix()
        self.perturbed_data = Matrix()

    def input_data(self, raw_data: tuple) -> None:
        for _, _, _, source_value, target_value, value in raw_data:
            self.source_data.set_element(row_key=source_value, col_key=target_value, value=value)

    def set_distribution(self, distribution: Distribution):
        self.distribution = distribution

    def add_item_to_data(self, source_key: str, target_key: str, value: float):
        self.source_data.set_element(row_key=source_key, col_key=target_key, value=value)

    def set_perturbed_matrix(self):
        self.perturbed_data = get_new_perturbed_matrix(self.source_data, self.distribution)


class ImportSourceData(SourceData):
    def __init__(self, year, source_region, target_region, type_):
        super().__init__(year, None, type_)
        self.source_region = source_region
        self.target_region = target_region

    @classmethod
    def get_new_empty_source_data_item(cls, source_data_item):
        """
        :param source_data_item:
        :type source_data_item: ImportSourceData
        :return:
        """
        return cls(source_data_item.year,
                   source_data_item.source_region,
                   source_data_item.target_region,
                   source_data_item.type_)


class EmissionsSourceData(SourceDataBase):
    def __init__(self, year, region, type_):
        super().__init__(year, region, type_)
        self.source_data = Vector()
        self.perturbed_data = Vector()

    def add_item_to_data(self, key: str, value: float):
        self.source_data.set_element(key, value)

    # OK this is named wrong but it makes things a lot easier to deal with and a vector is a 1D matrix anyway, right?!
    def set_perturbed_matrix(self):
        self.perturbed_data = get_new_perturbed_vector(self.source_data, self.distribution)


def create_source_class(year: int, region: str, type_: str) -> SourceData:
    return SourceData(year, region, type_)


def create_import_source_class(year: int, source_region: str, target_region: str, type_: str) -> SourceData:
    return ImportSourceData(year, source_region, target_region, type_)


def create_emission_source_class(year: int, region: str, type_: str) -> SourceData:
    return EmissionsSourceData(year, region, type_)


def get_data_source_of_type(year: int, region: str, type_: str, target_region: str=None):
    if type_ == "emissions":
        return create_emission_source_class(year, region, type_)
    elif type_ == "import":
        return create_import_source_class(year, region, target_region, type_)
    else:
        return create_source_class(year, region, type_)


def populate_source_data_of_type(source_data_item: SourceDataBase):
    if source_data_item.type_ == "emissions":
        populate_emissions_source_data(source_data_item)
    elif source_data_item.type_ == "import":
        populate_import_source_data(source_data_item)
    else:
        populate_source_data(source_data_item)


def check_only_one_classification_system(system: list):
    if len(set(system)) != 1:
        raise ValueError("{0} systems in file where there should only be one".format(len(set(system))))


def populate_source_data(source_data_item: SourceData):
    data = get_source_matrix_of_type(source_data_item.type_, source_data_item.region, source_data_item.year)

    # this is horrible and hacky but it's the only way I can think of without increasing the number of db hits
    # check there's only one classification system per input table, then assign it to the source_data_item
    check_only_one_classification_system([x[2] for x in data])
    source_data_item.system = data[0][2]

    for _, _, system, source_value, target_value, total in data:
        clean_source_values = clean_value(system, source_value)
        clean_target_values = clean_value(system, target_value)

        split_total = total / (len(clean_target_values) + len(clean_source_values))

        for source in clean_source_values:
            for target in clean_target_values:
                source_data_item.add_item_to_data(source_key=source, target_key=target, value=split_total)


def populate_import_source_data(source_data_item: ImportSourceData):
    data = get_source_matrix_of_type(source_data_item.type_,
                                     source_data_item.region,
                                     source_data_item.year,
                                     target_region=source_data_item.target_region
                                     )

    # this is horrible and hacky but it's the only way I can think of without increasing the number of db hits
    # check there's only one classification system per input table, then assign it to the source_data_item
    check_only_one_classification_system([x[3] for x in data])
    source_data_item.system = data[0][3]

    for _, _, _, system, source_value, target_value, total in data:
        clean_source_values = clean_value(system, source_value)
        clean_target_values = clean_value(system, target_value)

        split_total = total / (len(clean_target_values) + len(clean_source_values))

        for source in clean_source_values:
            for target in clean_target_values:
                source_data_item.add_item_to_data(source_key=source, target_key=target, value=split_total)


def populate_emissions_source_data(source_data_item: EmissionsSourceData):
    data = get_source_matrix_of_type(source_data_item.type_,
                                     source_data_item.region,
                                     source_data_item.year
                                     )

    # this is horrible and hacky but it's the only way I can think of without increasing the number of db hits
    # check there's only one classification system per input table, then assign it to the source_data_item
    check_only_one_classification_system([x[2] for x in data])
    source_data_item.system = data[0][2]

    for _, _, system, value, total in data:
        clean_source_values = clean_value(system, value)

        split_total = total / len(clean_source_values)

        for source in clean_source_values:
            source_data_item.add_item_to_data(key=source, value=split_total)


def create_and_populate_source_data(year) -> list:
    for region in INPUT_REGIONS:
        for type_ in INPUT_MATRICES:
            if not (type_ == "emissions" and region == "EU"):
                source_data_item = get_data_source_of_type(year=year, region=region, type_=type_)
                SOURCE_DATA.append(source_data_item)
                populate_source_data_of_type(source_data_item)
    # now do imports, we only care about EU importing into UK for now.
    source_data_item = get_data_source_of_type(year=year, region="EU", type_="import", target_region="UK")
    SOURCE_DATA.append(source_data_item)


def get_source_data_distribution():
    for source_data_item in SOURCE_DATA:
        source_data_item.distribution = get_distribution_of_type_and_region(type_=source_data_item.type_,
                                                                            region=source_data_item.region
                                                                            )


def perturb_source_data_matrix():
    for source_data_item in SOURCE_DATA:
        source_data_item.set_perturbed_matrix()


def map_emissions_data(source: EmissionsSourceData, target: EmissionsSourceData):
    # Hard-code Censa 123 values
    totals = {str(i): 0 for i in range(1, 124)}

    map_ = {key: map_value(source.system, key) for key in source.source_data.keys}
    map_length = {key: len(map_[key]) for key in source.source_data.keys}

    for key in source.source_data.keys:
        for target in map_[key]:
            totals[target] += source.source_data.get_element(key) / map_length[key]

    for key, total in totals.items():
        target.source_data.set_element(key, total)


def get_maps_from_list(source: list, system_id: str) -> dict:
    return {row_key: map_value(system_id, row_key) for row_key in source}


def get_map_len_from_map(map_: dict) -> dict:
    return {key: len(value) for key, value in map_.items()}


def get_maps_and_map_len_from_list(source: list, system_id: str) -> tuple:
    map_ = get_maps_from_list(source, system_id)
    map_len = get_map_len_from_map(map_)
    return (map_, map_len)


def map_data(source: SourceData, target: SourceData):

    # Hard-code Censa 123 values
    totals = {str(i): {str(j): 0 for j in range(1, 124)} for i in range(1, 124)}

    row_map = get_maps_from_list(source.source_data.row_keys, source.system)
    row_map_len = get_map_len_from_map(row_map)

    col_map = get_maps_from_list(source.source_data.column_keys, source.system)
    col_map_len = get_map_len_from_map(col_map)

    # this probably needs tidying, row_map[key] is a list, as is col_map[key] so loop over each of these lists and
    # assign totals, split the totals row_map_len[key] * col_map_len[key] times
    for row_key in source.source_data.row_keys:
        for col_key in source.source_data.column_keys:
            for row_target in row_map[row_key]:
                for col_target in col_map[col_key]:
                    totals[row_target][col_target] += \
                        source.source_data.elements[row_key][col_key] / (row_map_len[row_key] * col_map_len[col_key])

    for row_key, columns in totals.items():
        for col_key, total in columns.items():
            target.source_data.set_element(row_key, col_key, total)


def map_imports_data(source: ImportSourceData, target: ImportSourceData):
    map_data(source, target)


def map_source_data_matrix():
    for source_data_item in SOURCE_DATA:
        type_ = source_data_item.type_
        mapped_data = type(source_data_item).get_new_empty_source_data_item(source_data_item)
        MAPPED_DATA.append(mapped_data)

        if type_ == "emissions":
            map_emissions_data(source_data_item, mapped_data)
        elif type_ == "import":
            map_imports_data(source_data_item, mapped_data)
        else:
            map_data(source_data_item, mapped_data)


def run_single_region_model() -> list:
    pass


def run_two_region_model() -> list:
    pass


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s - %(asctime)-15s', level=logging.DEBUG)

    # TODO get all error distributions, get all source files, spit out new source files
    # each input matrix will be a (year, region, matrix, distribution) tuple

    # TODO do stuff for emissions, do stuff for imports, do the generic stuff
    # populate a SourceData
    # add data to the SourceData
    # get a distribution for that SourceData
    # for a large number of iterations
    #   for each data_type
    #     make a new perturbed matrix
    #     map the perturbed matrix
    #   run two cf models

    for input_year in INPUT_YEARS:
        logging.debug("year: {0}".format(input_year))

        logging.debug("creating and populating matrices")
        create_and_populate_source_data(input_year)

        logging.debug("getting distributions")
        get_source_data_distribution()

        logging.debug("running Monte Carlo...")
        for _ in range(NUMBER_OF_ITERATIONS):
            perturb_source_data_matrix()
            map_source_data_matrix()
            run_single_region_model()
            # run_two_region_model(year)

    logging.debug("finished")
