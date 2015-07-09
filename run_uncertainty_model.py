from uncertainty.data_sources import model_data_sources
from uncertainty.distribution import Distribution
from uncertainty.matrix import Matrix
from uncertainty.get_new_random_matrix import get_new_perturbed_matrix

from data_sanitation import clean_value


INPUT_YEARS = (2008, )
INPUT_MATRICES = ("consumption", "production", "emissions", "import")
INPUT_REGIONS = ("UK", "EU")


class SourceData:
    def __init__(self, year, region, type_):
        self.year = year
        self.region = region
        self.data = Matrix()
        self.distribution = None
        self.type_ = type_

    def input_data(self, raw_data: tuple) -> None:
        for _, _, _, source_value, target_value, value in raw_data:
            self.data.set_element(row_key=source_value, col_key=target_value, value=value)

    def set_distribution(self, distribution: Distribution):
        self.distribution = distribution

    def get_new_perturbed_matrix(self) -> Matrix:
        return get_new_perturbed_matrix(self.data, self.distribution)

    def add_item_to_data(self, source_key: str, target_key: str, value: float):
        self.data.set_element(row_key=source_key, col_key=target_key, value=value)


if __name__ == '__main__':
    # TODO get all error distributions, get all source files, spit out new source files
    # each input matrix will be a (year, region, matrix, distribution) tuple

    source_data = list()

    # consumption
    for region in INPUT_REGIONS:
        for year in INPUT_YEARS:
            for type_ in INPUT_MATRICES:
                data_item = SourceData(year, region, type_)
                source_data.append(data_item)
                raw_data = model_data_sources.get_source_matrix_of_type(type_, region=region, year=year)

                for rd in raw_data:
                    sys = rd[2]
                    source_value = rd[3]
                    if type_ != "emissions":

                        target_value = rd[4]
                        value = rd[5]
                        target_vals = clean_value(sys, target_value)

                    else:
                        value = rd[4]
                    source_vals = clean_value(sys, source_value)

                    len_multiplier = len(source_vals) + len(target_vals)

                    for source_val in source_vals:
                        for target_val in target_vals:
                            data_item.add_item_to_data(source_val, target_val, value)
    print(1)
