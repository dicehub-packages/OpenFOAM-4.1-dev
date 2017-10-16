"""
ansysToFoam
=============
Conversion utility based on ansysToFoam utility in OpenFOAM (
http://www.openfoam.org)

Copyright (c) 2014-2017 by DICE Developers
All rights reserved.
"""

# Standard Python modules
# =======================
import os
import shutil

# External modules
# ================
import yaml
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

# App modules
# ============

# DICE tools imports
# ==================
from dice_tools import *
from dice_tools.helpers import run_process

# DICE Libs
# =========
from dice_foam import FoamApp
from common.foam_result import Result
from common.basic_app import BasicApp

class ansysToFoam(
    Application,
    FoamApp,
    BasicApp
    ):
    """
    ansysToFoam
    =============
    Converts an ANSYS input mesh file, exported from I-DEAS,
    to OpenFOAM format.
    """
    def __init__(self):
        """
        Constructor of ansysToFoam
        """
        super().__init__()
        self.__result = Result(self)
        self.update_result()
        self.__load_config_files()

    def __load_config_files(self):
        """
        Loads config files for OpenFOAM with FoamParser.
        """
        # Parsed configuration files
        # ==========================
        control_dict = ParsedParameterFile(self.config_path('system/controlDict'))

        # Registered files
        # ================
        self.foam_file('system/controlDict', control_dict)

    def update_result(self):
        self.__result.update()

    @diceProperty('QVariant', name='result')
    def result(self):
        return self.__result

    def progress_changed(self, progress):
        super().progress_changed(progress)
        self.update_result()

    ans_file_name_updated = diceSignal(name="ans_file_name")

    @diceProperty('QString', name='ansFileName',
                  notify=ans_file_name_updated)
    def ans_file_name(self):
        return os.path.basename(self.source_path)

    @diceProperty('QString', name='sourcePath')
    def source_path(self):
        if self.config['source_path']:
            return os.path.abspath(self.config['source_path'].format(
                workflow_dir = self.workflow_dir))
        return ""

    @source_path.setter
    def source_path(self, value):
        wf = self.workflow_path()
        pre = os.path.commonprefix((value, wf))
        if pre:
             value = os.path.join('{workflow_dir}',
                 os.path.relpath(value, wf))
        self.config['source_path'] = value
        self.config.write()
        self.ans_file_name_updated()

    @diceProperty('QVariant', name='scalingFactor')
    def scaling_factor(self):
        return self.config['scale']

    @scaling_factor.setter
    def scaling_factor(self, value):
        self.config['scale'] = float(value)
        self.config.write()

    @diceSync('config:')
    def __config_sync(self, path):
        return self.config[path]

    @__config_sync.setter
    def __config_sync(self, path, value):
        self.config[path]=value
        self.config.write()
        signal('config:*')
        return True

    @diceSlot("QString", name="addANS")
    def import_ans(self, files):
        notify("Importing file: ...." + str(files))
        if not isinstance(files, (list, tuple)):
            files = (files,)
        
        for fn in files:
            self.source_path = FileOperations.parse_url(fn)
            break

    @diceSlot(name="deleteImport")
    def delete_import(self):
        self.source_path = ''
        self.set_progress(0)
        self.set_output('foam_mesh', None)
        self.clear_folder_content(self.run_path())

    @diceTask('ansysToFoam')
    def run_ansys_to_foam(self):
        """ Execute conversion from Ansys to OpenFOAM """

        if not self.source_path:
            return False
        self.clear_folder_content(self.run_path())
        self.copy_folder_content(self.config_path('system'),
                                 self.run_path('system'),
                                 overwrite=True)

        settings = app_settings()

        use_docker = settings['use_docker']
        if use_docker:
            cmd_pattern = settings['docker_cmd']
            source = shutil.copy(self.source_path, self.run_path())
            source_path = self.run_path(os.path.basename(source), relative=True)
        else:
            cmd_pattern = settings['foam_cmd']
            source_path = self.source_path

        cmd = cmd_pattern.format(
            dice_workflow=self.workflow_path(),
            user=os.environ.get('USER'),
            user_name=os.environ.get('USERNAME'),
            user_id=os.getuid(),
            command = ' '.join(["ansysToFoam",
            "-scale",
            str(self.config["scale"]),
            "-case",
            self.run_path(relative=True),
            source_path])
        )

        result = run_process(cmd,
            cwd=self.workflow_path(),
            stdout=self.log,
            stderr=self.log,
            stop=lambda: not self.running)

        if use_docker:
            os.unlink(source)

        return result == 0

    @diceTask('checkMesh', run_ansys_to_foam)
    def run_check_mesh(self):
        """ Checks mesh for errors """
        settings = app_settings()
        use_docker = settings['use_docker']
        if use_docker:
            cmd_pattern = settings['docker_cmd']
        else:
            cmd_pattern = settings['foam_cmd']

        cmd = cmd_pattern.format(
            dice_workflow=self.workflow_path(),
            user=os.environ.get('USER'),
            user_name=os.environ.get('USERNAME'),
            user_id=os.getuid(),
            command=' '.join(["checkMesh",
            "-allTopology" if self.config['checkMesh.allTopology'] else "",
            "-allGeometry" if self.config['checkMesh.allGeometry'] else "",
            "-case",
            self.run_path(relative=True)])
        )
        print(cmd)

        result = run_process(cmd,
                             cwd=self.workflow_path(),
                             stdout=self.log,
                             stderr=self.log,
                             stop=lambda: not self.running)

        self.set_output('foam_mesh', [self.run_path(relative=True)])

        return result == 0
