from dice_tools import DICEObject, diceProperty, diceSlot, wizard
from dice_vtk.utils.foam_reader import FoamReader
from dice_tools.helpers.xmodel import modelRole, modelMethod, ModelItem
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile, ParsedBoundaryDict
from dice_tools.helpers.xmodel import standard_model
import random
from dice_vtk.geometries import ScalarBarWidget
from dice_vtk.scene import VtkScene
from dice_vtk.utils.foam_reader import FoamReader
from dice_vtk.geometries.geometry_base import GeometryBase


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
        self.__reader = None
        self.__scene = VtkScene()
        self.__app = app
        self.__boundary = None
        self.__boundary_model = standard_model(BoundaryItem)
        self.__bar = ScalarBarWidget()
        self.__scene.add_object(self.__bar)
        self.__current_field = ''
        self.__field_names = []
        self.__field_range_auto = True
        self.__field_range = [0, 0]
        wizard.subscribe(self, self.__boundary_model)
        wizard.subscribe(self.w_geometry_object_clicked)
        wizard.subscribe(self, self.__scene)
        self.__result_loaded = False

    def w_scene_object_added(self, scene, obj):
        if isinstance(obj, GeometryBase):
            self.update_field_range()
            for m in obj.get_mappers():
                m.SetScalarModeToUsePointFieldData()
                m.SelectColorArray(self.__current_field)
                m.UseLookupTableScalarRangeOn()
                m.SetLookupTable(self.__bar.lut)
            wizard.subscribe(self, obj)

    def w_scene_object_removed(self, scene, obj):
        wizard.unsubscribe(self, obj)

    def w_property_changed(self, obj, name, value):
        if obj in self.__scene.objects and name == 'visible':
            self.update_field_range()

    def w_animation_frame_changed(self, anim, frame):
        self.update_field_range()

    @diceProperty('QVariant', name='scene')
    def scene(self):
        return self.__scene

    @diceProperty('QVariant', name='model')
    def model(self):
        return self.__boundary_model

    @property
    def boundary(self):
        return self.__boundary

    @diceProperty('QVariant', name='currentField')
    def current_field(self):
        return self.__current_field

    @current_field.setter
    def current_field(self, value):
        if self.__current_field != value:
            self.__current_field = value
            self.update_field()
            self.update_field_range()
            self.__scene.render()

    @diceProperty("QVariantList", name = "fieldNames")
    def field_names(self):
        return self.__field_names

    @field_names.setter
    def field_names(self, value):
        self.__field_names = value

    @diceProperty('QVariantList', name='fieldRange')
    def field_range(self):
        return self.__field_range

    @field_range.setter
    def field_range(self, value):
        self.__field_range = value
        self.__bar.lut.SetRange(value)
        self.__scene.render()

    @diceProperty('bool', name='fieldRangeAuto')
    def field_range_auto(self):
        return self.__field_range_auto

    @field_range_auto.setter
    def field_range_auto(self, value):
        self.__field_range_auto = value
        self.update_field_range()

    def update_field_names(self):
        field_names = set()
        for obj in self.__scene.objects:
            if isinstance(obj, GeometryBase):
                for source in obj.get_sources():
                    if source.IsA('vtkAlgorithm'):
                        source = source.GetOutputDataObject(0)
                    if source.IsA('vtkDataSet'):
                        cell_data = source.GetCellData()
                        arr_num = cell_data.GetNumberOfArrays()
                        for i in range(arr_num):
                            arr_name = cell_data.GetArrayName(i)
                            field_names.add(arr_name)
        self.field_names = sorted(field_names)

    def update_field_range(self):
        if self.field_range_auto:
            r = [float('+inf'), float('-inf')]
            for obj in self.__scene.objects:
                if isinstance(obj, GeometryBase) and obj.visible:
                    for source in obj.get_sources():
                        if source.IsA('vtkAlgorithm'):
                            source.Update()
                            source = source.GetOutputDataObject(0)
                        if source.IsA('vtkDataSet'):

                            cells = source.GetCellData().GetArray(self.__current_field)
                            if cells is not None:
                                rr = cells.GetRange()
                                r = [min(rr[0], r[0]), max(rr[1], r[1])]
            if r != [float('+inf'), float('-inf')]:
                self.field_range = r

    def update_field(self):
        for obj in self.__scene.objects:
            if isinstance(obj, GeometryBase):
                for m in obj.get_mappers():
                    m.SelectColorArray(self.__current_field)

    def update(self):
        if self.__app.progress < 0:
            if not self.__result_loaded:
                self.__boundary = ParsedBoundaryDict(self.__app.run_path(
                    'constant', 'polyMesh', 'boundary'))

                self.__reader = FoamReader(self.__app.run_path())
                wizard.subscribe(self, self.__reader)
                self.__scene.animation = self.__reader

                for v in self.__reader.patches:
                    self.__scene.add_object(v)
                    if v.name in self.boundary:
                        item = BoundaryItem(self, v)
                        self.__boundary_model.root_elements.append(item)
                        color = [random.uniform(0.3, 0.7),
                            random.uniform(0.6, 1.0), random.uniform(0.6, 1.0)]
                        v.color=color
                        v.visible=False

                self.update_field_names()
                self.__result_loaded = True
        else:
            if self.__reader:
                for v in self.__reader.patches:
                    self.__scene.remove_object(v)
                self.__reader = None
            self.fields = []
            self.__scene.animation = None
            self.__boundary = None
            self.__boundary_model.root_elements.clear()
            self.__result_loaded = False

    def w_model_selection_changed(self, model, selected, deselected):
        for v in deselected:
            if hasattr(v, 'vis_obj'):
                v.vis_obj.set_selected(False)
        for v in selected:
            if hasattr(v, 'vis_obj'):
                v.vis_obj.set_selected(True)

    def w_geometry_object_clicked(self, obj, *args, **kwargs):
        if obj == None:
            self.__boundary_model.current_item = None
