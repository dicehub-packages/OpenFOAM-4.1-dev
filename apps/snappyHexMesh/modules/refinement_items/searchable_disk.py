from .refinement_object import RefinementObject
from dice_vtk.geometries import Disk


class SearchableDisk(RefinementObject):

    default_region_mode = "distance"
    region_modes_list = ["distance"]

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.setup()

    @property
    def template_name(self):
        return "refinementDisk"

    def create_vis(self):
        vis = Disk()
        vis.opacity = 0.5
        vis.color = (.2, .8, .2)
        return vis

    def setup(self):
        self.vtk_obj.circumferential_resolution = 50
        self.vtk_obj.position = self.origin
        self.vtk_obj.normal = self.normal
        self.vtk_obj.inner_radius = 0
        self.vtk_obj.outer_radius = self.radius

    @property
    def origin(self):
        return list(self.app[self.object_path + ' origin'])

    @origin.setter
    def origin(self, value):
        self.app[self.object_path + ' origin'] = value
        self.setup()

    @property
    def normal(self):
        return list(self.app[self.object_path + ' normal'])

    @normal.setter
    def normal(self, value):
        self.app[self.object_path + ' normal'] = value
        self.setup()

    @property
    def radius(self):
        return self.app[self.object_path + ' radius']

    @radius.setter
    def radius(self, value):
        self.app[self.object_path + ' radius'] = value
        self.setup()
