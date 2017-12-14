from .refinement_object import RefinementObject
from dice_vtk.geometries import Plane
from dice_tools.helpers.xmodel import modelRole


class SearchablePlane3P(RefinementObject):

    default_region_mode = "distance"
    region_modes_list = ["distance"]

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.setup()

    @modelRole('templateName')
    def template_name(self):
        return "refinementPlane3P"

    def create_vis(self):
        vis = Plane()
        vis.opacity = 0.5
        vis.color = (.2, .8, .2)
        return vis

    def setup(self):
        self.vtk_obj.origin = self.point1
        self.vtk_obj.point1 = self.point2
        self.vtk_obj.point2 = self.point3

    @property
    def point1(self):
        return list(self.app[self.object_path + ' embeddedPointsDict point1'])

    @point1.setter
    def point1(self, value):
        self.app[self.object_path + ' embeddedPointsDict point1'] = value
        self.setup()

    @property
    def point2(self):
        return list(self.app[self.object_path + ' embeddedPointsDict point2'])

    @point2.setter
    def point2(self, value):
        self.app[self.object_path + ' embeddedPointsDict point2'] = value
        self.setup()

    @property
    def point3(self):
        return list(self.app[self.object_path + ' embeddedPointsDict point3'])

    @point3.setter
    def point3(self, value):
        self.app[self.object_path + ' embeddedPointsDict point3'] = value
        self.setup()
