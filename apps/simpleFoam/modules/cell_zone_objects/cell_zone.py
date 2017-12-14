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