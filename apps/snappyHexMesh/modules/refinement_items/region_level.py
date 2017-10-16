from dice_tools import wizard
from dice_tools.helpers.xmodel import modelRole, modelMethod

class RegionLevel:

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.__data = data

    @modelRole('data')
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data[:] = [value[0], int(value[1])]
        wizard.w_modified('snappy_hex_mesh_dict')



