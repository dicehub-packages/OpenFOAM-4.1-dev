from .refinement_object import RefinementObject
from dice_tools import wizard
from dice_tools.helpers.xmodel import modelRole, modelMethod
from dice_vtk.geometries import Cube

class SearchableBox(RefinementObject):

    default_region_mode = "inside"
    region_modes_list = ["inside", "outside"]

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.setup()

    @property
    def template_name(self):
        return "refinementBox"

    def create_vis(self):
        vis = Cube()
        vis.opacity = 0.5
        vis.color = (.2, .8, .2)
        return vis

    def setup(self):
        vmin = self.min
        vmax = self.max
        self.vtk_obj.position = [(v[1] + v[0]) / 2.0 for v in zip(vmin, vmax)]
        self.vtk_obj.x_length, self.vtk_obj.y_length, self.vtk_obj.z_length = [v[1] - v[0] for v in zip(vmin, vmax)]

    @property
    def min(self):
        return list(self.app[self.object_path + ' min'])

    @min.setter
    def min(self, value):
        self.app[self.object_path + ' min'] = value
        self.setup()

    @property
    def max(self):
        return list(self.app[self.object_path + ' max'])

    @max.setter
    def max(self, value):
        self.app[self.object_path + ' max'] = value
        self.setup()
