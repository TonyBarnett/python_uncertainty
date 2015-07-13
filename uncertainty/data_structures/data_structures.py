from ..get_new_random_matrix import get_new_perturbed_matrix, get_new_perturbed_vector
from ..matrix import Matrix, Vector
from ..source_uncertainty_distribution.distribution import Distribution


class BaseData:
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
        :type source_data_item: BaseData
        :return:
        """
        return cls(source_data_item.year, source_data_item.region, source_data_item.type_)


class Data(BaseData):
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

    def __len__(self):
        return len(self.source_data.row_keys)

    def __getitem__(self, item: tuple) -> float:
        (row, column) = item
        return self.source_data.elements[row, column]

    def __get__(self, instance, owner):
        return instance.source_data.elements


class ImportData(Data):
    def __init__(self, year, source_region, target_region, type_):
        super().__init__(year, None, type_)
        self.source_region = source_region
        self.target_region = target_region

    @classmethod
    def get_new_empty_source_data_item(cls, source_data_item):
        """
        :param source_data_item:
        :type source_data_item: ImportData
        :return:
        """
        return cls(source_data_item.year,
                   source_data_item.source_region,
                   source_data_item.target_region,
                   source_data_item.type_)


class EmissionsData(BaseData):
    def __init__(self, year, region, type_):
        super().__init__(year, region, type_)
        self.source_data = Vector()
        self.perturbed_data = Vector()

    def add_item_to_data(self, key: str, value: float):
        self.source_data.set_element(key, value)

    # OK this is named wrong but it makes things a lot easier to deal with and a vector is a 1D matrix anyway, right?!
    def set_perturbed_matrix(self):
        self.perturbed_data = get_new_perturbed_vector(self.source_data, self.distribution)

    def __len__(self):
        return len(self.source_data.keys)

    def __getitem__(self, item: tuple) -> float:
        return self.source_data.elements[item]

    def __get__(self, instance, owner):
        return self.source_data.elements
