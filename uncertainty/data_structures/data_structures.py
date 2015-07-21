import numpy
from ..get_new_random_matrix import get_new_perturbed_matrix, get_new_perturbed_vector
from ..matrix import Matrix, Vector
from IOModel.matrix_balancing import ras, cras


class BaseDataSource:
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
        :type source_data_item: BaseDataSource
        :return:
        """
        return cls(source_data_item.year, source_data_item.region, source_data_item.type_)


class DataSource(BaseDataSource):
    def __init__(self, year, region, type_):
        super().__init__(year, region, type_)
        self.source_data = None

    def input_data(self, raw_data: tuple) -> None:
        for _, _, _, source_value, target_value, value in raw_data:
            self.source_data.set_element(row_key=source_value, col_key=target_value, value=value)

    def get_new_perturbed_matrix(self):
        perturbed_data = DataSource(self.year, self.region, self.type_)
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


class ImportDataSource(DataSource):
    def __init__(self, year, source_region, target_region, type_):
        super().__init__(year, None, type_)
        self.source_region = source_region
        self.target_region = target_region

    @classmethod
    def get_new_empty_source_data_item(cls, source_data_item):
        """
        :param source_data_item:
        :type source_data_item: ImportDataSource
        :return:
        """
        return cls(source_data_item.year,
                   source_data_item.source_region,
                   source_data_item.target_region,
                   source_data_item.type_)


class EmissionsDataSource(BaseDataSource):
    def __init__(self, year, region, type_):
        super().__init__(year, region, type_)
        self.source_data = None

    # OK this is named wrong but it makes things a lot easier to deal with and a vector is a 1D matrix anyway, right?!
    def get_new_perturbed_matrix(self):
        perturbed_data = EmissionsDataSource(self.year, self.region, self.type_)
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


class TotalsOnlyDataSource(BaseDataSource):
    def __init__(self, year, region, type_, system=None):
        super().__init__(year, region, type_, system)
        self.row_totals = None
        self.column_totals = None
        self.constraints = dict()
        self.source_data = None

    def set_row_and_column_totals(self, row_totals: dict, column_totals: dict):
        self.row_totals = Vector.create_vector_from_dict(row_totals)
        self.column_totals = Vector.create_vector_from_dict(column_totals)

    @staticmethod
    def _make_vector_sums_equal(vector1: Vector, vector2: Vector) -> tuple:
        sum_vector1 = sum(x for x in vector1.elements.A1)
        sum_vector2 = sum(x for x in vector2.elements.A1)

        half_difference = (sum_vector1 - sum_vector2) / 2

        new_vector1 = Vector([x - (half_difference/len(vector1.elements.A1)) for x in vector1.elements.A1])
        new_vector2 = Vector([x + (half_difference/len(vector2.elements.A1)) for x in vector2.elements.A1])

        return new_vector1, new_vector2

    def _get_new_totals_vector(self):
        perturbed_row_totals = get_new_perturbed_vector(self.row_totals, self.distribution)
        perturbed_column_totals = get_new_perturbed_vector(self.column_totals, self.distribution)
        # TODO does one need to adjust the known elements of the matrix to the new totals?
        #  I'm assuming not
        return TotalsOnlyDataSource._make_vector_sums_equal(perturbed_row_totals, perturbed_column_totals)

    def _create_data_with_same_internals_as_self(self):
        perturbed_data = DataSource(self.year, self.region, self.type_)
        perturbed_data.distribution = self.distribution
        perturbed_data.system = self.system
        return perturbed_data

    def get_new_perturbed_matrix(self):
        """
        perturb the row and column totals, then use RAS to guess at a new matrix and return that
        :return:
        """
        perturbed_row_totals, perturbed_column_totals = self._get_new_totals_vector()

        perturbed_constraints = {key: float(value) + float(value) * self.distribution.get_observation()
                                 for key, value in self.constraints.items()}

        perturbed_data = self._create_data_with_same_internals_as_self()

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
