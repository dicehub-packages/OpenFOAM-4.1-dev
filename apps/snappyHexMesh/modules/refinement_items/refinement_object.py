from .region_refinement import RegionRefinement
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