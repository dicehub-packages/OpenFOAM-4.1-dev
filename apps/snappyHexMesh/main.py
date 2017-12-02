"""
snappyHexMesh
=============
DICE meshing app based on snappyHexMesh in OpenFOAM (http://www.openfoam.org)

Copyright (c) 2014-2017 by DICE Developers
All rights reserved.
"""

# External modules
# ================
import os
import sys
import shutil
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor

# External modules
# ================
import yaml

# App modules
# ============
from modules.refinement_items import Surface, SurfaceRegion

# DICE tools imports
# ==================
from dice_tools import Application, diceProperty, diceSignal, diceSlot, diceTask, diceSync
from dice_tools.helpers.xmodel import standard_model
from dice_tools import notify, wizard, app_settings, signal
from dice_tools.helpers import run_process

# DICE Libs
# =========
from dice_vtk import VisApp, VtkScene
from common.foam_app import FoamApp
from PyFoam.Basics.DataStructures import Vector
from modules.bounding_box import BoundingBox
from modules.material_point import MaterialPoint
from modules.refinement import Refinement
from common.foam_result import Result
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from time import time
from collections.abc import Sequence
from modules.api.app_api import AppApi
from common.basic_app import BasicApp


def logs_worker(line):
    wizard.w_log(line)


class snappyHexMesh(
    Application,
    BasicApp,
    FoamApp,
    VisApp
    ):

    """
    snappyHexMesh
    =============
    The snappyHexMesh utility generates 3-dimensional meshes containing
    hexahedra (hex) and split-hexahedra (split-hex) automatically from
    triangulated surface geometries in Stereolithography (STL) format.

    # Some folder conventions:
    # ========================
    # $WORKFLOW_DIR: Folder of the currently opened workflow
    # APP_DIR: Folder where the actual app is located
    # $APP_CONFIG_DIR: Folder with app config files
    # $APP_RUN_DIR: Folder where the actual commands are executed
    """
    def __init__(self, **kwargs):
        """
        Constructor of snappyHexMesh
        """
        super().__init__(**kwargs)

        self.__api = AppApi(self)

        # Load OpenFOAM config files
        # ==========================
        self.__load_config_files()

        self.__bounding_box = BoundingBox(self)
        self.__material_point = MaterialPoint(self)
        self.__refinement = Refinement(self)
        self.__result = Result(self)

        # Load short description
        # ======================
        self.__short_description = None
        self.__load_short_description()

        self.__modified_items = set()

        wizard.subscribe(self.w_idle)
        wizard.subscribe(self.w_modified)
        wizard.subscribe("w_log", self.__w_log)

        # Load input (STL)
        # ================
        self.__parameters = []
        self.__input_data = {}

        self.update_result()

    def execute_text(self, text):
        super().execute_text(text, self.api)

    @diceSlot('QString', name='getScript')
    def get_script(self, name):
        fname = self.config_path(name)
        if os.path.exists(fname):
            with open(fname) as f:
                return f.read()
        return ""

    @diceSlot('QString', 'QString', name='saveScript')
    def save_script(self, name, value):
        fname = self.config_path(name)
        if not value and os.path.exists(fname):
            os.unlink(fname)
        else:
            with open(fname, 'w') as f:
                f.write(value)

        if name == 'initialization.py':
            self.run_script(fname)

    def run_script(self, fname):
        if os.path.exists(fname):
            env = self.api
            try:
                try:
                    with open(fname) as f:
                     exec(f.read(), env)
                except NameError as e:
                    tb = sys.exc_info()[2]
                    if tb.tb_next and tb.tb_next.tb_next is None:
                        self.log("Error: %s\n"%e.args[0])
                        return False
                    else:
                        raise
            except:
                exc = traceback.format_exc(chain=False).split('\n')
                self.log("Error:\n%s\n"%'\n'.join(exc[:1]+exc[3:]))
                return False
            return True

    @property
    def api(self):
        return self.__api

    @diceProperty('QVariant', name='auto_load_result')
    def auto_load_result(self):
        return self.config['autoLoadResult']

    @auto_load_result.setter
    def auto_load_result(self, value):
        self.config['autoLoadResult'] = value
        self.update_result()

    @diceSlot(name='updateResult')
    def update_result(self):
        if self.auto_load_result:
            self.__result.update()

    def progress_changed(self, progress):
        super().progress_changed(progress)
        self.update_result()

    def save(self):
        if 'block_mesh_dict' in self.__modified_items:
            self._block_mesh_dict.writeFile()
        if 'snappy_hex_mesh_dict' in self.__modified_items:
            self._snappy_hex_mesh_dict.writeFile()
        if 'config' in  self.__modified_items:
            self.config.write()
        if 'surface_feature_extract_dict' in self.__modified_items:
            self._surface_feature_extract_dict.writeFile()
        if 'decompose_par_dict' in self.__modified_items:
            self._decompose_par_dict.writeFile()
        if self.__modified_items:
            self.__modified_items = set()

    def w_modified(self, *items):
        self.__modified_items |= set(items)

    def w_idle(self):
        self.save()

    @diceProperty('QVariant', name='boundingBox')
    def bounding_box(self):
        return self.__bounding_box

    @diceProperty('QVariant', name='materialPoint')
    def material_point(self):
        return self.__material_point

    @diceProperty('QVariant', name='refinement')
    def refinement(self):
        return self.__refinement

    @diceProperty('QVariant', name='result')
    def result(self):
        return self.__result

    def remove_stl(self, name):
        items = [
            'foam:system/snappyHexMeshDict castellatedMeshControls refinementRegions ',
            'foam:system/snappyHexMeshDict geometry ',
            'foam:system/snappyHexMeshDict castellatedMeshControls refinementSurfaces ',
            'foam:system/surfaceFeatureExtractDict '
        ]

        for v in items:
            self[v+name] = None

        file_name_e_mesh = '"{0}.eMesh"'.format(os.path.splitext(name)[0])
        for i, v in enumerate(
                self['foam:system/snappyHexMeshDict castellatedMeshControls features']):
            if v["file"] == file_name_e_mesh:
                self['foam:system/snappyHexMeshDict castellatedMeshControls features %i'%i] = None

    def input_changed(self, input_data):
        """
        Loads input from other applications.
        """
        self.debug("Loading input ..." + str(input_data))

        # before populate geometry clear current model

        for v in list(self.refinement.model.elements_of(Surface)):
            v.remove()

        # we need to initialize application input
        # to get current input get_input method shoul be used
        # get_input returns dictionary in following format:
        # {
        #   type_name: {
        #       from: value
        #   }
        # }
        # we expecting 'type_name' as 'stl_files' and list of
        # paths to stl files in 'value'
        # 'from' contains application instance id
        # which generates this input, useful to identity
        # data, previously saved from input

        self.__input_data = input_data

        # Get all Stl files
        # =================

        stl_input = self.__input_data.get('stl_files', {})
        for app, sources in stl_input.items():
            for file in sources:
                # Add every file to ModelItem Geometry
                # ====================================
                Surface(app=self, path=self.workflow_path(file))

        self.__clean_up()


        # Get parameters from input
        # =========================
        for parameters in self.__input_data.get('parameters', {}).values():
            self.__parameters = parameters
            break
        else:
            self.__parameters = []

        # Run custom initialization script
        self.run_script(self.config_path('initialization.py'))

    def __clean_up(self):
        """
        Clean up old stl files, refinement surfaces, features and layers.
        :return:
        """
        # Delete files which no longer exist in geometry
        for k, v in list(self['foam:system/snappyHexMeshDict geometry'].items()):
            if v.get('type') == 'triSurfaceMesh':
                for i in self.refinement.model.elements_of(Surface):
                    if i.name == k:
                        break
                else:
                    self.remove_stl(k)

        # Delete refinementSurfaces which have no corresponding geometry
        for k, v in list(self['foam:system/snappyHexMeshDict castellatedMeshControls refinementSurfaces'].items()):
            if k not in self['foam:system/snappyHexMeshDict geometry']:
                self['foam:system/snappyHexMeshDict castellatedMeshControls refinementSurfaces ' + k] = None

        # Delete features with no corresponding geometry
        geometry_names = [os.path.splitext(name)[0] for name in self['foam:system/snappyHexMeshDict geometry']]
        for i, v in enumerate(self['foam:system/snappyHexMeshDict castellatedMeshControls features']):
            if os.path.splitext(v["file"])[0] not in geometry_names:
                self['foam:system/snappyHexMeshDict castellatedMeshControls features %i'%i] = None
        feature_extract_dict_names = [name for name in self['foam:system/surfaceFeatureExtractDict']]
        for i, name in enumerate(self['foam:system/surfaceFeatureExtractDict']):
            print(i, name, name not in geometry_names)
            print(self['foam:system/surfaceFeatureExtractDict ' + name])
            if v not in geometry_names:
                self['foam:system/surfaceFeatureExtractDict ' + name] = None


        # Delete regions which no longer exist in stl files
        for k, v in list(self['foam:system/snappyHexMeshDict geometry'].items()):
            if v.get('type') == 'triSurfaceMesh':
                for kk, vv in list(v['regions'].items()):
                    for i in self.refinement.model.elements_of(SurfaceRegion):
                        if i.name == kk:
                            break
                    else:
                        del v['regions'][kk]

        # Delete layers for regions which no longer exist in stl files
        for k, v in list(self[
                             'foam:system/snappyHexMeshDict addLayersControls layers'].items()):
            for i in self.refinement.model.elements_of(SurfaceRegion):
                if i.name == k:
                    break
            else:
                self['foam:system/snappyHexMeshDict addLayersControls layers '+k] = None

    @property
    def parameters(self):
        return self.__parameters

    def __load_config_files(self):
        """
        Loads config files for OpenFOAM with FoamParser.
        """
        # Parsed configuration files
        # ==========================
        self._block_mesh_dict = ParsedParameterFile(
            self.config_path('system/blockMeshDict')
        )
        self._snappy_hex_mesh_dict = ParsedParameterFile(
            self.config_path('system/snappyHexMeshDict')
        )
        self.__mesh_quality_dict = ParsedParameterFile(
            self.config_path('system/meshQualityDict')
        )
        self._surface_feature_extract_dict = ParsedParameterFile(
            self.config_path('system/surfaceFeatureExtractDict')
        )
        self._decompose_par_dict = ParsedParameterFile(
            self.config_path('system/decomposeParDict')
        )
        self.__control_dict = ParsedParameterFile(
            self.config_path('system/controlDict')
        )

        self.foam_file('system/blockMeshDict', self._block_mesh_dict)
        self.foam_file('system/snappyHexMeshDict', self._snappy_hex_mesh_dict)
        self.foam_file('system/controlDict', self.__control_dict)
        self.foam_file('system/meshQualityDict', self.__mesh_quality_dict)
        self.foam_file('system/decomposeParDict', self._decompose_par_dict)
        self.foam_file('system/surfaceFeatureExtractDict', self._surface_feature_extract_dict)

    @diceSync('refinement:')
    def __refinement_sync(self, path):
        return self.refinement.refinement_get(path)

    @__refinement_sync.setter
    def __refinement_sync(self, path, value):
        return self.refinement.refinement_set(path, value)

    def __load_short_description(self):
        """
        Loads short description yaml file from the Overview-folder and sets
        the short description property.
        """
        with open(os.path.join("view", "config", "content", "1_Overview",
                               "description.yml")) as file:
            short_description = yaml.load(file)
            self.short_description = short_description["en"]

    '''
    QML Interface
    ===========================================================================
    '''

    # Short description
    # =================
    @diceProperty("QString", name="shortDescription")
    def short_description(self):
        """
        Property that describes the task of this application.
        :return: QString
        """
        return self.__short_description

    @short_description.setter
    def short_description(self, short_description):
        if self.__short_description != short_description:
            self.__short_description = short_description

    '''
    Main application control functions
    ==================================
    '''
    def pre_run_script_enabled(self):
        return os.path.exists(self.config_path('pre_run.py'))

    @diceTask('pre run script',
        enabled=pre_run_script_enabled)
    def pre_run_script(self):
        return self.run_script(self.config_path('pre_run.py'))

    # Prepare Application
    # ===================
    @diceTask('prepare', pre_run_script)
    def run_prepare(self):
        """
        Prepares the application for running procedure, i.e. copies all
        configuration files from config-folder to run-folder. Returns True
        if successfull.
        :return: True/False
        """
        # Save everything
        self.save()

        # Clear %APP_RUN in %WORKFLOW_DIR
        # ==================================
        self.clear_folder_content(self.run_path())

        # Copy "constant" and "system" - folder to %APP_RUN directory
        # ===========================================================
        self.copy_folder_content(self.config_path('constant'),
                                 self.run_path('constant'),
                                 overwrite=True)
        self.copy_folder_content(self.config_path('system'),
                                 self.run_path('system'),
                                 overwrite=True)

        os.mkdir(self.run_path('constant', 'triSurface'))
        for v in self.refinement.model.elements_of(Surface):
            shutil.copy(v.path, self.run_path('constant', 'triSurface'))

        # For paraview post-processing
        self.copy(self.config_path('p.foam'),
                  self.run_path())

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
        self.paraview_cmd = settings['paraview_cmd']
        return True

    def stop(self):
        if self.running and self.__use_docker:
            run_process('docker', 'rm', '-f', self.instance_id)
        super().stop()

    def execute_command(self, *args, allow_mpi = False):
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

        result = run_process(command=cmd_pattern,
            cwd=self.workflow_path(),
            stdout=self.print_log,
            stderr=self.print_log,
            format_kwargs=params,
            stop=self.stopped)

        return result

    @diceTask('surfaceFeatureExtract', run_prepare)
    def run_feature_extract(self):
        """ Execute surfaceFeatureExtract command. """
        self.read_settings()
        path = self.run_path(relative=True)
        if "win" in sys.platform and self.__use_docker:
            path = path.replace('\\', '/')
        return 0 == self.execute_command(
                "surfaceFeatureExtract",
                "-case",
                path
            )

    @diceTask('blockMesh', run_feature_extract)
    def run_block_mesh(self):
        """ Execute blockMesh command. """
        self.read_settings()
        path = self.run_path(relative=True)
        if "win" in sys.platform and self.__use_docker:
            path = path.replace('\\', '/')
        return 0 == self.execute_command(
                "blockMesh",
                "-case",
                path
            )

    def decompose_par_enabled(self):
        self.read_settings()
        return self.__use_mpi

    @diceTask('decomposePar', run_block_mesh,
        enabled=decompose_par_enabled)
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

    @diceTask('mesher', run_decompose_par)
    def run_mesher(self):
        """ Execute mesher command. """
        self.read_settings()
        mesher = self.__control_dict['application']
        path = self.run_path(relative=True)
        if "win" in sys.platform and self.__use_docker:
            path = path.replace('\\', '/')
        return 0 == self.execute_command(
                mesher,
                "-overwrite",
                "-case",
                path,
                allow_mpi = True
            )

    def reconstruct_par_mesh_enabled(self):
        self.read_settings()
        return self.__use_mpi

    @diceTask('reconstructParMesh', run_mesher,
        enabled=reconstruct_par_mesh_enabled)
    def run_reconstruct_par_mesh(self):
        """ Execute mesher command. """
        self.read_settings()
        path = self.run_path(relative=True)
        if "win" in sys.platform and self.__use_docker:
            path = path.replace('\\', '/')
        return 0 == self.execute_command(
                "reconstructParMesh",
                "-constant",
                "-fullMatch",
                "-case",
                path
            )

    @diceTask('cleanup', run_reconstruct_par_mesh)
    def run_cleanup(self):
        self.read_settings()
        if self.__use_mpi:
            for i in range(self.__cpu_count):
                self.rmtree(self.run_path("processor"+str(i)))
        self.set_output('foam_mesh', [self.run_path(relative=True)])
        return True

    def post_run_script_enabled(self):
        return os.path.exists(self.config_path('post_run.py'))

    @diceTask('post run script', run_cleanup, enabled=post_run_script_enabled)
    def post_run_script(self):
        return self.run_script(self.config_path('post_run.py'))

    def print_log(self, line):
        # self.log(line)
        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(logs_worker, line)

    def __w_log(self, line):
        self.log(line, callback=None)
