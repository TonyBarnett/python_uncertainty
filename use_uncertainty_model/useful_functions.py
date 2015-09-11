from uncertainty.data_sources import read_from_sql


def _add_entry_to_dict(dict_: dict, file_name: str, entry: int):
    if file_name not in dict_:
        dict_[file_name] = dict()
    if entry not in dict_[file_name]:
        dict_[file_name][entry] = 0.0


def _add_item_to_pas(pas_cf: dict, file_name: str, line_number: int, pas: float):
    _add_entry_to_dict(pas_cf, file_name, line_number)
    pas_cf[file_name][line_number] = pas


def _add_item_to_atuk(atuk_cf: dict, file_name: str, line_number: int, pas: float):
    raise NotImplementedError()


def get_carbon_footprints_of_source_data(source_data):
    result = list()
    foo = 0.0
    pas_cf = dict()
    atuk_cf = dict()
    io_cf = dict()

    for file_name, line_number, price, e_class, pas, atuk, weight, new_intensities, model_uncertainty in source_data:

        if file_name not in pas_cf:
            pas_cf[file_name] = dict()


def get_source_data() -> tuple:
    """
    gets the output of the model under uncertainty.
    (file_name, file_line_number, price, eClass, PAS2050_footprint, atuk_footprint, weight, model_cf, model_uncertainty)
    :return:
    """
    query = """
    SELECT t.strFileName,
        t.intFileLineNo,
        t.strEClass,
        t.PAS2050Footprint,
        t.atukFootprint,
        t.ioFootprint,
        t.ModelUncertainty,
        t.PriceUncertainty,
        SQRT(t.ModelUncertainty * t.ModelUncertainty + t.PriceUncertainty * t.PriceUncertainty) AS TotalUncertainty,
        t.ioFootprint + (SQRT(t.ModelUncertainty * t.ModelUncertainty + t.PriceUncertainty * t.PriceUncertainty) * t.ioFootprint / 100),
        t.ioFootprint - (t.ModelUncertainty * t.ioFootprint / 100)
    FROM (
        SELECT t.strFileName,
            t.intFileLineNo,
            t.strEClass,
            MIN(t.fltPAS2050Footprint) AS PAS2050Footprint,
            SUM(t.fltAtukFootprint) AS atukFootprint,
            SUM(t.mean * t.fltWeight * t.MonPrice) AS ioFootprint,
            SQRT(SUM(t.fltModelUncertainty * t.fltModelUncertainty) / CAST(COUNT(*) AS float)) AS ModelUncertainty,
            100 AS PriceUncertainty
        FROM (
            SELECT data.strFileName,
                data.intFileLineNo,
                CAST(data.MonPrice AS float) AS MonPrice,
                data.strEClass,
                data.fltPAS2050Footprint,
                data.MonPrice * data.fltC123Intensity * ce.fltWeight AS fltAtukFootprint,
                ce.fltWeight,
                mc.strCensa123Key,
                mc.mean,
                mc.fltModelUncertainty
            FROM dataPAS2050Atuk data
                INNER JOIN God..gCensa123_eClass ce ON ce.strEClass = data.strEClass
                INNER JOIN MonteCarlo_test..ModelUncertainty mc ON mc.strCensa123Key = CAST(ce.intCensa123 AS varchar(3))
            ) t
        GROUP BY t.strFileName,
            t.intFileLineNo,
            t.strEClass
    ) t
    ORDER BY 1, 2
    """
    return read_from_sql(query, db="PasVsAtuk")
