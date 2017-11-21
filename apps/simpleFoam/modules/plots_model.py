import re
import time

import matplotlib.pyplot as plt

from dice_tools import *
from dice_tools.helpers.xmodel import *
from .plot_objects import *

# import concurrent.futures

# executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)


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
        self.__model.root_elements.append(
            ResidualsPlotObject('Residuals 1', app=self.app))
        self.__model.root_elements.append(
            ResidualsPlotObject('Residuals 2', app=self.app))
        self.__model.root_elements.append(
            ResidualsPlotObject('Residuals 3', app=self.app))
        self.__model.root_elements.append(
            ResidualsPlotObject('Residuals 4', app=self.app))

        wizard.subscribe("finalize_plot", self.__w_finalize_plot)

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

    def log_line(self, line):
        for p in self.__model:
            # print("plotting ..", p)
            if isinstance(p, ResidualsPlotObject):
                # executor.submit(p.plot_log, line)
                p.plot_log(line)
            elif isinstance(p, ForcesPlotObject):
                p.plot_log(line)
                # executor.submit(p.plot_log, line)

    def __w_finalize_plot(self):
        for p in self.__model:
            if isinstance(p, ResidualsPlotObject):
                p.finalize_plot()
            elif isinstance(p, ForcesPlotObject):
                p.finalize_plot()
