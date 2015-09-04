from IOModel.matrix_balancing import cras
from run_uncertainty_model import create_and_populate_source_data
from uncertainty.data_mapping import map_source_data_matrix
from uncertainty.data_structures import TotalsOnlyDataSource, DataSource
from uncertainty.matrix import Matrix, Vector


def estimate_unknowns(year: int):
    raise NotImplementedError()


def map_data(year: int):
    raise NotImplementedError()


def run_model(year: int):
    raise NotImplementedError()


if __name__ == '__main__':
    # get data
    # estimate unknowns
    # map data
    # run model
    year = 2008
    sd = create_and_populate_source_data(year)
    source_data = list()
    for source_thing in sd:
        if source_thing.region == "UK":
            if type(source_thing) == TotalsOnlyDataSource:
                new_source_thing = source_thing._create_data_with_same_internals_as_self()

                row_sums, column_sums = TotalsOnlyDataSource._get_row_and_column_sums(source_thing.source_data)

                new_source_thing.source_data = Matrix.get_new_matrix(cras.run_cras(
                    row_sums,
                    column_sums.T,
                    source_thing.constraints
                ))
                source_thing = new_source_thing
            source_data.append(source_thing)

    for source_data_item in source_data:
        if type(source_data_item) is TotalsOnlyDataSource:
            raise NotImplementedError()

    mapped_data = map_source_data_matrix(source_data)

    print(1)
