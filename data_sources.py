import pymongo
import pymssql


def read_from_sql(query: str, params: tuple=None, db: str=None, server='localhost', uid='sa', pw='deter101!'):
    with pymssql.connect(server, uid, pw, db) as conn:
        with conn.cursor() as cursor:
            # The star says you want a list of parameters for the format.
            cursor.execute(query if not params else query.format(*params))
            return cursor.fetchall()


def get_map(map_collection: str='Plain_KNN_Without_Ancestors_k_3'):
    collection = pymongo.MongoClient('10.10.20.37').ClassificationMap[map_collection]
    mapping = dict()
    for map_ in collection.find():
        system = map_["_id"]["system"]
        value = map_["_id"]["value"]
        mapped_values = map_["map"]
        if system not in mapping:
            mapping[system] = dict()
        mapping[system][value] = mapped_values
    return mapping


def get_classification_systems_data(system_id: str=None, value_id: str=None, used: bool=None):
    """ I'm sorry, this is really badly made but I can't be bothered to make it any better
    :param system_id:
    :param value_id:
    :param used:
    :return:
    """
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
    where_string = "blah"
    if used or system_id:
        where_string = "WHERE "
        for w in where:
            where_string += " {0} AND".format(w)

    # trim the last AND
    query += where_string[:-4]
    class_sys_data = dict()
    for sys_id, val_id, description in read_from_sql(query, tuple([system_id, value_id]), db="ClassificationSystems"):
        if sys_id not in class_sys_data:
            class_sys_data[sys_id] = dict()

        class_sys_data[sys_id][val_id] = description
    return class_sys_data