from .refinement_object import RefinementObject
# from dice_tools import wizard
from dice_tools.helpers.xmodel import modelRole
from dice_vtk.geometries import Plane


class SearchablePlate(RefinementObject):

    default_region_mode = "distance"
    region_modes_list = ["distance"]

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.setup()

    @modelRole('templateName')
    def template_name(self):
        return "refinementPlate"

    def create_vis(self):
        vis = Plane()
        vis.opacity = 0.5
        vis.color = (.2, .8, .2)
        return vis

    def setup(self):
        self.vtk_obj.origin = self.origin
        if self.span[2] == 0:
            self.vtk_obj.point1 = [self.origin[0] + self.span[0], self.origin[1], 0]
            self.vtk_obj.point2 = [self.origin[0], self.origin[1] + self.span[1], 0]
        elif self.span[1] == 0:
            self.vtk_obj.point1 = [self.origin[0] + self.span[0], 0, self.origin[0]]
            self.vtk_obj.point2 = [self.origin[0], 0, self.origin[2] + self.span[2]]
        elif self.span[0] == 0:
            self.vtk_obj.point1 = [0, self.origin[1] + self.span[1], self.origin[2]]
            self.vtk_obj.point2 = [0, self.origin[1], self.origin[2] + self.span[2]]

    @property
    def origin(self):
        return list(self.app[self.object_path + ' origin'])

    @origin.setter
    def origin(self, value):
        self.app[self.object_path + ' origin'] = value
        self.setup()

    @property
    def span(self):
        return list(self.app[self.object_path + ' span'])

    @span.setter
    def span(self, value):
        self.app[self.object_path + ' span'] = value
        self.setup()