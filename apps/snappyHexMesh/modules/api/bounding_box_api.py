
from .api import Api

class BoundingBoxApi(Api):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.__app = app

    @property
    def min_x(self):
        '''minimum X of bounding box'''
        return self.__app.bounding_box.bb_min[0]

    @min_x.setter
    def min_x(self, value):
        v = self.__app.bounding_box.bb_min[:]
        v[0] = value
        self.__app.bounding_box.bb_min = v

    @property
    def min_y(self):
        '''minimum Y of bounding box'''
        return self.__app.bounding_box.bb_min[1]

    @min_y.setter
    def min_y(self, value):
        v = self.__app.bounding_box.bb_min[:]
        v[1] = value
        self.__app.bounding_box.bb_min = v

    @property
    def min_z(self):
        '''minimum Z of bounding box'''
        return self.__app.bounding_box.bb_min[2]

    @min_z.setter
    def min_z(self, value):
        v = self.__app.bounding_box.bb_min[:]
        v[2] = value
        self.__app.bounding_box.bb_min = v

    @property
    def max_x(self):
        '''maximum X of bounding box'''
        return self.__app.bounding_box.bb_max[0]

    @max_x.setter
    def max_x(self, value):
        v = self.__app.bounding_box.bb_max[:]
        v[0] = value
        self.__app.bounding_box.bb_max = v

    @property
    def max_y(self):
        '''maximum Y of bounding box'''
        return self.__app.bounding_box.bb_max[1]

    @max_y.setter
    def max_y(self, value):
        v = self.__app.bounding_box.bb_max[:]
        v[1] = value
        self.__app.bounding_box.bb_max = v

    @property
    def max_z(self):
        '''maximum Z of bounding box'''
        return self.__app.bounding_box.bb_max[2]

    @max_z.setter
    def max_z(self, value):
        v = self.__app.bounding_box.bb_max[:]
        v[2] = value
        self.__app.bounding_box.bb_max = v

    @property
    def cell_size_x(self):
        '''cell size by X of bounding box'''
        return self.__app.bounding_box.cells_size[0]

    @cell_size_x.setter
    def cell_size_x(self, value):
        v = self.__app.bounding_box.cells_size[:]
        v[0] = value
        self.__app.bounding_box.cells_size = v

    @property
    def cell_size_y(self):
        '''cell size by Y of bounding box'''
        return self.__app.bounding_box.cells_size[1]

    @cell_size_y.setter
    def cell_size_y(self, value):
        v = self.__app.bounding_box.cells_size[:]
        v[1] = value
        self.__app.bounding_box.cells_size = v

    @property
    def cell_size_z(self):
        '''cell size by Z of bounding box'''
        return self.__app.bounding_box.cells_size[2]

    @cell_size_z.setter
    def cell_size_z(self, value):
        v = self.__app.bounding_box.cells_size[:]
        v[2] = value
        self.__app.bounding_box.cells_size = v

    @property
    def cells_num_x(self):
        '''cells number by X of bounding box'''
        return self.__app.bounding_box.cells_num[0]

    @cells_num_x.setter
    def cells_num_x(self, value):
        v = self.__app.bounding_box.cells_num[:]
        v[0] = value
        self.__app.bounding_box.cells_num = v

    @property
    def cells_num_y(self):
        '''cells number by Y of bounding box'''
        return self.__app.bounding_box.cells_num[1]

    @cells_num_y.setter
    def cells_num_y(self, value):
        v = self.__app.bounding_box.cells_num[:]
        v[1] = value
        self.__app.bounding_box.cells_num = v

    @property
    def cells_num_z(self):
        '''cells number by Z of bounding box'''
        return self.__app.bounding_box.cells_num[2]

    @cells_num_z.setter
    def cells_num_z(self, value):
        v = self.__app.bounding_box.cells_num[:]
        v[2] = value
        self.__app.bounding_box.cells_num = v

    @property
    def use_cell_size(self):
        '''use cell size for calculating cells number bounding box'''
        return self.__app.bounding_box.use_cell_size

    @use_cell_size.setter
    def use_cell_size(self, value):
        self.__app.bounding_box.use_cell_size = value
