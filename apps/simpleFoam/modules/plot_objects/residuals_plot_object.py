import os
import re
import json
import time

from .plot_object import PlotObject
from dice_tools import *
from dice_tools.helpers.xmodel import *

import matplotlib.pyplot as plt
from dice_plot.plot import Plot


class ResidualsPlotObject(PlotObject):

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)

        self.__plot = Plot(plt.figure())
        self.__plot_ax = self.__plot.figure.add_subplot(111)

        self.__plot_data_directory_path = self.app.run_path('data', 'plots')
        self.__plot_data_path = os.path.join(
            self.__plot_data_directory_path, self.name + '_plot_data'
        )

        self.__w_prepare()
        self.__load_reg_expr()

        wizard.subscribe("progress_changed", self.__w_progress_changed)
        wizard.subscribe("prepare", self.__w_prepare)
        wizard.subscribe("w_log", self.__w_log)
        wizard.subscribe("finalize_plot", self.finalize_plot)
        wizard.subscribe("w_visible_changed", self.__w_visible_changed)

    def __load_reg_expr(self):
        # reg-expression:
        # ===============
        # ^  : assert position at start of the string
        # () : capturing group
        # .+ : mathes any character (except newline), + : between one and unlimited times

        reg_expression = "^(.+):  Solving for (.+), Initial residual = (.+), Final residual = (.+), No Iterations (.+)$"
        self.__expression = re.compile(reg_expression)

        time_reg_expression = "^Time = (.+)$"
        self.__res_time_expression = re.compile(time_reg_expression)

    @modelRole('plot')
    def plot(self):
        return self.__plot

    def __w_visible_changed(self):
        self.__draw_plot(force=True)

    def __w_progress_changed(self, progress):
        """
        Load plot data if app is finished with simpleFoam task.
        """
        simple_foam_index = self.app.__dice_tasks__.index(self.app.__class__.run_simpleFoam)
        if ((progress < 0 or progress > simple_foam_index)
            and (not self.__plot_data and os.path.exists(self.__plot_data_path))):

                with open(self.__plot_data_path) as f:
                    self.__plot_data = json.load(f)
                    self.__draw_plot()

    def __w_prepare(self):
        self.__plot_data = {}
        self.__init_residual = {}
        self.__time_value = None
        self.__plot_time_value = None
        self.__lines = {}
        self.__plot_time = 0

        self.__plot_ax.cla()
        self.__set_init_plot_style()
        self.__update_plot_scale()

    def __draw_plot(self, force=False):
        if not self.visible and not force:
            return
        now = time.time()
        if force or (now - self.__plot_time) > 0.5:
            for field_name, xy_values in self.__plot_data.items():
                if field_name not in [line_name for line_name in self.__lines]:
                    self.__lines[field_name], = self.__plot_ax.plot(*xy_values, label=field_name)
                else:
                    self.__lines[field_name].set_data(*xy_values)
            self.__update_plot_scale()
            self.__plot.draw()
            self.__plot_time = now

    def __w_log(self, line):
        """
        Parse logs to plot the initial residuals and iteration/time step.
        """
        res = self.__expression.match(line)
        if res is not None:
            linear_solver_name = res.groups()[0]
            field_var_name = res.groups()[1]
            init_residual = res.groups()[2]
            final_residual = res.groups()[3]
            iterations = res.groups()[4]
            self.__init_residual[field_var_name] = float(init_residual)

        res_time = self.__res_time_expression.match(line)
        if res_time is not None:
            self.__time_value = float(res_time.groups()[0])
            for field_name, field_value in self.__init_residual.items():
                if field_name not in self.__plot_data:
                    self.__plot_data[field_name] = [[], []]
                self.__plot_data[field_name][0].append(self.__time_value)
                self.__plot_data[field_name][1].append(field_value)
            self.__draw_plot()

    def __set_init_plot_style(self):
        self.__plot.figure.patch.set_alpha(0)
        self.__plot_ax.set_facecolor('None')
        self.__plot_ax.set_yscale('log')
        self.__plot_ax.grid(True)
        self.__plot_ax.set_ylim(ymax=1)
        self.__plot_ax.set_ylabel("Residuals (Log Scale)")
        self.__plot_ax.set_xlabel("Time (s) / Iterations")
        self.__plot_ax.set_autoscale_on(True)
        # self.__plot.figure.tight_layout()

    def __update_plot_scale(self):
        self.__plot_ax.legend(loc='upper right')
        self.__plot_ax.relim()
        self.__plot_ax.autoscale_view(True, True, True)

    def finalize_plot(self):
        """
        Execute plot at the end because of the plot interval in draw_plot
        and save data.
        """
        self.__draw_plot(force=True)
        self.__save_data()
        self.__save_figure()

    def __save_data(self):
        if not os.path.exists(self.__plot_data_directory_path):
            os.makedirs(self.__plot_data_directory_path)
        with open(self.__plot_data_path, 'w') as file:
            json.dump(self.__plot_data, file)

    def __save_figure(self):
        self.__plot.figure.savefig(self.__plot_data_path + '.png')
