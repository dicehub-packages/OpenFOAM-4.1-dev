from .refinement_object import RefinementObject
from dice_vtk.geometries import Plane


class SearchablePlanePaN(RefinementObject):

    default_region_mode = "distance"
    region_modes_list = ["distance"]

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.setup()

    @property
    def template_name(self):
        return "refinementPlanePaN"

    def create_vis(self):
        vis = Plane()
        vis.opacity = 0.5
        vis.color = (.2, .8, .2)
        return vis

    def setup(self):
        self.vtk_obj.center = self.basePoint
        self.vtk_obj.normal = self.normal

    @property
    def basePoint(self):
        return list(self.app[self.object_path + ' pointAndNormalDict basePoint'])

    @basePoint.setter
    def basePoint(self, value):
        self.app[self.object_path + ' pointAndNormalDict basePoint'] = value
        self.setup()

    @property
    def normal(self):
        return list(self.app[self.object_path + ' pointAndNormalDict normalVector'])

    @normal.setter
    def normal(self, value):
        self.app[self.object_path + ' pointAndNormalDict normalVector'] = value
        self.setup()
