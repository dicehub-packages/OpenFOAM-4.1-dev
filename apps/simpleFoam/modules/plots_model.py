import re
import time

import matplotlib.pyplot as plt

from dice_tools import *
from dice_tools.helpers.xmodel import *
from .plot_objects import *


class PlotsApp(DICEObject):

    def __init__(self, app, **kwargs):
        super().__init__(base_type='QObject', **kwargs)

        self.__app = app
        self.__model = standard_model(
            PlotObject,
            ResidualsPlotObject
        )

        self.__model.root_elements.append(
            ResidualsPlotObject('Residuals', app=self.app))

        wizard.subscribe("finalize_plot", self.__w_finalize_plot)

    @property
    def app(self):
        return self.__app

    @diceProperty('QVariant', name='model')
    def model(self):
        return self.__model

    def add_plot(self, name):
        plot_names = [plot.name for plot in self.__model]
        if name not in plot_names:
            plot = PlotObject(name, app=self.__app)
            self.__model.root_elements.append(plot)
            return plot

    def remove_plot(self, name):
        for plot in self.__model:
            if plot.name == name:
                self.__model.root_elements.remove(plot)

    def log_line(self, line):
        for p in self.__model:
            if isinstance(p, ResidualsPlotObject):
                p.plot_log(line)

    def __w_finalize_plot(self):
        for p in self.__model:
            if isinstance(p, ResidualsPlotObject):
                p.finalize_plot()
