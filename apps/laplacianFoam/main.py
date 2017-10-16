"""
laplacianFoam
=============
Solver app based on laplacianFoam in OpenFOAM (http://www.openfoam.org)

Copyright (c) 2014-2017 by DICE Developers
All rights reserved.
"""

from dice_vtk import VisApp

from dice_tools import *
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from dice_tools.helpers import run_process
from dice_plot.plot import Plot
import matplotlib.pyplot as plt
import re

import time
import os
import shutil
import random
import yaml

from common.foam_app import FoamApp
from common.boundary_model import *
from common.foam_result import Result
from common.basic_app import BasicApp

class laplacianFoam(
    Application,
    VisApp,
    FoamApp,
    BasicApp,
    BoundaryApp
    ):

    """
    laplacianFoam
    =============
    LaplacianFoam solver solves the Laplace equation for unsteady, isotropic
    diffusion.
    """
    def __init__(self, **kwargs):
        """
        Constructor of laplacianFoam
        """
        super().__init__(**kwargs)

        self.__load_config_files()
        self.__plot = Plot(plt.figure())
        self.__plot_ax = self.__plot.figure.add_subplot(111)
        self.__plot.figure.patch.set_alpha(0)
        self.__plot_ax.set_axis_bgcolor('white')
        self.__plot_ax.set_title('Residuals')
        self.__plot_data = [[],[]]
        self.__plot_time = 0

        self.__result = Result(self)
        self.update_result()
        wizard.subscribe(self.w_foam)

    def w_foam(self, path):
        if path[0] == 'system/controlDict':
            self.copy(self.config_path('system', 'controlDict'),
                self.run_path('system', 'controlDict'))

    @diceProperty('QVariant')
    def plot(self):
        return self.__plot

    def input_changed(self, input_data):
        """
        Loads input from other applications.
        """
        boundary_props = {
            'foam:0/T boundaryField':{
                    "type": "fixedValue",
                    "value": Field(0)
                }
        }
        self.load_boundary(boundary_props, input_data)

    def __load_config_files(self):
        """
        Loads config files for OpenFOAM with FoamParser.
        """
        # Parsed configuration files
        # ==========================
        T_dict = ParsedParameterFile(self.config_path('0/T'))
        fv_solutions = ParsedParameterFile(self.config_path('system/fvSolution'))
        fv_schemes = ParsedParameterFile(self.config_path('system/fvSchemes'))
        control_dict = ParsedParameterFile(self.config_path('system/controlDict'))
        transport_props = ParsedParameterFile(self.config_path('constant/transportProperties'))

        # Registered files
        # ================
        self.foam_file('0/T', T_dict)
        self.foam_file('system/controlDict', control_dict)
        self.foam_file('system/fvSolution', fv_solutions)
        self.foam_file('system/fvSchemes', fv_schemes)
        self.foam_file('system/controlDict', control_dict)
        self.foam_file('constant/transportProperties', transport_props)

    @diceTask('prepare')
    def prepare(self):
        """
        Copy all necessary folders for running potentialFoam
        :return:
        """
        self.__plot_data = [[], []]
        self.final_residual = None
        self.time_value = None
        self.clear_folder_content(self.run_path())
        self.copy_folder_content(self.config_path('system'), self.run_path('system'), overwrite=True)
        self.copy_folder_content(self.config_path('constant'), self.run_path('constant'), overwrite=True)
        self.copy_folder_content(self.config_path('0'), self.run_path('0'), overwrite=True)
        return True

    def read_settings(self):
        """ Initialize run parameters. """
        settings = app_settings()
        self.__use_docker = settings['use_docker']
        if self.__use_docker:
            self.__cmd_pattern = settings['docker_cmd']
        else:
            self.__cmd_pattern = settings['foam_cmd']
        return True

    def execute_command(self, *args, **kwargs):
        args = list(args)
        # cmd_name = args[0] 
        cmd_pattern = self.__cmd_pattern
        cmd = cmd_pattern.format(
                dice_workflow=self.workflow_path(),
                user=os.environ.get('USER'),
                user_name=os.environ.get('USERNAME'),
                user_id=os.getuid(),
                command = ' '.join(args)
            )

        run_kwargs = {
            'stdout': self.log,
            'stderr': self.log
        }
        run_kwargs.update(kwargs)
        print('cmd', cmd)
        result = run_process(cmd, 
            cwd=self.workflow_path(),
            stop=lambda: not self.running,
            **run_kwargs)
        return result

    @prepare.after('laplacianFoam')
    def run_laplacianFoam(self):
        self.read_settings()
        application = self.control_dict['application']
        result = 0 == self.execute_command(
                application,
                "-case",
                self.run_path(relative=True),
                stdout=self.plot_log
            )
        self.draw_plot(True)
        return result

    def draw_plot(self, force = False):
        now = time.time()
        if force or (now - self.__plot_time) > 0.5:
            self.__plot_ax.cla()
            self.__plot_ax.plot(*self.__plot_data, c='black', label='T')
            self.__plot_ax.legend(loc='upper left')
            self.__plot.draw()
            self.__plot_time = now

    @diceSlot(name='selectMaterial')
    def select_material(self):
        with open(os.path.join('library', 'materials.yaml')) as f:
            templates = [yaml.load(f)]
        path = os.path.join('library', 'materials')
        entities = []
        for v in os.listdir(path):
            with open(os.path.join(path, v)) as f:
                entities.append(yaml.load(f))
        material = browse_rdl(templates, entities)
        if material is not None:
            self.transport_props['DT'][2] = \
                material['thermalConductivity']/(material['density']*material['specificHeatCapacity'])
            signal('foam:constant/transportProperties*')

    def plot_log(self, line):
        # reg-expression:
        # ===============
        # ^  : assert position at start of the string
        # () : capturing group
        # .+ : mathes any character (except newline), + : between one and unlimited times
        
        self.log(line, callback = None)
        reg_expression="^(.+):  Solving for (.+), Initial residual = (.+), Final residual = (.+), No Iterations (.+)$"
        expression = re.compile(reg_expression)
        res = expression.match(line)
        if res is not None:
            linear_solver_name = res.groups()[0]
            field_var_name = res.groups()[1]
            init_residual = res.groups()[2]
            final_residual = res.groups()[3]
            iterations = res.groups()[4]
            self.final_residual = float(final_residual)

        time_reg_expression = "^Time = (.+)$"
        res_time = re.compile(time_reg_expression).match(line)
        if res_time is not None:
            if self.final_residual is not None:
                self.__plot_data[0].append(self.time_value)
                self.__plot_data[1].append(self.final_residual)
                self.draw_plot()
            self.time_value = float(res_time.groups()[0])

    def update_result(self):
        self.__result.update()

    @diceProperty('QVariant', name='result')
    def result(self):
        return self.__result

    def progress_changed(self, progress):
        super().progress_changed(progress)
        self.update_result()


