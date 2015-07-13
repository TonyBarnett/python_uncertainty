import logging

from data_structures.get import get_data_source_of_type
from data_structures.populate import populate_source_data_of_type
from uncertainty.data_mapping.map_data import map_source_data_matrix
from uncertainty.source_uncertainty_distribution import get_distribution_of_type_and_region
from uncertainty.Monte_Carlo.single_region_model import run_single_region_model

INPUT_YEARS = (2008,)
INPUT_MATRICES = ("consumption", "production", "emissions")
INPUT_REGIONS = ("UK", "EU")
SOURCE_DATA = list()
MAPPED_DATA = dict()
NUMBER_OF_ITERATIONS = 1
# NUMBER_OF_ITERATIONS = 10000


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

            uk_consumption = MAPPED_DATA["consumption"]["UK"]
            uk_production = MAPPED_DATA["production"]["UK"]
            uk_emissions = MAPPED_DATA["emissions"]["UK"]
            intensities = run_single_region_model(uk_production, uk_consumption, uk_emissions)
            print(intensities)
            # run_two_region_model(year)

    logging.debug("finished")
