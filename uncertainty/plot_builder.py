import multiprocessing

from matplotlib import pyplot

colours = {"black": "k", "blue": "b", "red": "r", "green": "g"}
markers = {"cross": "x", "line": "-", "dot": ".", "big_dot": "o"}
marker_size = 5


def sort_axes_by_x(x: list, y: list) -> tuple:
    y = [b for (a, b) in sorted(zip(x, y))]
    x = sorted(x)
    return x, y


class PlotType:
    def __init__(self, x: list, y: list):
        self.marker = None
        self.x = x
        self.y = y

    def set_marker(self, marker_type):
        if marker_type in markers.values():
            self.marker = marker_type

        elif marker_type in markers.keys():
            self.marker = markers[marker_type]

        else:
            raise ValueError("{0} not a valid marker type".format(marker_type))

    def set_colour(self, colour):
        if colour in colours.values():
            self.marker = colour

        elif colour in colours.keys():
            self.marker = colours[colour]

        else:
            raise ValueError("{0} not a valid colour".format(colour))


class ScatterPlot(PlotType):
    def __init__(self, x: list, y: list):
        super().__init__(x, y)
        self.marker = "x"


class LinePlot(PlotType):
    def __init__(self, x: list, y: list):
        (x, y) = sort_axes_by_x(x, y)
        super().__init__(x, y)
        self.marker = "-"


class PlotBuilder:
    def __init__(self):
        # a list of PlotTypes
        self.plots = list()

    def add_plot_type(self, plot_type: PlotType):
        self.plots.append(plot_type)

    @staticmethod
    def _plot_worker(plots):
        pyplot.figure()

        for plot_type in plots:
            pyplot.plot(plot_type.x, plot_type.y, plot_type.marker)
            pyplot.hold(True)
        pyplot.show()

    def plot(self):
        p = multiprocessing.Process(target=PlotBuilder._plot_worker, kwargs={"plots": self.plots})
        p.start()
