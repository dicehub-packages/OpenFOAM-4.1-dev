from dice_tools import *
from dice_tools.helpers.xmodel import *

import matplotlib.pyplot as plt
from dice_plot.plot import Plot


class PlotObject:

    def __init__(self, name, app, **kwargs):
        super().__init__(**kwargs)
        self.__name = name
        self.__app = app

        self.__plot = Plot(plt.figure())
        self.__plot_ax = self.__plot.figure.add_subplot(111)
        self.__plot.figure.patch.set_alpha(0)
        # # self.__set_plot_style()
        self.__plot_data = {}
        self.__plot_time = 0
        self.__lines = {}

    @property
    def app(self):
        return self.__app

    @modelRole('name')
    def name(self):
        return self.__name

    @modelRole('plot')
    def plot(self):
        return self.__plot

    @property
    def plot_ax(self):
        return self.__plot_ax

    @property
    def plot_data(self):
        return self.__plot_data