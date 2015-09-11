from matplotlib import pyplot
from uncertainty.data_sources import read_from_sql

from useful_scripts.useful_functions.plot_functions import plot, THESIS_LOCATION, \
    PRESENTATION_LOCATION, save_to_usual_places

if __name__ == '__main__':
    query = """ ;
WITH T AS (
    SELECT LEFT(ci.strValue, 1) AS strClass, intInstanceId, ROUND(AVG(monPmax) / AVG(monPmin), 1) AS intQ
    FROM bmkBenchmark bmk
        INNER JOIN pInstance i ON bmk.intInstanceId = i.intId
        INNER JOIN pUnit u ON i.intUnitId = u.intId
        INNER JOIN clasInstance ci ON u.intProductID = ci.intProductID AND ci.intSystemID = 4
    WHERE strCurrencyCode = 'GBP'
        AND intBuyers > 1
        AND fltQmin > 1
        AND YEAR(datWindowStart) = 2008
        AND monPmin > 0
    GROUP BY intInstanceId, ci.strValue
)
SELECT intQ, CAST(COUNT(*) AS float) / CAST(MIN(c.countStar) AS float)
FROM T
    CROSS APPLY (
        SELECT COUNT(*) AS countStar
        FROM T
    ) c
WHERE T.intQ <= 5
GROUP BY intQ
ORDER BY intQ
"""

    result = read_from_sql(query, db="Heaven", server="spendsql1.london.ukplc.corp", uid="OFFICE\\Tony.barnett",
                           pw="CAll3vaa")

    total = 0
    x = list()
    y = list()
    # culmulative frequencying
    for x_i, y_i in result:
        x.append(x_i)
        total += y_i
        y.append(total)

    # foo = {"2006": 32.78308122, "2007": 50.43775076, "2008": 95.02981872, "2009": 94.60830317, "2010": 89.78880001,
    #        "2011": 81.47413047, "2012": 119.1611073, "2013": 115.2751452, "2014": 118.6303942, "2015": 88.92820672}

    plot((x,), (y,), ("kx",), xlabel="$\\lambda$",
         ylabel="""percentage of products for which the maximum unit
         price is less than $\\lambda$ times the minimum price""",
         hold=True)
    # add_regression_lines_to_graph(x)
    save_to_usual_places("uncertainty_unit_price_default.pdf")
