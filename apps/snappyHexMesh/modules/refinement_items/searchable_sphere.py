from .refinement_object import RefinementObject
from dice_tools import wizard
from dice_tools.helpers.xmodel import modelRole, modelMethod
from dice_vtk.geometries import Sphere

class SearchableSphere(RefinementObject):

    default_region_mode = "inside"
    region_modes_list = ["inside", "outside"]

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.setup()

    @property
    def template_name(self):
        return "refinementSphere"

    def create_vis(self):
        vis = Sphere()
        vis.opacity = 0.5
        vis.color = (.2, .8, .2)
        return vis

    def setup(self):
        self.vtk_obj.position = self.centre
        self.vtk_obj.radius = self.radius

    @property
    def centre(self):
        return list(self.app[self.object_path + ' centre'])

    @centre.setter
    def centre(self, value):
        self.app[self.object_path + ' centre'] = value
        self.setup()

    @property
    def radius(self):
        return self.app[self.object_path + ' radius']

    @radius.setter
    def radius(self, value):
        self.app[self.object_path + ' radius'] = value
        self.setup()
