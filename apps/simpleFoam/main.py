from dice_vtk import VisApp

from dice_tools import *
from dice_tools.helpers.xmodel import *
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile, ParsedBoundaryDict
from PyFoam.Basics.DataStructures import Field, Vector, DictProxy
from dice_tools.helpers import FileOperations, JsonOrderedDict, run_process

from dice_plot.plot import Plot
import matplotlib.pyplot as plt
import re

import os
import shutil
import random
import yaml
import sys

from common.foam_app import FoamApp
from common.boundary_model import *
from common.foam_result import Result
from common.basic_app import BasicApp

import time

class potentialFoamApp(
    Application,
    VisApp,
    FoamApp,
    BasicApp,
    BoundaryApp
    ):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__plot = Plot(plt.figure())
        self.__plot_ax = self.__plot.figure.add_subplot(111)
        self.__plot.figure.patch.set_alpha(0)
        self.__plot_ax.set_axis_bgcolor('white')
        self.__plot_ax.set_title('Residuals')
        self.__plot_data = {}
        self.__plot_time = 0

        self.__load_config_files()


        self.__result = Result(self)
        self.update_result()
 
    def update_result(self):
        self.__result.update()

    @diceProperty('QVariant', name='result')
    def result(self):
        return self.__result

    def progress_changed(self, progress):
        super().progress_changed(progress)
        self.update_result()

    @diceProperty('QVariant')
    def plot(self):
        return self.__plot

    turbulence_model_changed = diceSignal(name='turbulenceModelChanged')

    @diceProperty('QString', name='turbulenceModel',  notify=turbulence_model_changed)
    def turbulence_model(self):
        if not self["foam:constant/turbulenceProperties RAS turbulence"]:
            return "none"
        return self["foam:constant/turbulenceProperties RAS RASModel"]

    @turbulence_model.setter
    def turbulence_model(self, value):
        if self.turbulence_model != value:
            if value == "none":
                self["foam:constant/turbulenceProperties RAS turbulence"] = False
            else:
                self["foam:constant/turbulenceProperties RAS turbulence"] = True
                self["foam:constant/turbulenceProperties RAS RASModel"] = value
            self.turbulence_model_changed()

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
                },
            'foam:0/k boundaryField': {
                    "type": "turbulentIntensityKineticEnergyInlet",
                    "value": Field(1.0),
                    "intensity": 0.05
                },
            'foam:0/nut boundaryField': {
                    "type": "calculated",
                    "value": Field(1.0)
                },
            'foam:0/omega boundaryField': {
                    "type": "turbulentMixingLengthFrequencyInlet",
                    "value": Field(1.0),
                    "mixingLength": 0.001
                },
            'foam:0/epsilon boundaryField': {
                    "type": "turbulentMixingLengthDissipationRateInlet",
                    "value": Field(1.0),
                    "mixingLength": 0.001
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

        k_dict = ParsedParameterFile(self.config_path('0/k'))
        omega_dict = ParsedParameterFile(self.config_path('0/omega'))
        nut_dict = ParsedParameterFile(self.config_path('0/nut'))
        epsilon_dict = ParsedParameterFile(self.config_path('0/epsilon'))
        fv_schemes = ParsedParameterFile(self.config_path('system/fvSchemes'))
        control_dict = ParsedParameterFile(self.config_path('system/controlDict'))
        fv_solutions = ParsedParameterFile(self.config_path('system/fvSolution'))

        control_dict = ParsedParameterFile(
            self.config_path('system/controlDict')
        )

        transport_props = ParsedParameterFile(
            self.config_path('constant/transportProperties')
        )

        turbulence_props = ParsedParameterFile(
            self.config_path('constant/turbulenceProperties')
        )

        # Registered files
        # ================
        self.foam_file('0/p', p_dict)
        self.foam_file('0/U', U_dict)
        self.foam_file('0/k', k_dict)
        self.foam_file('0/nut', nut_dict)
        self.foam_file('0/omega', omega_dict)
        self.foam_file('0/epsilon', epsilon_dict)
        

        self.foam_file('system/controlDict', control_dict)
        self.foam_file('system/fvSolution', fv_solutions)
        self.foam_file('system/fvSchemes', fv_schemes)
        self.foam_file('system/controlDict', control_dict)
        
        self.foam_file('constant/transportProperties', transport_props)
        self.foam_file('constant/turbulenceProperties', turbulence_props)


    @diceTask('prepare')
    def prepare(self):
        """
        Copy all necessary folders for running potentialFoam
        :return:
        """
        self.__plot_data = {}
        self.final_residual = {}
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

        params = dict(dice_workflow=self.workflow_path(),
                user=os.environ.get('USER'),
                user_name=os.environ.get('USERNAME'),
                command = ' '.join(args))

        if "win" not in sys.platform:
            params['user_id'] = os.getuid()

        run_kwargs = {
            'stdout': self.log,
            'stderr': self.log
        }
        run_kwargs.update(kwargs)

        result = run_process(command=cmd_pattern, 
            format_kwargs=params,
            cwd=self.workflow_path(),
            stop=lambda: not self.running,
            **run_kwargs)
        return result


    @prepare.after('simpleFoam')
    def run_simpleFoam(self):
        self.read_settings()
        application = self.control_dict['application']
        path = self.run_path(relative=True)
        if "win" in sys.platform and self.__use_docker:
            path = path.replace('\\', '/')
        return 0 == self.execute_command(
                application,
                # "-withFunctionObjects", "-writep",
                "-case",
                path,
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
        if material is not None:
            self['foam:constant/transportProperties nu 2'] = material['kinematicViscosity']

    def draw_plot(self, force = False):
        now = time.time()
        if force or (now - self.__plot_time) > 0.5:
            self.__plot_ax.cla()
            for k, v in self.__plot_data.items():
                self.__plot_ax.plot(*v, label=k)
            self.__plot_ax.legend(loc='upper right')
            self.__plot.draw()
            self.__plot_time = now

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
            self.final_residual[field_var_name] = float(final_residual)

        time_reg_expression = "^Time = (.+)$"
        res_time = re.compile(time_reg_expression).match(line)
        if res_time is not None:
            for k, v in self.final_residual.items():
                if k not in self.__plot_data:
                    self.__plot_data[k] = [[],[]]
                self.__plot_data[k][0].append(self.time_value)
                self.__plot_data[k][1].append(v)
                self.draw_plot()
            self.time_value = float(res_time.groups()[0])