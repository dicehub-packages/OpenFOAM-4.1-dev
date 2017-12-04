import os
import re
import json
import time

from .plot_object import PlotObject
from dice_tools import *
from dice_tools.helpers.xmodel import *

import matplotlib.pyplot as plt
from dice_plot.plot import Plot


class ForcesPlotObject(PlotObject):

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)

        self.__plot = Plot(plt.figure())
        self.__plot_ax = self.__plot.figure.add_subplot(121)
        self.__plot_ax_2 = self.__plot.figure.add_subplot(122)

        self.__plot_data_directory_path = self.app.run_path('data', 'plots')
        self.__plot_data_path = os.path.join(
            self.__plot_data_directory_path, self.name + '_plot_data'
        )
        self.__data_file_path = self.app.run_path('postProcessing', self.name,
                                                  '0', 'forces.dat')

        self.__w_prepare()
        self.__load_reg_expr()

        wizard.subscribe("progress_changed", self.__w_progress_changed)
        wizard.subscribe("prepare", self.__w_prepare)
        wizard.subscribe("w_log", self.__w_log)
        wizard.subscribe("finalize_plot", self.finalize_plot)
        wizard.subscribe("w_visible_changed", self.__w_visible_changed)

    def __load_reg_expr(self):
        time_reg_expression = "^Time = (.+)$"
        self.__res_time_expression = re.compile(time_reg_expression)

        forces_name_reg_expression = "^forces (.+) write:$"
        self.__forces_name_expression = re.compile(forces_name_reg_expression)

        sum_of_forces_start_reg_expression = "\s*sum of forces:$"
        self.__sum_of_forces_start_expression = re.compile(sum_of_forces_start_reg_expression)

        forces_pressure_reg_expression = "\s*pressure\s*:\s*[^b](.+) (.+) (.+)[^b]$"
        self.__forces_pressure_expression = re.compile(forces_pressure_reg_expression)

        forces_viscous_reg_expression = "\s*viscous\s*:\s*[^b](.+) (.+) (.+)[^b]$"
        self.__forces_viscous_expression = re.compile(forces_viscous_reg_expression)

        sum_of_moments_reg_expression = "\s*sum of moments:"
        self.__sum_of_moments_expression = re.compile(sum_of_moments_reg_expression)

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
            and (not self.__plot_data['forces'] and not self.__plot_data['moments']
                 and os.path.exists(self.__plot_data_path))):

                with open(self.__plot_data_path) as f:
                    self.__plot_data = json.load(f)
                    if not self.__plot_data['forces'] or not self.__plot_data['moments']:
                        self.__draw_plot()

    def __w_prepare(self):
        self.__f_name = None
        self.__current_block = None
        self.__plot_data = dict()
        self.__plot_data['forces'] = {}
        self.__plot_data['moments'] = {}
        self.__init_residual = {}
        self.__time_value = None
        self.__lines = {}
        self.__lines_2 = {}
        self.__plot_time = 0

        self.__plot_ax.cla()
        self.__plot_ax_2.cla()
        self.__set_init_plot_style()
        self.__update_plot_scale()

    def __draw_plot(self, force=False):
        if not self.visible:
            return
        now = time.time()
        if force or (now - self.__plot_time) > 1.0:
            for field_name, xy_values in self.__plot_data['forces'].items():
                if field_name not in [line_name for line_name in self.__lines]:
                    self.__lines[field_name], = self.__plot_ax.plot(*xy_values, label=field_name)
                else:
                    self.__lines[field_name].set_data(*xy_values)
            for field_name, xy_values in self.__plot_data['moments'].items():
                if field_name not in [line_name for line_name in self.__lines_2]:
                    self.__lines_2[field_name], = self.__plot_ax_2.plot(*xy_values, label=field_name)
                else:
                    self.__lines_2[field_name].set_data(*xy_values)
            self.__update_plot_scale()
            self.__plot.draw()
            self.__plot_time = now

    def __w_log(self, line):
        """
        Parse logs for plot.
        """
        # TODO: Monitor post processing files instead of logs

        # Time step
        # =========
        res_time = self.__res_time_expression.match(line)
        if res_time is not None:
            self.__time_value = float(res_time.groups()[0])

        # Forces name
        # ===========
        res_f_name = self.__forces_name_expression.match(line)
        if res_f_name is not None:
            self.__f_name = res_f_name.groups()[0]

            # get only the correct block
            if self.__f_name != self.name:
                return

        # sum of forces (block start)
        # ===========================
        res_sum_of_forces_start = self.__sum_of_forces_start_expression.match(line)
        if res_sum_of_forces_start is not None and self.__f_name == self.name:
            sum_of_forces_start = res_sum_of_forces_start.group()
            self.__current_block = 'forces'
            # print(">> sum of forces start ", sum_of_forces_start)

        # sum of moments (block start)
        # ============================
        res_sum_of_moments_start = self.__sum_of_moments_expression.match(line)
        if res_sum_of_moments_start is not None and self.__f_name == self.name:
            sum_of_moments_start = res_sum_of_moments_start.group()
            self.__current_block = 'moments'

        # Actual data
        # ===========
        res_pressure = self.__forces_pressure_expression.match(line)
        if res_pressure is not None and self.__f_name == self.name:
            pressure = res_pressure.groups()
            pressure = [float(i) for i in pressure]

            if self.__current_block == 'forces':
                # print(">> forces pressure ", pressure)
                field_names = ('Pressure force [X]', 'Pressure force [Y]', 'Pressure force [Z]')
                self.__add_field_data(field_names, pressure, 'forces')
            else:
                # print(">> moments pressure ", pressure)
                field_names = ('Pressure moment [X]', 'Pressure moment [Y]', 'Pressure moment [Z]')
                self.__add_field_data(field_names, pressure, 'moments')

        res_viscous = self.__forces_viscous_expression.match(line)
        if res_viscous is not None and self.__f_name == self.name:
            viscous = res_viscous.groups()
            viscous = [float(i) for i in viscous]

            if self.__current_block == 'forces':
                # print(">> forces viscous ", viscous)
                field_names = ('Viscous force [X]', 'Viscous force [Y]', 'Viscous force [Z]')
                self.__add_field_data(field_names, viscous, 'forces')
            else:
                # print(">> moments viscous ", viscous)
                field_names = ('Viscous moment [X]', 'Viscous moment [Y]', 'Viscous moment [Z]')
                self.__add_field_data(field_names, viscous, 'moments')

        self.__draw_plot()

    def __add_field_data(self, field_names=(), value=None, block_type='forces'):
        for field_name in field_names:
            if field_name not in self.__plot_data[block_type]:
                self.__plot_data[block_type][field_name] = [[], []]
            self.__plot_data[block_type][field_name][0].append(self.__time_value)
            self.__plot_data[block_type][field_name][1].append(value[field_names.index(field_name)])

    def __set_init_plot_style(self):
        self.__plot.figure.patch.set_alpha(0)

        # Plot 1 (Forces)
        # ===============
        box = self.__plot_ax.get_position()
        self.__plot_ax.set_position([box.x0, box.y0 + box.height * 0.10,
                                     box.width, box.height * 0.90])
        self.__plot_ax.set_facecolor('None')
        self.__plot_ax.set_ylim(ymax=1)
        self.__plot_ax.set_title("Pressure/viscous forces")
        self.__plot_ax.set_ylabel("Forces [N]")
        self.__plot_ax.set_xlabel("Time(s)/Iterations")
        self.__plot_ax.grid(True)
        self.__plot_ax.set_autoscale_on(True)

        # Plot 2 (Moments)
        # ================
        box_2 = self.__plot_ax_2.get_position()
        self.__plot_ax_2.set_position([box_2.x0, box_2.y0 + box_2.height * 0.10,
                                       box_2.width, box_2.height * 0.90])
        self.__plot_ax_2.set_facecolor('None')
        self.__plot_ax_2.set_ylim(ymax=1)
        self.__plot_ax_2.set_title("Moments")
        self.__plot_ax_2.set_ylabel("Moments [Nm]")
        self.__plot_ax_2.set_xlabel("Time(s)/Iterations")
        self.__plot_ax_2.yaxis.set_label_position("right")
        self.__plot_ax_2.grid(True)
        self.__plot_ax_2.set_autoscale_on(True)

    def __update_plot_scale(self):
        # Plot 1 (Forces)
        # ===============
        self.__plot_ax.legend(loc='upper center',
                              bbox_to_anchor=(0.5, -0.10), ncol=2)
        self.__plot_ax.relim(visible_only=True)
        self.__plot_ax.autoscale_view(True, True, True)

        # Plot 2 (Moments)
        # ================
        self.__plot_ax_2.legend(loc='upper center',
                                bbox_to_anchor=(0.5, -0.10), ncol=2)
        self.__plot_ax_2.relim(visible_only=True)
        self.__plot_ax_2.autoscale_view(True, True, True)

    def finalize_plot(self):
        """
        Execute plot at the end because of the plot interval in draw_plot
        and save data.
        """
        # print("--->>Finalizing", self)
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
