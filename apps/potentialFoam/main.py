from dice_vtk import VisApp

from dice_tools import *
from dice_tools.helpers.xmodel import *
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile, ParsedBoundaryDict
from PyFoam.Basics.DataStructures import Field, Vector, DictProxy
from dice_tools.helpers import FileOperations, JsonOrderedDict, run_process
from dice_vtk.utils.foam_reader import FoamReader
from dice_plot.plot import Plot
import matplotlib.pyplot as plt
import re

import os
import shutil
import random
import yaml
from common.foam_app import FoamApp
from common.boundary_model import *
from common.foam_result import Result
from common.basic_app import BasicApp


class potentialFoamApp(
    Application,
    VisApp,
    FoamApp,
    BasicApp,
    BoundaryApp
    ):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__load_config_files()

        self.__plot = Plot(plt.figure())
        self.__plot_ax = self.__plot.figure.add_subplot(111)
        self.__plot.figure.patch.set_alpha(0)
        self.__plot_ax.set_axis_bgcolor('white')
        self.__plot_data = [[],[]]

    @diceProperty('QVariant')
    def plot(self):
        return self.__plot


    def input_changed(self, input_data):
        """
        Loads input from other applications.
        """

        boundary_props = {
            'foam:0/p boundaryField':{
                    'type': 'fixedValue',
                    'value': Field(0)
                },
            'foam:0/U boundaryField': {
                    "type": "fixedValue",
                    "value": Field(Vector(0, 0, 0))
                }
        }

        self.load_boundary(boundary_props, input_data)


    def __load_config_files(self):
        """
        Loads config files for OpenFOAM with FoamParser.
        """
        # Parsed configuration files
        # ==========================

        p_dict = ParsedParameterFile(self.config_path('0/p'))
        U_dict = ParsedParameterFile(self.config_path('0/U'))
        control_dict = ParsedParameterFile(self.config_path('system/controlDict'))
        fv_solutions = ParsedParameterFile(self.config_path('system/fvSolution'))

        control_dict = ParsedParameterFile(
            self.config_path('system/controlDict')
        )

        # Registered files
        # ================
        self.foam_file('0/p', p_dict)
        self.foam_file('0/U', U_dict)
        self.foam_file('system/controlDict', control_dict)
        self.foam_file('system/fvSolution', fv_solutions)
        self.foam_file('system/controlDict', control_dict)

    @diceTask('prepare')
    def prepare(self):
        """
        Copy all necessary folders for running potentialFoam
        :return:
        """
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
        cmd_name = args[0] 
        cmd_pattern = self.__cmd_pattern
        run_kwargs = {
            'stdout': self.log,
            'stderr': self.log
        }
        run_kwargs.update(kwargs)
        result = run_process(command=cmd_pattern, 
            format_kwargs=params,
            cwd=self.workflow_path(),
            log_cmd_name=cmd_name,
            stop=lambda: self.running
            **run_kwargs)
        return result


    @prepare.after('potentialFoam')
    def run_potentialFoam(self):
        self.read_settings()
        application = self['foam:system/controlDict application']
        return 0 == self.execute_command(
                application,
                # "-withFunctionObjects", "-writep",
                "-case",
                self.run_path(relative=True),
                stdout=self.plot_log
            )

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

    def plot_log(self, line):
        # reg-expression:
        # ===============
        # ^  : assert position at start of the string
        # () : capturing group
        # .+ : mathes any character (except newline), + : between one and unlimited times
        reg_expression="^(.+):  Solving for (.+), Initial residual = (.+), Final residual = (.+), No Iterations (.+)$"
        expression = re.compile(reg_expression)
        res = expression.match(line)
        if res is not None:
            linear_solver_name = res.groups()[0]
            field_var_name = res.groups()[1]
            init_residual = res.groups()[2]
            final_residual = res.groups()[3]
            iterations = res.groups()[4]
            self.final_residual = "{:.2e}".format(float(final_residual))

        time_reg_expression = "^Time = (.+)$"
        res_time = re.compile(time_reg_expression).match(line)
        if res_time is not None:
            self.time_value = res_time.groups()[0]

        self.log(line)