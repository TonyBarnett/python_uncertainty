import logging
import multiprocessing
import time

from uncertainty.data_structures.get import get_data_source_of_type
from uncertainty.data_structures.populate import populate_source_data_of_type
from uncertainty.data_mapping.map_data import map_source_data_matrix
from uncertainty.source_uncertainty_distribution import get_distribution_of_type_and_region
from uncertainty.Monte_Carlo.single_region_model import run_single_region_model
from uncertainty.data_sources.sql import write_intensities_to_sql

INPUT_YEARS = (2008,)
INPUT_MATRICES = ("consumption", "production", "emissions")
INPUT_REGIONS = ("UK", "EU")
# NUMBER_OF_ITERATIONS = 1
NUMBER_OF_ITERATIONS = 10000


def create_and_populate_source_data(year) -> list:
    source_data = list()
    for region in INPUT_REGIONS:
        for type_ in INPUT_MATRICES:
            if not (type_ == "emissions" and region == "EU"):
                source_data_item = get_data_source_of_type(year=year, region=region, type_=type_)
                source_data.append(source_data_item)
                populate_source_data_of_type(source_data_item)
    # now do imports, we only care about EU importing into UK for now.
    # TODO uncomment the next 3 lines, you will need to work out why IOModel.sor.Exports is empty...
    # source_data_item = get_data_source_of_type(year=year, region="EU", type_="import", target_region="UK")
    # source_data.append(source_data_item)
    # populate_source_data_of_type(source_data_item)
    return source_data


def get_source_data_distribution(source_data):
    for source_data_item in source_data:
        source_data_item.distribution = get_distribution_of_type_and_region(type_=source_data_item.type_,
                                                                            region=source_data_item.region
                                                                            )


def get_perturb_source_data(source_data):
    perturbed_data = list()
    for source_data_item in source_data:
        perturbed_data.append(source_data_item.get_new_perturbed_matrix())
    return perturbed_data


def process_worker(source_data, percent_complete, input_year, pipe_end):
    logging.basicConfig(format='%(message)s - %(asctime)-15s', level=logging.DEBUG)

    while True:
        run_number = pipe_end.recv()
        if run_number is None:
            return
        if run_number % percent_complete == 0:
            logging.debug("{0}% complete".format(run_number / percent_complete))

        perturbed_data = get_perturb_source_data(source_data)
        mapped_data = map_source_data_matrix(perturbed_data)

        uk_consumption = mapped_data["consumption"]["UK"]
        uk_production = mapped_data["production"]["UK"]
        uk_emissions = mapped_data["emissions"]["UK"]
        intensities = run_single_region_model(uk_production, uk_consumption, uk_emissions)
        write_intensities_to_sql(intensities, run_number, input_year, "Single Region")
        pipe_end.send("hit me")


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
    process_count = 3

    for input_year in INPUT_YEARS:
        logging.debug("year: {0}".format(input_year))

        logging.debug("creating and populating matrices")
        source_data = create_and_populate_source_data(input_year)

        logging.debug("getting distributions")
        get_source_data_distribution(source_data)

        logging.debug("running Monte Carlo...")
        percent_complete = NUMBER_OF_ITERATIONS / 100
        run_number_queue = [x for x in range(NUMBER_OF_ITERATIONS)]
        pipe_process = list()

        for _ in range(process_count):
            mine, theirs = multiprocessing.Pipe(duplex=True)
            process = multiprocessing.Process(target=process_worker, kwargs=dict(source_data=source_data,
                                                                                 percent_complete=percent_complete,
                                                                                 input_year=input_year,
                                                                                 pipe_end=theirs))
            process.start()
            pipe_process.append({'pipe': mine, 'process': process})

        for pp in pipe_process:
            thing = run_number_queue.pop()
            pp["pipe"].send(thing)
            # run_two_region_model(year)
        while pipe_process:
            for pp in pipe_process:
                if pp["pipe"].poll():
                    pp["pipe"].recv()
                    if run_number_queue:
                        message = run_number_queue.pop()
                        pp["pipe"].send(message)
                    else:
                        pp["pipe"].send(None)

                    # pp["pipe"].send(message)
            time.sleep(1)
            pipe_process = [x for x in pipe_process if x["process"].is_alive()]

    logging.debug("finished")
