import os
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

from dice_tools import *
from dice_tools.helpers.xmodel import *


class CellZone:

    def __init__(self, app, name):
        super().__init__()
        self.app = app
        self.__name = name

    @modelRole('name')
    def name(self):
        return self.__name


class CellZonesApp:

    def __init__(self):
        super().__init__()
        self.__cell_zone_model = standard_model(CellZone)

    @property
    def path(self):
        return "foam:constant/polyMesh/cellZones"

    @diceProperty('QVariant', name='cellZoneModel')
    def cell_zone_model(self):
        return self.__cell_zone_model

    def load_cell_zone_model(self):
        self.__cell_zone_model.root_elements.clear()

        cell_zone_file_path = self.config_path("constant",
                                               "polyMesh", "cellZones")

        if os.path.exists(cell_zone_file_path):
            cell_zone_file = ParsedParameterFile(
                cell_zone_file_path, listDictWithHeader=True)
            if len(cell_zone_file) > 1:
                for name in cell_zone_file[1]:
                    if isinstance(name, str):
                        self.__cell_zone_model.root_elements.append(CellZone(self, name))