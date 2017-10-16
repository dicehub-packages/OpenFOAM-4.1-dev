from dice_tools import DICEObject, diceProperty, diceSlot, wizard
from dice_vtk.geometries import DynamicSphere

class MaterialPoint(DICEObject):

    point_path = "foam:system/snappyHexMeshDict castellatedMeshControls locationInMesh"

    def __init__(self, app, **kwargs):
        super().__init__(base_type='QObject', **kwargs)
        self.__app = app
        self.__vis = DynamicSphere(name='Material point')
        self.__vis.movable = True
        self.__vis.position = self.location
        self.__vis.target = self.__app.bounding_box.vis_obj
        self.__app.vis_add_object(self.__vis)
        wizard.subscribe(self, self.__vis)
        wizard.subscribe(self.w_geometry_object_clicked)

    def w_geometry_object_clicked(self, obj, *args, **kwargs):
        if obj == self.__vis:
            self.__vis.set_selected(True)
        else:
            self.__vis.set_selected(False)

    @diceSlot(name='selectVisObject')
    def select_vis_object(self):
        wizard.w_reset_camera_to_object([self.__vis], scale = 5)
        wizard.w_geometry_object_clicked(self.__vis, control_modifier = False)

    @diceSlot(name='resetToBoundingBox')
    def reset_vis_object(self):
        self.__vis.position = self.__app.bounding_box.vis_obj.center
        wizard.w_reset_camera_to_object([self.__vis], scale = 5)
        wizard.w_geometry_object_clicked(self.__vis, control_modifier = False)

    @diceProperty('QVariantList', name='location')
    def location(self):
        return list(self.__app[self.point_path])

    @location.setter
    def location(self, value):
        self.__app[self.point_path] = value
        self.__vis.position = value

    def w_property_changed(self, obj, name, value):
        if name == 'position':
            wizard.unsubscribe(self, self.__vis)
            self.location = value
            wizard.subscribe(self, self.__vis)