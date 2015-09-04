from decimal import Decimal
from uncertainty.data_sources import read_from_sql
from matplotlib import pyplot
from useful_scripts.useful_functions.plot_functions import plot, THESIS_LOCATION, PRESENTATION_LOCATION


def get_x_y(x, y, index, file_name, line_number, value):
    if index[file_name][line_number] not in pas_x:
        x.append(index[file_name][line_number])
        y.append(pas)
    return x, y


if __name__ == '__main__':
    query = """
    SELECT data.strFileName,
        data.intFileLineNo,
        data.MonPrice,
        data.strEClass,
        data.fltPAS2050Footprint,
        data.fltAtukFootprint,
        ce.fltWeight,
        mc.mean,
        mc.fltModelUncertainty
    FROM dataPAS2050Atuk data
        INNER JOIN God..gCensa123_eClass ce ON ce.strEClass = data.strEClass
        INNER JOIN MonteCarlo..ModelUncertainty mc ON mc.strCensa123Key = CAST(ce.intCensa123 AS varchar(3))
    """
    source_data = read_from_sql(query, db="PasVsAtuk")
    index = dict()
    # awkward time: because there's no id for a given product (other than file_name, fileLineNo) we create an id
    # lookup.
    for idx, file_name, line_number in read_from_sql("SELECT "
                                                     "    ROW_NUMBER() "
                                                     "        OVER (ORDER BY data.strFileName, data.intFileLineNo) "
                                                     "        AS intIndex, "
                                                     "    data.strFileName, "
                                                     "    data.intFileLineNo "
                                                     "FROM dataPAS2050Atuk data",
                                                     db="PasVsAtuk"):
        if file_name not in index:
            index[file_name] = dict()
        if line_number not in index[file_name]:
            index[file_name][line_number] = idx

    pas_x = list()
    pas_y = list()
    atuk_x = list()
    atuk_y = list()
    new_model_x = list()
    new_model_y = list()
    foo = Decimal(0)
    for file_name, line_number, price, e_class, pas, atuk, weight, new_intensities, model_uncertainty in source_data:
        weight = Decimal(weight)
        new_intensities = Decimal(new_intensities)
        if index[file_name][line_number] not in pas_x:
            pas_x.append(index[file_name][line_number])
            pas_y.append(pas)

        if index[file_name][line_number] not in atuk_x:
            atuk_x.append(index[file_name][line_number])
            atuk_y.append(atuk)

        if index[file_name][line_number] not in new_model_x:
            new_model_x.append(index[file_name][line_number])
            if foo:
                new_model_y.append(foo)
            foo = Decimal(price * new_intensities * weight)
        else:
            foo += price * new_intensities * weight
    new_model_y.append(foo)
    plot((pas_x, atuk_x, new_model_x),
         (pas_y, atuk_y, new_model_y),
         styles=("kx", "b.", "r*"),
         xlabel="Product",
         ylabel="Carbon footprint",
         hold=True)

    pyplot.savefig(THESIS_LOCATION + r"three_cf_comparison.pdf")
    pyplot.savefig(PRESENTATION_LOCATION + r"three_cf_comparison.pdf")
