import re
import time

import matplotlib.pyplot as plt

from dice_tools import *
from dice_tools.helpers.xmodel import *
from .plot_objects import *

import concurrent.futures

executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)


def plot(line):
    wizard.plot_log(line)


class PlotsApp(DICEObject):

    def __init__(self, app, **kwargs):
        super().__init__(base_type='QObject', **kwargs)

        self.__app = app
        self.__model = standard_model(
            PlotObject,
            ResidualsPlotObject,
            ForcesPlotObject
        )

        self.__model.root_elements.append(
            ResidualsPlotObject('Residuals', app=self.app))

        # wizard.subscribe("w_log", self.__w_log)
        # wizard.subscribe("finalize_plot", self.__finalize_plots)

    @property
    def app(self):
        return self.__app

    @diceProperty('QVariant', name='model')
    def model(self):
        return self.__model

    def add_function_objects_plot(self, item):
        plot_names = [plot.name for plot in self.__model]
        if item.name not in plot_names:
            if item.type == "forces":
                plot = ForcesPlotObject(item.name, app=self.__app)
            else:
                plot = PlotObject(item.name, app=self.__app)
            self.__model.root_elements.append(plot)

    def remove_function_objects_plot(self, item):
        for plot in self.__model:
            if plot.name == item.name:
                self.__model.root_elements.remove(plot)

    # def __w_log(self, line):
    #     for p in self.__model:
    #         if isinstance(p, ResidualsPlotObject):
    #             p.plot_log(line)
    #         elif isinstance(p, ForcesPlotObject):
    #             p.plot_log(line)
    #
    # def __finalize_plots(self):
    #     for p in self.__model:
    #         if isinstance(p, ResidualsPlotObject):
    #             p.finalize_plot()
    #         elif isinstance(p, ForcesPlotObject):
    #             p.finalize_plot()
