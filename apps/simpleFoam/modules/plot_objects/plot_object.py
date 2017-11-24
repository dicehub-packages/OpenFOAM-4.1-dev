from dice_tools import *
from dice_tools.helpers.xmodel import *

import matplotlib.pyplot as plt
from dice_plot.plot import Plot


class PlotObject:

    def __init__(self, name, app, **kwargs):
        super().__init__(**kwargs)
        self.__name = name
        self.__app = app
        self.__visible = False

    @property
    def app(self):
        return self.__app

    @modelRole('name')
    def name(self):
        return self.__name

    @modelRole('visible')
    def visible(self):
        return self.__visible

    @modelMethod('setVisible')
    def set_visible(self, value):
        print("value ..", value)
        self.__visible = value
        wizard.w_visible_changed()
