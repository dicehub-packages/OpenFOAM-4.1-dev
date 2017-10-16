
from .refinement_object_api import RefinementObjectApi

class SearchableBoxApi(RefinementObjectApi):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def min_x(self):
        return self._instance.min[0]

    @min_x.setter
    def min_x(self, value):
        v = self._instance.min[:]
        v[0] = value
        self._instance.min = v

    @property
    def min_y(self):
        return self._instance.min[1]

    @min_y.setter
    def min_y(self, value):
        v = self._instance.min[:]
        v[1] = value
        self._instance.min = v

    @property
    def min_z(self):
        return self._instance.min[2]

    @min_z.setter
    def min_z(self, value):
        v = self._instance.min[:]
        v[2] = value
        self._instance.min = v

    @property
    def max_x(self):
        return self._instance.max[0]

    @max_x.setter
    def max_x(self, value):
        v = self._instance.max[:]
        v[0] = value
        self._instance.max = v

    @property
    def max_y(self):
        return self._instance.max[1]

    @max_y.setter
    def max_y(self, value):
        v = self._instance.max[:]
        v[1] = value
        self._instance.max = v

    @property
    def max_z(self):
        return self._instance.max[2]

    @max_z.setter
    def max_z(self, value):
        v = self._instance.max[:]
        v[2] = value
        self._instance.max = v