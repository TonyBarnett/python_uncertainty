import numpy
from ..get_new_random_matrix import get_new_perturbed_matrix, get_new_perturbed_vector
from ..matrix import Matrix, Vector
from IOModel.matrix_balancing import ras, cras


class BaseData:
    def __init__(self, year, region, type_, system=None):
        self.year = year
        self.region = region
        self.distribution = None
        self.type_ = type_
        self.system = system

    def get_new_perturbed_matrix(self):
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
        self.source_data = None

    def input_data(self, raw_data: tuple) -> None:
        for _, _, _, source_value, target_value, value in raw_data:
            self.source_data.set_element(row_key=source_value, col_key=target_value, value=value)

    def get_new_perturbed_matrix(self):
        perturbed_data = Data(self.year, self.region, self.type_)
        perturbed_data.distribution = self.distribution
        perturbed_data.system = self.system
        perturbed_data.source_data = get_new_perturbed_matrix(self.source_data, self.distribution)
        return perturbed_data

    def __len__(self):
        return len(self.source_data.row_keys)

    def __getitem__(self, item: tuple) -> float:
        (row, column) = item
        return self.source_data[(row, column)]

    def __get__(self, instance, owner):
        return instance.perturbed_data

    def add_data_from_tuple(self, data):
        self.source_data = Matrix.create_matrix_from_tuple(data)


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
        self.source_data = None

    # OK this is named wrong but it makes things a lot easier to deal with and a vector is a 1D matrix anyway, right?!
    def get_new_perturbed_matrix(self):
        perturbed_data = EmissionsData(self.year, self.region, self.type_)
        perturbed_data.distribution = self.distribution
        perturbed_data.system = self.system
        perturbed_data.source_data = get_new_perturbed_vector(self.source_data, self.distribution)
        return perturbed_data

    def __len__(self):
        return len(self.source_data.keys)

    def __getitem__(self, item: tuple) -> float:
        return self.source_data[item]

    def __get__(self, instance, owner):
        return self.source_data

    def add_data_from_tuple(self, data):
        self.source_data = Vector.create_vector_from_tuple(data)


class TotalsOnlyData(BaseData):
    def __init__(self, year, region, type_, system=None):
        super().__init__(year, region, type_, system)
        self.row_totals = None
        self.column_totals = None
        self.constraints = dict()
        self.data_source = None

    def set_row_and_column_totals(self, row_totals: dict, column_totals: dict):
        self.row_totals = Vector.create_vector_from_dict(row_totals)
        self.column_totals = Vector.create_vector_from_dict(column_totals)

    def get_new_perturbed_matrix(self):
        """
        perturb the row and column totals, then use RAS to guess at a new matrix and return that
        :return:
        """
        perturbed_row_totals = get_new_perturbed_vector(self.row_totals, self.distribution)
        perturbed_column_totals = get_new_perturbed_vector(self.column_totals, self.distribution)
        # perturbed_row_totals = get_new_perturbed_vector(Vector.create_vector_from_dict(self.row_totals), self.distribution)
        # perturbed_column_totals = get_new_perturbed_vector(Vector.create_vector_from_dict(self.column_totals), self.distribution)
        perturbed_constraints = {key: float(value) + float(value) * self.distribution.get_observation()
                                 for key, value in self.constraints.items()}

        perturbed_data = Data(self.year, self.region, self.type_)
        perturbed_data.distribution = self.distribution
        perturbed_data.system = self.system
        perturbed_data.source_data = \
            Matrix.get_new_matrix(cras.run_cras(numpy.matrix(perturbed_row_totals.elements.A1).T,
                                                numpy.matrix(perturbed_column_totals.elements.A1).T,
                                                perturbed_constraints))
        perturbed_data.source_data.column_keys = self.column_totals.keys
        perturbed_data.source_data.row_keys = self.row_totals.keys
        return perturbed_data

    def set_constraints(self, constraints):
        self.constraints = constraints

    def add_data_from_tuple(self, data):
        self.source_data = Matrix.create_matrix_from_tuple(data)
