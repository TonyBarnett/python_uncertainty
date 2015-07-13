from uncertainty.matrix import Matrix, Vector
from models import single_region


def run_single_region_model(uk_production: Matrix,
                            uk_consumption: Matrix,
                            uk_emissions: Vector) -> Vector:
    single_region.run_model(uk_consumption, uk_production, uk_emissions)
