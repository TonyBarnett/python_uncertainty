from decimal import Decimal
from uncertainty.data_sources import read_from_sql
from matplotlib import pyplot
from use_uncertainty_model.useful_functions import get_source_data
from useful_scripts.useful_functions.plot_functions import plot, THESIS_LOCATION, PRESENTATION_LOCATION, \
    save_to_usual_places


def get_x_y(x, y, index, file_name, line_number, value):
    if index[file_name][line_number] not in pas_x:
        x.append(index[file_name][line_number])
        y.append(pas)
    return x, y


if __name__ == '__main__':
    source_data = get_source_data()
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
    foo = 0.0
    # FileName, FileLineNo, EClass,  PAS2050Footprint, atukFootprint, ioFootprint, ModelUncertainty, PriceUncertainty
    # mean + uncertainty, mean - uncertainty
    for file_name, line_number, _, pas, atuk, new_intensities, _, _, _, _, _ in source_data:
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
            foo = Decimal(new_intensities)
        else:
            foo += new_intensities
    new_model_y.append(foo)
    plot((pas_x, atuk_x, new_model_x),
         (pas_y, atuk_y, new_model_y),
         styles=("kx", "b.", "r*"),
         xlabel="Product",
         ylabel="Carbon footprint",
         y_axis=(-1, 14),
         hold=True,
         legends=('PAS2050 model', '@UK model', 'single-region input-output model'))

    save_to_usual_places("three_cf_comparison.pdf")

