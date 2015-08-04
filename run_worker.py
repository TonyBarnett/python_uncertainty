import logging
import multiprocessing
import time
from uncertainty.Monte_Carlo import run_single_region_model
from uncertainty.data_mapping.map_data import map_source_data_matrix
from uncertainty.data_sources.sql import write_intensities_to_sql

NUMBER_OF_ITERATIONS = 10000


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


def pop_from_queue():
    raise NotImplementedError()


def create_and_start_processes(process_count, source_data, input_year):
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


def run_processes(pipe_process, run_number_queue):
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

if __name__ == "__main__":
    raise NotImplementedError()