from dice_tools import wizard
from dice_tools.helpers.xmodel import modelRole, modelMethod
import random
from dice_vtk.geometries import VtkNumpySTL

class SurfaceRegion:

    def __init__(self, parent, mesh, app, **kwargs):
        super().__init__(**kwargs)
        self.__app = app
        self.__parent = parent
        self.__mesh = mesh
        self.__load()

    @property
    def app(self):
        return self.__app

    @property
    def mesh(self):
        return self.__mesh

    @property
    def name(self):
        return self.__mesh.name.decode('ascii', errors='ignore')

    @property
    def vtk_obj(self):
        return self.__vtk_obj

    @property
    def geometry_path(self):
        return self.__parent.geometry_path + ' regions ' + self.name
    
    def __load(self):
        color = [random.uniform(0.3, 0.7),
            random.uniform(0.6, 1.0), random.uniform(0.6, 1.0)]
        self.__vtk_obj = VtkNumpySTL(
            data = self.__mesh.vectors, name=self.name, color=color)

        if self.app[self.geometry_path] is None:
            self.app[self.geometry_path] = {
                'name': self.name
            }

        self.app.vis_add_object(self.__vtk_obj)
        wizard.subscribe(self, self.__vtk_obj)

    def w_geometry_object_clicked(self, obj, *args, **kwargs):
        self.app.refinement.model.current_item = self

    def remove_vis(self):
        self.app.vis_remove_object(self.__vtk_obj)

    @property
    def parent_level(self):
        return self.name not in self.app[self.__parent.refinement_path + ' regions']

    @parent_level.setter
    def parent_level(self, value):
        if value and not self.parent_level:
            self.app[self.__parent.refinement_path + ' regions ' + self.name] = None
            del self.__parent.refinement['regions'][self.name]
        elif not value and self.parent_level:
            self.app[self.__parent.refinement_path + ' regions ' + self.name] = {
                'level': self.__parent.surface_level
            }

    @property
    def surface_level(self):
        if self.parent_level:
            return self.__parent.surface_level
        else:
            return list(self.app[self.__parent.refinement_path
                + ' regions ' + self.name + ' level'])

    @surface_level.setter
    def surface_level(self, value):
        self.app[self.__parent.refinement_path
                + ' regions ' + self.name + ' level'] = value
    @property
    def has_layers_addition(self):
        path = 'foam:system/snappyHexMeshDict addLayersControls layers'
        return self.name in self.app[path]

    @has_layers_addition.setter
    def has_layers_addition(self, value):
        path = 'foam:system/snappyHexMeshDict addLayersControls layers '+self.name
        if value:
            self.app[path] = {
                    "nSurfaceLayers": 0
                }
        else:
            self.app[path] = None

    @property
    def layers_addition(self):
        if self.has_layers_addition:
            path = 'foam:system/snappyHexMeshDict addLayersControls layers '+self.name+' nSurfaceLayers'
            return self.app[path]

    @layers_addition.setter
    def layers_addition(self, value):
        if self.has_layers_addition:
            path = 'foam:system/snappyHexMeshDict addLayersControls layers '+self.name+' nSurfaceLayers'
            self.app[path] = value

    @modelMethod('showInScene')
    def show_in_scene(self):
        wizard.w_reset_camera_to_object([self.vtk_obj])

    @modelRole('label')
    def label(self):
        return self.name

    @modelRole('isVisible')
    def visible(self):
        return self.__vtk_obj.visible != 0

    @visible.setter
    def visible(self, value):
        if (self.__vtk_obj.visible != 0) != value:
            self.__vtk_obj.visible = value