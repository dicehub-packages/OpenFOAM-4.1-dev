from dice_tools import *
from dice_tools.helpers.xmodel import *


class NonRotatingPatch:

    def __init__(self, app, name):
        super().__init__()
        self.app = app
        self.__name = name

    @modelRole('name')
    def name(self):
        return self.__name


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
    def name(self):
        return self.__name

    @property
    def path(self):
        return "foam:constant/MRFProperties " + self.name

    @modelRole('active')
    def active(self):
        return self.app[self.path + ' active']

    @active.setter
    def active(self, value):
        self.app[self.path + ' active'] = value

    @modelRole('origin')
    def origin(self):
        return self.app[self.path + ' origin']

    @origin.setter
    def origin(self, value):
        self.app[self.path + ' origin'] = value

    @modelRole('axis')
    def axis(self):
        return self.app[self.path + ' axis']

    @axis.setter
    def axis(self, value):
        self.app[self.path + ' axis'] = value

    @modelRole('omega')
    def omega(self):
        return self.app[self.path + ' omega']

    @omega.setter
    def omega(self, value):
        self.app[self.path + ' omega'] = value

    # Non rotating patches
    # ====================

    @modelRole('nonRotatingPatches')
    def non_rotating_patches(self):
        return self.app[self.path + ' nonRotatingPatches']

    @non_rotating_patches.setter
    def non_rotating_patches(self, value):
        self.app[self.path + ' nonRotatingPatches'] = value