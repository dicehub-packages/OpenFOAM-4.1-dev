from dice_tools import DICEObject, diceProperty, diceSlot, wizard
from dice_vtk.utils.foam_reader import FoamReader
from dice_tools.helpers.xmodel import modelRole, modelMethod, ModelItem
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile, ParsedBoundaryDict
from dice_tools.helpers.xmodel import standard_model
import random

class BoundaryItem:

    def __init__(self, parent, vis_obj):
        self.parent = parent
        self.vis_obj = vis_obj
        wizard.subscribe(self, self.vis_obj)
        
    def w_geometry_object_clicked(self, obj, *args, **kwargs):
        self.parent.model.current_item = self

    @modelMethod('showInScene')
    def show_in_scene(self):
        wizard.w_reset_camera_to_object([self.vis_obj])

    @modelRole('name')
    def name(self):
        return self.vis_obj.name

    @name.setter
    def name(self, value):
        self.parent.boundary[value] = self.parent.boundary[self.name]
        del self.parent.boundary[self.name]
        self.vis_obj.name = value
        self.parent.boundary.writeFile()

    @modelRole('type')
    def type(self):
        return self.parent.boundary[self.name]['type']

    @type.setter
    def type(self, value):
        self.parent.boundary[self.name]['type'] = value
        self.parent.boundary.writeFile()

    @modelRole('isVisible')
    def visible(self):
        return self.vis_obj.visible
    
    @visible.setter
    def visible(self, value):
        self.vis_obj.visible = value



class Result(DICEObject):

    def __init__(self, app, **kwargs):
        super().__init__(base_type='QObject', **kwargs)
        self.__app = app
        self.__reader = None
        self.__boundary = None
        self.__boundary_model = standard_model(BoundaryItem)
        wizard.subscribe(self, self.__boundary_model)
        wizard.subscribe(self.w_geometry_object_clicked)

    @diceProperty('QVariant', name='model')
    def model(self):
        return self.__boundary_model

    @property
    def boundary(self):
        return self.__boundary

    def update(self):
        if self.__app.progress < 0:
            self.__boundary = ParsedBoundaryDict(self.__app.run_path(
                'constant', 'polyMesh', 'boundary'))
            self.__reader = FoamReader(self.__app.run_path())
            self.__app.result_scene.animation = self.__reader
            for v in self.__reader.patches:
                self.__app.result_scene.add_object(v)
                if v.name in self.boundary:
                    item = BoundaryItem(self, v)
                    self.__boundary_model.root_elements.append(item)

                    color = [random.uniform(0.3, 0.7),
                        random.uniform(0.6, 1.0), random.uniform(0.6, 1.0)]
                    # v.opacity=0.8
                    v.color=color
                    v.visible=False
                else:
                    v.visible=True
        else:
            if self.__reader:
                for v in self.__reader.patches:
                    self.__app.result_scene.remove_object(v)
                self.__reader = None
            self.__boundary = None
            self.__boundary_model.root_elements.clear()

    def w_model_selection_changed(self, model, selected, deselected):
        for v in deselected:
            if hasattr(v, 'vis_obj'):
                v.vis_obj.set_selected(False)
                # v.vis_obj.opacity=0.8
        for v in selected:
            if hasattr(v, 'vis_obj'):
                v.vis_obj.set_selected(True)
                # v.vis_obj.opacity=1

    def w_geometry_object_clicked(self, obj, *args, **kwargs):
        if obj == None:
            self.__boundary_model.current_item = None
