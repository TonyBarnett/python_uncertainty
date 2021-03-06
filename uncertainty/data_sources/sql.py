import multiprocessing
import pymssql


def read_from_sql(query: str, params: tuple=None, db: str=None, server='localhost', uid='sa', pw='deter101!'):
    with pymssql.connect(server, uid, pw, db) as conn:
        with conn.cursor() as cursor:
            # The star says you want a list of parameters for the format.
            cursor.execute(query if not params else query.format(params))
            return make_query_result_tuple(cursor.fetchall())


def write_to_sql(query: str, params: tuple=None, db: str=None, server='localhost', uid='sa', pw='deter101!'):
    with pymssql.connect(server, uid, pw, db) as conn:
        with conn.cursor() as cursor:

            # The star says you want a list of parameters for the format.
            if params and isinstance(params[0], tuple):
                cursor.executemany(query, params)
            elif params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
        conn.commit()


def build_clas_value_query(system_id: str, value_id: str, used: bool) -> str:
    where = list()
    select = "v.strSystemId, v.strValue, v.strDescription "
    from_ = "clasValue v"

    inner_join = ""
    if used:
        inner_join = " clasSystem s ON s.strName = v.strSystemId"
        where.append("s.bolUsed = {0}".format(1 if used else 0))

    if system_id:
        if not value_id:
            raise ValueError("cannot have a value_id without a system_id")
        where.append(" v.strSystemId = %s")

        if value_id:
            where.append(" v.strValue = %s")
    query = "SELECT {0} FROM {1} ".format(select, from_)

    if inner_join:
        query += "INNER JOIN {0} ".format(inner_join)
    # we have to have four letters so we have something to strip off at the end if there are no conditions
    # feels a little hacky but this isn't a big thing
    where_string = ""
    if where:
        where_string = "WHERE "
        where_string += " AND ".join(where)

    # trim the last AND
    return query + where_string[:-4]


def make_query_result_tuple(query_results) -> tuple:
    return tuple([result for result in query_results])


def clean_sql(query):
    return query.replace("  ", " ")


def _build_where_string(where_list):
    if where_list:
        return " WHERE " + " AND ".join(where_list)
    return ""


def build_import_query(query, source_region=None, target_region=None, year=None):
    where = list()
    if source_region is not None:
        where.append(" strSourceRegion = '{}'".format(source_region))

    if target_region is not None:
        where.append(" strTargetRegion = '{}'".format(target_region))

    if year is not None:
        where.append(" intYear = {}".format(year))

    where_string = _build_where_string(where)
    return clean_sql(query + where_string)


def build_source_query(query, region=None, year=None):
    """

    :param query: the SELECT, the FROM and any JOINs you wish
    :param region:
    :param year:
    :return:
    """
    where = list()
    if region is not None:
        where.append(" strRegion = '{}'".format(region))

    if year is not None:
        where.append(" intYear = {}".format(year))

    where_string = _build_where_string(where)
    return clean_sql(query + where_string)


def write_to_sql_in_background(query: str,
                               params: tuple=None,
                               db: str=None,
                               server='localhost',
                               uid='sa',
                               pw='deter101!'
                               ):
    p = multiprocessing.Process(target=write_to_sql, kwargs=dict(query=query,
                                                                 params=params,
                                                                 db=db,
                                                                 server=server,
                                                                 uid=uid,
                                                                 pw=pw
                                                                 ))

    p.start()


def write_intensities_to_sql(intensities: list, run_number: int, year: int, model: str) -> None:
    """
    Spawn a background worker that writes the intensities to SQL
    :param intensities:
    :param run_number:
    :return:
    """
    params = list()
    for counter, intensity in enumerate(intensities[0]):
        params.append((year, model, run_number, str(counter + 1), intensity))
    write_to_sql_in_background("INSERT INTO Intensities (intYear, strModel, intRun, strCensa123Key, fltIntensity) "
                               "VALUES (%d, %s, %d, %s, %d)",
                               params=tuple(params),
                               db="MonteCarlo")
