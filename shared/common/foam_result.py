import math
import random
import subprocess

from dice_tools import DICEObject, diceProperty, diceSlot, wizard, diceSignal, \
    app_settings
from dice_vtk.utils.foam_reader import FoamReader
from dice_tools.helpers import run_process
from dice_tools.helpers.xmodel import modelRole, modelMethod, ModelItem
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile, ParsedBoundaryDict
from dice_tools.helpers.xmodel import standard_model
from dice_vtk.geometries import ScalarBarWidget
from dice_vtk.scene import VtkScene
from dice_vtk.utils.foam_reader import FoamReader
from dice_vtk.geometries.geometry_base import GeometryBase
from vtk import vtkDoubleArray, vtkDataArray, vtkFloatArray, vtkCellDataToPointData


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
        for v in self.parent.model.elements_of(BoundaryItem):
            if v.name == value:
                return
        if self.name != value:
            v = self.parent.boundary[self.name]
            del self.parent.boundary[self.name]
            self.parent.boundary[value] = v
            self.vis_obj.name = value
            self.parent.boundary.writeFile()
            self.parent.app.update_output()

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
        self.__scene = VtkScene()
        self.__boundary = None
        self.__boundary_model = standard_model(BoundaryItem)
        self.__bar = ScalarBarWidget()
        self.__scene.add_object(self.__bar)
        self.__current_field = 'Solid Color'
        self.__current_field_component = ''
        self.__field_names = []
        self.__field_range_auto = True
        self.__field_range = [0, 0]
        self.__result_loaded = False
        self.__result_is_loading = False
        self.__current_selected_obj = None
        self.__point_data_mode = True
        wizard.subscribe(self, self.__boundary_model)
        wizard.subscribe(self.w_geometry_object_clicked)
        wizard.subscribe(self, self.__scene)
        wizard.subscribe("prepare", self.__w_prepare)

        if self.__app.config["autoLoadResult"]:
            self.update()

    @property
    def app(self):
        return self.__app

    def __w_prepare(self):
        self.result_loaded = False

    def w_scene_object_added(self, scene, obj):
        if isinstance(obj, GeometryBase):
            self.update_field_range()
            for m in obj.get_mappers():
                m.InterpolateScalarsBeforeMappingOn()
                m.SetScalarModeToUsePointFieldData()
                m.SelectColorArray(self.__current_field)
                m.UseLookupTableScalarRangeOn()
                m.SetLookupTable(self.__bar.lut)
            wizard.subscribe(self, obj)
            self.set_component_names(obj)

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

    def set_component_names(self, obj):
        if isinstance(obj, GeometryBase):
            for source in obj.get_sources():
                if source.IsA('vtkAlgorithm'):
                    source = source.GetOutputDataObject(0)
                if source.IsA('vtkDataSet'):
                    dataCellSet = source.GetCellData()
                    dataPointSet = source.GetPointData()
                    n_arrays = dataCellSet.GetNumberOfArrays()
                    for i in range(n_arrays):
                        arr_name = dataCellSet.GetArrayName(i)
                        if arr_name is not None:
                            cells_array = dataCellSet.GetAbstractArray(i)
                            points_array = dataPointSet.GetAbstractArray(i)
                            component_count = cells_array.GetNumberOfComponents()
                            if not cells_array.HasAComponentName():
                                for c_index in range(0, component_count):
                                    cells_array.SetComponentName(c_index, str(c_index))
                                    points_array.SetComponentName(c_index, str(c_index))

                            # if component_count == 3:
                            #
                            #     print("----calculating ...", obj.name, arr_name)
                            #
                            #     # Magnitude (Cells)
                            #     # =================
                            #     num_tuples = cells_array.GetNumberOfTuples()
                            #     num_comps = cells_array.GetNumberOfComponents()
                            #
                            #     new_array = vtkFloatArray()
                            #     new_array.SetNumberOfComponents(1)
                            #     new_array.SetNumberOfTuples(num_tuples)
                            #     new_array.SetName("{} Magnitude".format(arr_name))
                            #
                            #     for cc in range(num_tuples):
                            #         mag = 0.0
                            #         tuple = cells_array.GetTuple(cc)
                            #         for comp in range(num_comps):
                            #             mag += tuple[comp] * tuple[comp]
                            #         new_array.SetTuple1(cc, math.sqrt(mag))
                            #     dataCellSet.AddArray(new_array)
                            #     dataCellSet.Update()
                            #
                            #     # Magnitude (Points)
                            #     # ==================
                            #     num_tuples = points_array.GetNumberOfTuples()
                            #     num_comps = points_array.GetNumberOfComponents()
                            #
                            #     new_array = vtkFloatArray()
                            #     new_array.SetNumberOfComponents(1)
                            #     new_array.SetNumberOfTuples(num_tuples)
                            #     new_array.SetName("{} Magnitude".format(arr_name))
                            #
                            #     for cc in range(num_tuples):
                            #         mag = 0.0
                            #         tuple = points_array.GetTuple(cc)
                            #         for comp in range(num_comps):
                            #             mag += tuple[comp] * tuple[comp]
                            #         new_array.SetTuple1(cc, math.sqrt(mag))
                            #     dataPointSet.AddArray(new_array)
                            self.update_field()
                            self.update_field_names()

    current_field_changed = diceSignal(name='currentFieldChanged')

    @diceProperty('QVariant', name='currentField',
                  notify=current_field_changed)
    def current_field(self):
        return self.__current_field

    @current_field.setter
    def current_field(self, value):
        if self.__current_field != value:
            self.__current_field = value
            self.set_default_component_name()
            self.update_field()
            self.update_field_range()
            self.__scene.render()
            self.current_field_changed()

    @diceProperty("QVariantList", name="fieldNames")
    def field_names(self):
        return self.__field_names

    @field_names.setter
    def field_names(self, value):
        self.__field_names = value

    @diceProperty("QVariant", name="currentFieldComponentNames",
                  notify=current_field_changed)
    def current_field_component_names(self):
        component_count = self.get_number_of_components_for_current_field()
        if component_count is not None:
            if component_count <= 1:
                return []
            elif component_count == -1:
                return "Magnitude"
            elif component_count <= 3:
                titles = ["X", "Y", "Z"]
                return titles
            elif component_count == 6:
                # symmetric matrix is assumed here
                titles = ["XX", "YY", "ZZ", "XY", "YZ", "XZ"]
                return titles
        else:
            return []

    def get_number_of_components_for_current_field(self):
        """
        Get number of components from one of the visible objects.
        :return:
        """
        for obj in self.__scene.objects:
            if isinstance(obj, GeometryBase) and obj.visible:
                for source in obj.get_sources():
                    if source.IsA('vtkAlgorithm'):
                        source = source.GetOutputDataObject(0)
                    if source.IsA('vtkDataSet'):
                        cells = source.GetCellData().GetArray(self.__current_field)
                        if cells is not None:
                            n_components = cells.GetNumberOfComponents()
                            return n_components

    current_field_component_changed = diceSignal(name="currentFieldComponentChanged")

    @diceProperty('QVariant', name='currentFieldComponent', notify=current_field_component_changed)
    def current_field_component(self):
        return self.__current_field_component

    @current_field_component.setter
    def current_field_component(self, value):
        if self.__current_field_component != value:
            self.__current_field_component = value
            self.update_field()
            self.update_field_range()
            self.__scene.render()
            self.current_field_component_changed()

    def set_default_component_name(self):
        for obj in self.__scene.objects:
            if isinstance(obj, GeometryBase) and obj.visible:
                for source in obj.get_sources():
                    if source.IsA('vtkAlgorithm'):
                        source.Update()
                        source = source.GetOutputDataObject(0)
                    if source.IsA('vtkDataSet'):
                        cells = source.GetCellData().GetArray(self.__current_field)
                        if cells is not None:
                            component_count = cells.GetNumberOfComponents()
                            title = self.get_default_component_name(0, component_count)
                            self.current_field_component = title

    def get_default_component_name(self, component_number, component_count):
        """
        Based on the vtkPVpostFilter method.
        https://github.com/Kitware/ParaView/blob/master/ParaViewCore/VTKExtensions/Core/vtkPVPostFilter.cxx#L146
        :param component_number:
        :param component_count:
        :return:
        """
        if component_count <= 1:
            return ""
        elif component_number == -1:
            return "Magnitude"
        elif component_count <= 3 and component_number < 3:
            titles = ["X", "Y", "Z"]
            return titles[component_number]
        elif component_count == 6:
            # symmetric matrix is assumed here
            titles = ["XX", "YY", "ZZ", "XY", "YZ", "XZ"]
            return titles[component_number]
        else:
            str(component_number)

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
        field_names.add('Solid Color')
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
                            cells = source.GetPointData().GetAbstractArray(self.__current_field)
                            if cells is not None:
                                comp_names = self.current_field_component_names
                                if isinstance(comp_names, list) and \
                                                self.current_field_component in self.current_field_component_names:
                                    i = comp_names.index(self.current_field_component)
                                else:
                                    i = 0
                                rr = cells.GetRange(i)
                                r = [min(rr[0], r[0]), max(rr[1], r[1])]
            if r != [float('+inf'), float('-inf')]:
                self.field_range = r

    def update_field(self):
        for obj in self.__scene.objects:
            if isinstance(obj, GeometryBase):
                for m in obj.get_mappers():
                    m.SelectColorArray(self.__current_field)

    @diceSlot(name="update")
    def update(self):
        self.result_is_loading = True
        if self.__app.progress < 0:
            if not self.result_loaded:
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
                                 random.uniform(0.6, 1.0),
                                 random.uniform(0.6, 1.0)]
                        v.color = color
                        v.visible = False
                self.update_field_names()
                self.result_loaded = True
        else:
            if self.__reader:
                for v in self.__reader.patches:
                    self.__scene.remove_object(v)
                self.__reader = None
            self.__scene.animation = None
            self.__boundary = None
            self.__boundary_model.root_elements.clear()
            self.result_loaded = False
        self.result_is_loading = False

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
        self.current_selected_obj = obj
        self.bounds_changed()

    @property
    def current_selected_obj(self):
        return self.__current_selected_obj

    @current_selected_obj.setter
    def current_selected_obj(self, obj):
        if self.__current_selected_obj != obj:
            self.__current_selected_obj = obj

    result_is_loading_changed = diceSignal(name="resultIsLoadingChanged")

    @diceProperty('QVariant', name='resultIsLoading', notify=result_is_loading_changed)
    def result_is_loading(self):
        return self.__result_is_loading

    @result_is_loading.setter
    def result_is_loading(self, value):
        self.__result_is_loading = value
        self.result_is_loading_changed()

    result_loaded_changed = diceSignal(name="resultLoadedChanged")

    @diceProperty('QVariant', name="resultLoaded", notify=result_loaded_changed)
    def result_loaded(self):
        return self.__result_loaded

    @result_loaded.setter
    def result_loaded(self, value):
        self.__result_loaded = value
        self.result_loaded_changed()

    bounds_changed = diceSignal(name='boundsChanged')

    @diceProperty('QVariant', name='bounds', notify=bounds_changed)
    def bounds(self):
        obj = self.current_selected_obj
        if isinstance(obj, GeometryBase):
            for source in obj.get_sources():
                if source.IsA('vtkAlgorithm'):
                    source.Update()
                    source = source.GetOutputDataObject(0)
                if source.IsA('vtkDataSet'):
                    return source.GetBounds()

    @diceProperty('QVariant', name='statistics', notify=bounds_changed)
    def statistics(self):
        obj = self.current_selected_obj
        if isinstance(obj, GeometryBase):
            for source in obj.get_sources():
                if source.IsA('vtkAlgorithm'):
                    source.Update()
                    source = source.GetOutputDataObject(0)
                if source.IsA('vtkDataSet'):
                    stats = {}
                    # stats['Type'] = source.GetDataObjectType()
                    stats['Number of Cells'] = source.GetNumberOfCells()
                    stats['Number of Points'] = source.GetNumberOfPoints()
                    stats['Memory [MB]'] = source.GetActualMemorySize()*0.001024
                    stats['Center'] = source.GetCenter()
                    return stats

    @diceSlot(name='openParaview')
    def open_paraview(self):
        settings = app_settings()
        paraview_cmd = settings['paraview_cmd']

        subprocess.Popen([paraview_cmd, 'p.foam'], cwd=self.__app.run_path())

    @diceProperty('QVariant', name='pointDataMode')
    def point_data_mode(self):
        return self.__point_data_mode

    @point_data_mode.setter
    def point_data_mode(self, value):
        if self.point_data_mode != value:
            for obj in self.__scene.objects:
                if isinstance(obj, GeometryBase):
                    for m in obj.get_mappers():
                        if value:
                            m.SetScalarModeToUsePointFieldData()
                        else:
                            m.SetScalarModeToUseCellFieldData()
            self.__scene.render()
            self.__point_data_mode = value
