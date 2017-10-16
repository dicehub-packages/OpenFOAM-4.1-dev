
from .api import Api

class MaterialPointApi(Api):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.__app = app

    @property
    def location_x(self):
        '''material point's location by X'''
        return self.__app.material_point.location[0]

    @location_x.setter
    def location_x(self, value):
        v = self.__app.material_point.location[:]
        v[0] = value
        self.__app.material_point.location = v

    @property
    def location_y(self):
        '''material point's location by Y'''
        return self.__app.material_point.location[1]

    @location_y.setter
    def location_y(self, value):
        v = self.__app.material_point.location[:]
        v[1] = value
        self.__app.material_point.location = v

    @property
    def location_z(self):
        '''material point's location by Z'''
        return self.__app.material_point.location[2]

    @location_z.setter
    def location_z(self, value):
        v = self.__app.material_point.location[:]
        v[2] = value
        self.__app.material_point.location = v
