from .refinement_object import RefinementObject
# from dice_tools import wizard
# from dice_tools.helpers.xmodel import modelRole, modelMethod
from dice_vtk.geometries import Tube


class SearchableCylinder(RefinementObject):

    default_region_mode = "inside"
    region_modes_list = ["inside", "outside"]

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.setup()

    @property
    def template_name(self):
        return "refinementCylinder"

    def create_vis(self):
        vis = Tube()
        vis.opacity = 0.5
        vis.color = (.2, .8, .2)
        return vis

    def setup(self):
        self.vtk_obj.point1 = self.point_1
        self.vtk_obj.point2 = self.point_2
        self.vtk_obj.radius = self.radius

    @property
    def point_1(self):
        return list(self.app[self.object_path + ' point1'])

    @point_1.setter
    def point_1(self, value):
        self.app[self.object_path + ' point1'] = value
        self.setup()

    @property
    def point_2(self):
        return list(self.app[self.object_path + ' point2'])

    @point_2.setter
    def point_2(self, value):
        self.app[self.object_path + ' point2'] = value
        self.setup()

    @property
    def radius(self):
        return self.app[self.object_path + ' radius']

    @radius.setter
    def radius(self, value):
        self.app[self.object_path + ' radius'] = value
        self.setup()
