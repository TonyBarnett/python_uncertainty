from utility_functions import float_range
from use_uncertainty_model.useful_functions import get_source_data
from useful_scripts.useful_functions.plot_functions import plot, save_to_usual_places, background_plot


def get_new_footprint(footprint, uncertainty, comparer):
    if footprint + uncertainty < comparer:
        return footprint + uncertainty

    if footprint - uncertainty > comparer:
        return footprint - uncertainty

    return comparer


def do(x: list, y: list, file_name, xlabel, ylabel):
    tolerance = 10 ** -5
    lambda_ = [i for i in float_range(0, 1.0001, 0.0001)]

    percentage_same = list()

    for l in lambda_:
        modified_y = list()
        for i, x_i in enumerate(x):
            modified_y.append(get_new_footprint(x_i, x_i * l, y[i]))

        percentage_same.append(100 * sum(1 for i, m_y in enumerate(modified_y)
                                         if abs(m_y - y[i]) < tolerance) / len(modified_y))

    print("percent of products for which p_i = s'_i: {0}".format(percentage_same[0]))

    plot((lambda_,),
         (percentage_same,),
         ('k.',),
         hold=True,
         x_axis=(-0.01, 1.01),
         y_axis=(-1, 101),
         xlabel=xlabel,
         ylabel=ylabel)

    save_to_usual_places(file_name)


# TODO work out the variance required in the PAS footprint to make it the same as the modified SRIO footprint
if __name__ == '__main__':
    source_data = get_source_data()

    pas_cfs = list()
    atuk_cfs = list()
    io_cfs = list()
    for _, _, _, pas, atuk, new_footprint, _, _, total_uncertainty, _, _ in source_data:
        pas_cfs.append(pas)
        io_cfs.append(get_new_footprint(new_footprint, total_uncertainty * new_footprint / 100, pas))
        atuk_cfs.append(get_new_footprint(atuk, total_uncertainty * atuk / 100, pas))

    do(pas_cfs, io_cfs, "new_fp_pas_variance.pdf", "$\lambda$", "Percentage of products for which $p'_i = s'_i$.")
    do(pas_cfs, atuk_cfs, "atuk_pas_io_variance.pdf", "$\lambda$", "Percentage of products for which $p'_i = s'_i$.")

    # t.strFileName, t.intFileLineNo, t.strEClass, t.PAS2050Footprint, t.atukFootprint, t.ioFootprint,
    # t.ModelUncertainty,
    #     t.ioFootprint + (t.ModelUncertainty * t.ioFootprint / 100),
    #     t.ioFootprint - (t.ModelUncertainty * t.ioFootprint / 100)
