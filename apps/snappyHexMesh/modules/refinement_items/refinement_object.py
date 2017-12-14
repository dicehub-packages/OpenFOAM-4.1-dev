from .region_refinement import RegionRefinement
from .surface_region import SurfaceRegion
from .surface import Surface
from dice_tools import wizard
from dice_tools.helpers.xmodel import modelRole, modelMethod, ModelItem


class RefinementObject(RegionRefinement):

    def __init__(self, name, app, **kwargs):
        super().__init__(**kwargs)
        self.__app = app
        self.__name = name
        self.vtk_obj = self.create_vis()
        self.vtk_obj.name = name
        self.app.vis_add_object(self.vtk_obj)
        wizard.subscribe(self, self.vtk_obj)
        self.setup_region(self.region_modes_list, self.default_region_mode)
        wizard.subscribe(self, self.vtk_obj)
        self.__load()
        wizard.w_refinement_created(self)

    @property
    def object_path(self):
        return 'foam:system/snappyHexMeshDict geometry '+self.name

    def w_geometry_object_clicked(self, obj, *args, **kwargs):
        self.app.refinement.model.current_item = self

    @property
    def app(self):
        return self.__app

    @property
    def name(self):
        return self.__name

    @modelRole('type')
    def type(self):
        return "RefinementObject"

    @modelMethod('remove')
    def remove_refinement(self):
        self.clear_region_levels()
        self.app[self.object_path] = None
        self.app[self.refinement_path] = None
        self.app.vis_remove_object(self.vtk_obj)
        wizard.w_refinement_removed(self)

    @modelRole('isVisible')
    def visible(self):
        return self.vtk_obj.visible
    
    @visible.setter
    def visible(self, value):
        self.vtk_obj.visible = value

    @modelMethod('showInScene')
    def show_in_scene(self):
        wizard.w_reset_camera_to_object([self.vtk_obj])

    @modelRole('label')
    def label(self):
        return self.name

    @property
    def refinement_path(self):
        return 'foam:system/snappyHexMeshDict castellatedMeshControls refinementSurfaces ' + self.name

    def __load(self):
        # if self.app[self.refinement_path] is None:
        #     self.app[self.refinement_path] = {
        #         'level': [0, 0]
        #     }

        self.setup_region(["inside", "outside", "distance"], "inside")

    @property
    def refinement_surface_is_enabled(self):
        return self.app[self.refinement_path] is not None

    @refinement_surface_is_enabled.setter
    def refinement_surface_is_enabled(self, value):
        if self.app[self.refinement_path] is None and value:
            self.app[self.refinement_path] = {
                'level': [0, 0]
            }
        elif self.app[self.refinement_path] is not None and not value:
            self.app[self.refinement_path] = None

    @property
    def surface_level(self):
        if self.refinement_surface_is_enabled:
            return list(self.app[self.refinement_path + ' level'])

    @surface_level.setter
    def surface_level(self, value):
        if self.refinement_surface_is_enabled:
            self.app[self.refinement_path + ' level'] = [value[0], int(value[1])]

    @property
    def cell_zone_inside(self):
        if self.is_region:
            return self.app[self.refinement_path + ' cellZoneInside']
        return -1

    @cell_zone_inside.setter
    def cell_zone_inside(self, value):
        if self.is_region:
            self.app[self.refinement_path + ' cellZoneInside'] = value

    @property
    def face_type(self):
        if self.is_region:
            return self.app[self.refinement_path + ' faceType']

    @face_type.setter
    def face_type(self, value):
        if self.is_region:
            self.app[self.refinement_path + ' faceType'] = value

    @property
    def is_region(self):
        return self.app[self.refinement_path + ' faceZone'] is not None

    @is_region.setter
    def is_region(self, value):
        if value:
            if self.app[self.refinement_path + ' faceZone'] is None:
                self.app[self.refinement_path + ' faceZone'] = self.__name
                self.app[self.refinement_path + ' cellZone'] = self.__name
                self.app[self.refinement_path + ' cellZoneInside'] = "inside"
                self.app[self.refinement_path + ' faceType'] = "internal"
        else:
            if self.app[self.refinement_path + ' faceZone'] is not None:
                self.app[self.refinement_path + ' faceZone'] = None
                self.app[self.refinement_path + ' cellZone'] = None
                self.app[self.refinement_path + ' cellZoneInside'] = None
                self.app[self.refinement_path + ' faceType'] = None