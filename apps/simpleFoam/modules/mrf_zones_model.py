from dice_tools import *
from dice_tools.helpers.xmodel import *

# from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


class MRFZone:
    """
    One MRF Zone specified in constant/MRFProperties.
    """

    def __init__(self, app, name):
        """
        :param app: main application
        :param name: name of the mrf zone specified in constant/MRFProperties
        file. <name>{ ... }
        """
        super().__init__()
        self.app = app
        self.__name = name

    @property
    def path(self):
        return "foam:constant/MRFProperties " + self.name


class MRFZonesApp:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__mrf_zones_model = standard_model(MRFZone)

    @property
    def path(self):
        return "foam:constant/MRFProperties"

    @diceProperty('QVariant', name='mrfZonesModel')
    def mrf_zones_model(self):
        return self.__mrf_zones_model

    def load_mrf_zones(self):
        self.__mrf_zones_model.root_elements.clear()
        self.__mrf_zones_model.root_elements.append(MRFZone(self, "test"))