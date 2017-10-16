
from .refinement_object_api import RefinementObjectApi

class SearchableSphereApi(RefinementObjectApi):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def centre_x(self):
        return self._instance.centre[0]

    @centre_x.setter
    def centre_x(self, value):
        v = self._instance.centre[:]
        v[0] = value
        self._instance.centre = v

    @property
    def centre_y(self):
        return self._instance.centre[1]

    @centre_y.setter
    def centre_y(self, value):
        v = self._instance.centre[:]
        v[1] = value
        self._instance.centre = v

    @property
    def centre_z(self):
        return self._instance.centre[2]

    @centre_z.setter
    def centre_z(self, value):
        v = self._instance.centre[:]
        v[2] = value
        self._instance.centre = v

    @property
    def radius(self):
        return self._instance.radius

    @radius.setter
    def radius(self, value):
        self._instance.radius = value
