from collections import OrderedDict
from IOModel import matrix_functions
import numpy
from IOModel.matrix_balancing import cras

from ..get_new_random_matrix import get_new_perturbed_matrix, get_new_perturbed_vector
from ..matrix import Matrix, Vector
from ..get_new_random_matrix import get_perturbed_value


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
        x = cls(source_data_item.year, source_data_item.region, source_data_item.type_)
        x.system = source_data_item.system
        return x

    def __str__(self):
        return str(self.source_data.elements)


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
        half_difference_over_v1 = (half_difference / len(vector1.elements.A1))
        half_difference_over_v2 = (half_difference / len(vector2.elements.A1))
        for x in vector1.elements.A1:
            if abs(x) < abs(half_difference_over_v1):
                print([x for x in vector1.elements])
                print("half difference of {0}".format(half_difference))
                raise ValueError("problem with vector jigery pokery")

        for x in vector2.elements.A1:
            if abs(x) < abs(half_difference_over_v2):
                print([x for x in vector2.elements])
                print("half difference of {0}".format(half_difference))
                raise ValueError("problem with vector jigery pokery")

        new_vector1 = Vector([x - half_difference_over_v1 for x in vector1.elements.A1])
        new_vector2 = Vector([x + half_difference_over_v2 for x in vector2.elements.A1])

        return new_vector1, new_vector2

    def _perturb_certain_elements(self, vector: Vector, elements_to_perturb: list) -> Vector:
        perturbations = list()
        for row in range(len(vector)):
            value = vector[row, 0]
            if row in elements_to_perturb:
                perturbation = self.distribution[value]
                if perturbation <= -1:
                    raise ValueError("trying to perturb an element of value {0} by {1}".format(value, perturbation))
                value = get_perturbed_value(vector[row, 0], perturbation)
            perturbations.append((row, value))
        return Vector.create_vector_from_tuple(tuple(perturbations))

    def _get_new_totals_vector(self, row_sum_perturbations, rows_to_perturb, col_sum_perturbations, columns_to_perturb):

        perturbed_row_totals = self._perturb_certain_elements(row_sum_perturbations, rows_to_perturb)
        perturbed_column_totals = self._perturb_certain_elements(col_sum_perturbations.T, columns_to_perturb)

        return TotalsOnlyDataSource._make_vector_sums_equal(perturbed_row_totals, perturbed_column_totals)

    def _create_data_with_same_internals_as_self(self):
        perturbed_data = DataSource(self.year, self.region, self.type_)
        perturbed_data.distribution = self.distribution
        perturbed_data.system = self.system
        return perturbed_data

    def _get_matrix_of_perturbations(self) -> Matrix:
        """
        make a matrix of perturbations, of the same properties as "self.source_data", unknowns will be zero
        :return:
        """
        data = list()
        for row, col, value in numpy.nditer(self.source_data.elements.A):
            if str(value) == "c":
                data.append((row, col, 0))
            else:
                data.append((row, col, float(value) * self.distribution[float(value)]))
        return Matrix.create_matrix_from_tuple(tuple(data))

    @staticmethod
    def _find_cs_in_matrix(m: numpy.matrix) -> list:
        """
        get a list of rows and a list of columns containing unknowns
        :param m:
        :return:
        """
        values = list()
        for row in range(m.shape[0]):
            for column in range(m.shape[1]):
                if m[(row, column)] == "c":
                    values.append((row, column))

        return values

    @staticmethod
    def _remove_cs_and_make_elements_float(m: Matrix) -> numpy.matrix:
        x = Matrix.deep_copy(m)
        for i in range(m.elements.shape[0]):
            for j in range(m.elements.shape[1]):
                x.elements[(i, j)] = 0 \
                    if m.elements[(i, j)] == "c" \
                    else float(m.elements[(i, j)])
        return x

    @staticmethod
    def _get_row_and_column_sums(m: numpy.matrix):
        just_numbers = TotalsOnlyDataSource._remove_cs_and_make_elements_float(m)
        row_sums = matrix_functions.get_row_sum(just_numbers.elements.astype(float))
        column_sums = matrix_functions.get_col_sum(just_numbers.elements.astype(float))
        return row_sums, column_sums

    def get_new_perturbed_matrix(self):
        """
        perturb the row and column totals, then use RAS to guess at a new matrix and return that
        :return:
        """
        # TODO perturb each known value, fix col and row sums, perturb row and col sums for rows/ cols with unknowns,
        # loop over row and column,
        #   if it's non-zero get a perturbation, add to the relevant row and column sums,
        #       if it's non-c then add to it and write to output and add it to constraints
        #       if it's c write "c" to the output
        # get the row and column sums from the original matrix and add the new values to them
        # get the constraints and run cRAS to get a brand spanking new matrix of perturbed values

        # FIXME for the love of God make this more maintainable
        row_sums, column_sums = TotalsOnlyDataSource._get_row_and_column_sums(self.source_data)

        perturbed_matrix = list()
        add_to_rows = {key: 0 for key in self.source_data.row_keys.keys()}
        add_to_columns = {key: 0 for key in self.source_data.column_keys.keys()}
        constraints = dict()
        for row in self.source_data.row_keys.keys():
            m_row = self.source_data.row_keys[row]
            perturbed_row = list()
            for column in self.source_data.column_keys.keys():
                m_column = self.source_data.column_keys[column]
                if self.source_data[(row, column)] == 0:
                    perturbed_row.append(0)

                    constraints[(m_row, m_column)] = 0

                elif self.source_data[(row, column)] == "c":
                    perturbed_row.append("c")
                    perturbation = self.distribution[1]
                    add_to_rows[row] += perturbation
                    add_to_columns[column] += perturbation

                else:
                    value = float(self.source_data[(row, column)])
                    perturbation = self.distribution[value]
                    perturbed_row.append(value + perturbation)
                    add_to_rows[row] += perturbation
                    add_to_columns[column] += perturbation

                    constraints[(m_row, m_column)] = value + perturbation
            perturbed_matrix.append(perturbed_row)

        new_row_sum = OrderedDict()
        new_column_sum = OrderedDict()

        for i, row_sum in enumerate(row_sums.A1):
            row_key = [key for key, value in self.source_data.row_keys.items() if value == i]
            if len(row_key) != 1:
                raise ValueError("row lookup failed")
            row_key = row_key[0]
            value_to_add = 0 if row_key not in add_to_rows.keys() else add_to_rows[row_key]
            new_row_sum[row_key] = row_sum + value_to_add

        for i, column_sum in enumerate(column_sums.A1):
            column_key = [key for key, value in self.source_data.column_keys.items() if value == i]
            if len(column_key) != 1:
                raise ValueError("column lookup failed")
            column_key = column_key[0]
            value_to_add = 0 if column_key not in add_to_columns.keys() else add_to_columns[column_key]
            new_column_sum[column_key] = column_sum + value_to_add

        perturbed_matrix = self._create_data_with_same_internals_as_self()

        perturbed_matrix.source_data = Matrix.get_new_matrix(cras.run_cras(
            Vector.create_vector_from_dict(new_row_sum).elements.T,
            Vector.create_vector_from_dict(new_column_sum).elements.T,
            constraints
        ))
        perturbed_matrix.source_data.row_keys = self.source_data.row_keys
        perturbed_matrix.source_data.column_keys = self.source_data.column_keys
        return perturbed_matrix

    def set_constraints(self, constraints):
        self.constraints = constraints

    def add_data_from_tuple(self, data):
        self.source_data = Matrix.create_matrix_from_tuple(data)
