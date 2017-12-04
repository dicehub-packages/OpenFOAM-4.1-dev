"""
simpleFoam
==========
DICE incomrepssible solver app based on steady-state solver for 
incompressible flows with turbulence modelling in OpenFOAM. 
(http://www.openfoam.org)

Copyright (c) 2014-2017 by DICE Developers
All rights reserved.
"""

# External modules
# ================
import os
import sys
from concurrent.futures import ThreadPoolExecutor

# External modules
# ================
import yaml
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile, ParsedBoundaryDict
from PyFoam.Basics.DataStructures import Field, Vector, DictProxy

# DICE Libs
# =========
from dice_vtk import VisApp
from dice_tools import *
from dice_tools.helpers.xmodel import *
from dice_tools.helpers import JsonOrderedDict, run_process

# Shared package libs
# ===================
from common.foam_app import FoamApp
from common.boundary_model import *
from common.foam_result import Result
from common.basic_app import BasicApp
from common.div_schemes_model import DivSchemesApp
from modules.cell_zones_model import CellZonesApp
from modules.function_objects_model import FunctionObjectsApp
from modules.plots_model import PlotsApp


def logs_worker(line):
    wizard.w_log(line)


class simpleFoamApp(
    Application,
    VisApp,
    FoamApp,
    BasicApp,
    CellZonesApp,
    DivSchemesApp,
    BoundaryApp
    ):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__load_config_files()

        self.__plots = PlotsApp(self)
        self.__function_objects = FunctionObjectsApp(self)
        self.__result = Result(self)

        wizard.subscribe(self.w_foam)
        # self.update_result()

        wizard.subscribe("w_log", self.__w_log)

    def w_foam(self, path):
        """
        Catch if controlDict and fvSolution are being changed during the run
        and write both to run and to config. Important so user can switch
        schemes or update relaxation factors during runtime.
        """
        updated_run_files = (
            "system/controlDict",
            "system/fvSolution"
        )
        for file_path in updated_run_files:
            if file_path in path:
                self.control_dict.writeFile()
                self.fv_solutions.writeFile()
                src = self.config_path(file_path)
                dst = self.run_path(file_path)
                self.copy(src, dst)

    @diceProperty('QVariant', name='auto_load_result')
    def auto_load_result(self):
        return self.config['autoLoadResult']

    @auto_load_result.setter
    def auto_load_result(self, value):
        if self.auto_load_result != value:
            self.config['autoLoadResult'] = value

    @diceSlot(name='updateResult')
    def update_result(self):
        if self.auto_load_result:
            self.__result.update()

    @diceProperty('QVariant', name='result')
    def result(self):
        return self.__result

    @diceProperty('QVariant', name='functionObjects')
    def function_objects(self):
        return self.__function_objects

    def progress_changed(self, progress):
        """
        Overrides progress function and if simpleFoam is finished load plot data.
        """
        super().progress_changed(progress)
        wizard.progress_changed(progress)
        self.update_result()

    @diceProperty('QVariant')
    def plots(self):
        return self.__plots

    turbulence_model_changed = diceSignal(name='turbulenceModelChanged')

    @diceProperty('QString', name='turbulenceModel', notify=turbulence_model_changed)
    def turbulence_model(self):
        if self["foam:constant/turbulenceProperties simulationType"] == "laminar":
            return "laminar"
        elif self["foam:constant/turbulenceProperties simulationType"] == "RAS":
            return self["foam:constant/turbulenceProperties RAS RASModel"]

    @turbulence_model.setter
    def turbulence_model(self, value):        
        if self.turbulence_model != value:
            if value == "laminar":
                self["foam:constant/turbulenceProperties simulationType"] = "laminar"
                self["foam:constant/turbulenceProperties RAS"] = {}
            elif value == "kOmegaSST":
                self["foam:constant/turbulenceProperties simulationType"] = "RAS"
                self["foam:constant/turbulenceProperties RAS"] = {
                         'RASModel': 'kOmegaSST',
                         'kOmegaSSTCoeffs': {
                            'F3': False,
                            'a1': 0.31,
                            'alphaK1': 0.85,
                            'alphaK2': 1.0,
                            'alphaOmega1': 0.5,
                            'alphaOmega2': 0.856,
                            'b1': 1.0,
                            'beta1': 0.075,
                            'beta2': 0.0828,
                            'betaStar': 0.09,
                            'c1': 10.0,
                            'gamma1': 0.5532,
                            'gamma2': 0.4403
                          },
                         'printCoeffs': True,
                         'turbulence': True
                     }
            elif value == "kEpsilon":
                self["foam:constant/turbulenceProperties simulationType"] = "RAS"
                self["foam:constant/turbulenceProperties RAS"] = {
                         'RASModel': 'kEpsilon',
                         'kEpsilonCoeffs': {
                            "Cmu": 0.09,
                            "C1": 1.44,
                            "C2": 1.92,
                            "C3": -0.33,
                            "sigmak": 1,
                            "sigmaEps": 1.3
                         },
                         'printCoeffs': True,
                         'turbulence': True
                     }
            self.turbulence_model_changed()
            wizard.w_turbulence_model_changed()

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
        self.load_schemes()
        self.load_cell_zone_model()
        self.load_mrf_zones()
        wizard.input_changed()

    def __load_config_files(self):
        """
        Loads config files for OpenFOAM with FoamParser.
        """
        # Parsed configuration files
        # ==========================

        # Main Fields
        p_dict = ParsedParameterFile(self.config_path('0/p'))
        U_dict = ParsedParameterFile(self.config_path('0/U'))

        # Turbulence model fields
        k_dict = ParsedParameterFile(self.config_path('0/k'))
        omega_dict = ParsedParameterFile(self.config_path('0/omega'))
        nut_dict = ParsedParameterFile(self.config_path('0/nut'))
        epsilon_dict = ParsedParameterFile(self.config_path('0/epsilon'))

        turbulence_props = ParsedParameterFile(
            self.config_path('constant/turbulenceProperties')
        )

        # Material values
        transport_props = ParsedParameterFile(
            self.config_path('constant/transportProperties')
        )

        # Controls
        fv_schemes = ParsedParameterFile(self.config_path('system/fvSchemes'))
        self.control_dict = ParsedParameterFile(self.config_path('system/controlDict'))
        self.fv_solutions = ParsedParameterFile(self.config_path('system/fvSolution'))
        self._decompose_par_dict = ParsedParameterFile(
            self.config_path('system/decomposeParDict')
        )

        # cellZone options
        self.mrf_props = ParsedParameterFile(
            self.config_path('constant/MRFProperties')
        )

        # Post-Processing
        self.function_objects_dict = ParsedParameterFile(
            self.config_path('system/functionObjects'),
            noHeader=True, preserveComments=False
        )

        # Registered files
        # ================
        self.foam_file('0/p', p_dict)
        self.foam_file('0/U', U_dict)
        self.foam_file('0/k', k_dict)
        self.foam_file('0/nut', nut_dict)
        self.foam_file('0/omega', omega_dict)
        self.foam_file('0/epsilon', epsilon_dict)
        
        self.foam_file('system/fvSolution', self.fv_solutions)
        self.foam_file('system/fvSchemes', fv_schemes)
        self.foam_file('system/controlDict', self.control_dict)
        self.foam_file('system/decomposeParDict', self._decompose_par_dict)

        self.foam_file('constant/transportProperties', transport_props)
        self.foam_file('constant/turbulenceProperties', turbulence_props)

        self.foam_file('constant/MRFProperties', self.mrf_props)
        self.foam_file('system/functionObjects', self.function_objects_dict)

    @diceSync('functionObjects:')
    def __function_objects_sync(self, path):
        return self.__function_objects.function_objects_get(path)

    @__function_objects_sync.setter
    def __function_objects_sync(self, path, value):
        return self.__function_objects.function_objects_set(path, value)

    @diceTask('prepare')
    def prepare(self):
        """
        Copy all necessary folders for running simpleFoam
        :return:
        """
        self.clear_folder_content(self.run_path())
        self.copy_folder_content(self.config_path('system'), self.run_path('system'), overwrite=True)
        self.copy_folder_content(self.config_path('constant'), self.run_path('constant'), overwrite=True)
        self.copy_folder_content(self.config_path('0'), self.run_path('0'), overwrite=True)
        self.copy(self.config_path('p.foam'), self.run_path())
        wizard.prepare()
        return True

    def read_settings(self):
        """ Initialize run parameters. """
        settings = app_settings()
        self.__use_docker = settings['use_docker']
        if self.__use_docker:
            self.__cmd_pattern_mpi = settings['docker_cmd_mpi']
            self.__cmd_pattern = settings['docker_cmd']
        else:
            self.__cmd_pattern_mpi = settings['foam_cmd_mpi']
            self.__cmd_pattern = settings['foam_cmd']
        self.__cpu_count = self._decompose_par_dict['numberOfSubdomains']
        self.__use_mpi = self.config['parallelRun']
        self.__use_potentialFoam = self.config['potentialFoam']
        return True

    def stop(self):
        if self.running and self.__use_docker:
            run_process('docker', 'rm', '-f', self.instance_id)
        super().stop()

    def execute_command(self, *args, allow_mpi=False, **kwargs):
        args = list(args)
        cmd_name = args[0] 
        if allow_mpi and self.__use_mpi:
            args.insert(1, '-parallel')
            args.insert(0, '-np %i'%self.__cpu_count)
            cmd_pattern = self.__cmd_pattern_mpi
        else:
            cmd_pattern = self.__cmd_pattern

        params = dict(dice_workflow=self.workflow_path(),
                docker_name=self.instance_id,
                user=os.environ.get('USER'),
                user_name=os.environ.get('USERNAME'),
                command=' '.join(args))
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
            stop=self.stopped,
            **run_kwargs)

        return result

    def decompose_par_enabled(self):
        self.read_settings()
        return self.__use_mpi

    @diceTask('decomposePar', prepare, enabled=decompose_par_enabled)
    def run_decompose_par(self):
        """ Execute decomposePar command. """
        path = self.run_path(relative=True)
        if "win" in sys.platform and self.__use_docker:
            path = path.replace('\\', '/')
        return 0 == self.execute_command(
                "decomposePar",
                "-force",
                "-case",
                path
            )

    def potentialFoam_enabled(self):
        self.read_settings()
        return self.__use_potentialFoam

    @diceTask('potentialFoam', run_decompose_par,
        enabled=potentialFoam_enabled)
    def run_potentialFoam(self):
        self.read_settings()
        path = self.run_path(relative=True)
        if "win" in sys.platform and self.__use_docker:
            path = path.replace('\\', '/')
        result = self.execute_command(
                "potentialFoam",
                "-case",
                path,
                allow_mpi=True
            )
        return result == 0

    @diceTask('postProcess', run_potentialFoam)
    def run_post_process(self):
        self.read_settings()
        path = self.run_path(relative=True)
        if "win" in sys.platform and self.__use_docker:
            path = path.replace('\\', '/')
        return 0 == self.execute_command(
                "postProcess",
                "-func",
                "\"mag(U)\"",
                "-case",
                path,
                allow_mpi=True
            )

    @diceTask('simpleFoam', run_post_process)
    def run_simpleFoam(self):
        self.read_settings()
        application = self['foam:system/controlDict application']
        path = self.run_path(relative=True)
        if "win" in sys.platform and self.__use_docker:
            path = path.replace('\\', '/')
        result = self.execute_command(
                application,
                "-case",
                path,
                stdout=self.plot_log,
                allow_mpi=True
            )
        wizard.finalize_plot()

        return result == 0

    def reconstruct_par_enabled(self):
        self.read_settings()
        return self.__use_mpi

    @diceTask('reconstructPar', run_simpleFoam,
        enabled=reconstruct_par_enabled)
    def run_reconstruct_par(self):
        """ Execute mesher command. """
        self.read_settings()
        path = self.run_path(relative=True)
        if "win" in sys.platform and self.__use_docker:
            path = path.replace('\\', '/')
        return 0 == self.execute_command(
                "reconstructPar",
                # "-latestTime",
                "-case",
                path,
                "-withZero"
            )

    @diceTask('cleanup', run_reconstruct_par)
    def run_cleanup(self):
        self.read_settings()
        if self.__use_mpi:
            for i in range(self.__cpu_count):
                self.rmtree(self.run_path("processor"+str(i)))
        self.set_output('foam_mesh', [self.run_path(relative=True)])
        return True

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

    def plot_log(self, line):
        self.log(line)
        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(logs_worker, line)

    def __w_log(self, line):
        # self.log(line, callback=None)
        pass

    @diceSlot(name="runCheckMesh")
    def run_check_mesh(self):
        self.read_settings()
        """ Execute checkMesh command. """
        path = self.run_path(relative=True)
        if "win" in sys.platform and self.__use_docker:
            path = path.replace('\\', '/')
        return 0 == self.execute_command(
                "checkMesh",
                "-case",
                path
        )