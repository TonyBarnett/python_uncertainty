from run_uncertainty_model import create_and_populate_source_data
from uncertainty.data_mapping import map_source_data_matrix
from uncertainty.data_structures import TotalsOnlyDataSource


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
            source_data.append(source_thing)

    for source_data_item in source_data:
        if type(source_data_item) is TotalsOnlyDataSource:
            raise NotImplementedError()

    mapped_data = map_source_data_matrix(source_data)

    print(1)

