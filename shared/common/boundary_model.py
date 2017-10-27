from dice_tools import *
from dice_tools.helpers.xmodel import *
from PyFoam.Basics.DataStructures import Field, Vector, DictProxy
from dice_vtk.utils.foam_reader import FoamReader
from PyFoam.RunDictionary.ParsedParameterFile import ParsedBoundaryDict

import os
import random
import shutil

class BoundaryGroup(ModelItem):

    def __init__(self, items, **kwargs):
        super().__init__(**kwargs)
        for v in items:
            self.elements.append(v)
        wizard.subscribe(self, self)

    def w_model_remove_items(self, *args, **kwargs):
        wizard.w_model_update_item(self)

    def w_model_insert_items(self, *args, **kwargs):
        wizard.w_model_update_item(self)

    @modelRole('name')
    def name(self):
        return ', '.join([v.vis.name for v in self.elements])

    @modelRole('boundaryGroupType')
    def boundary_group_type(self):
        for v in self.elements:
            return v.boundary_type

    @boundary_group_type.setter
    def boundary_group_type(self, value):
        for v in self.elements:
            v.boundary_type = value
        a, b = self.elements
        a.neighbour_patch = b.name
        b.neighbour_patch = a.name

class Boundary:

    def __init__(self, vis, app):
        self.vis = vis
        self.app = app
        wizard.subscribe(self, self.vis)

    def w_geometry_object_clicked(self, obj, *args, **kwargs):
        self.app.boundaries_model.current_item = self

    @property
    def path(self):
        return 'foam:constant/polyMesh/boundary ' + self.name
    
    @modelRole('name')
    def name(self):
        return self.vis.name

    @name.setter
    def name(self, value):
        v = self.app[self.path]
        self.app[self.path] = None
        self.vis.name = value
        self.app[self.path] = v

    @modelRole('boundaryType')
    def boundary_type(self):
        type_path = self.path + ' type'
        return self.app[type_path]

    @boundary_type.setter
    def boundary_type(self, value):
        type_path = self.path + ' type'
        if self.app[type_path] == value:
            return
        if ((self.app[type_path] in ('cyclic', 'cyclicAMI')) != 
                (value in ('cyclic', 'cyclicAMI'))):

            for v in list(self.app[self.path]):
                if v not in ('inGroups', 'type', 'nFaces', 'startFace'):
                    self.app[self.path + ' ' + v] = None

            if value in ('cyclic', 'cyclicAMI'):
                self.app[self.path + ' matchTolerance'] = 1e-4
                self.app[self.path + ' transform'] = 'noOrdering'
                self.app[self.path + ' lowWeightCorrection'] = 0.2
                self.app[self.path + ' neighbourPatch'] = ''

        self.app[self.path + ' type'] = value


    @modelRole('isVisible')
    def visible(self):
        return self.vis.visible
    
    @visible.setter
    def visible(self, value):
        self.vis.visible = value

    @property
    def neighbour_patch(self):
        if self.boundary_type in ('cyclic', 'cyclicAMI'):
            return self.app[self.path + ' neighbourPatch'] or ''

    @neighbour_patch.setter
    def neighbour_patch(self, value):
        if self.boundary_type in ('cyclic', 'cyclicAMI'):
            self.app[self.path + ' neighbourPatch'] = value

    @property
    def transform(self):
        if self.boundary_type in ('cyclic', 'cyclicAMI'):
            return self.app[self.path + ' transform']

    @transform.setter
    def transform(self, value):
        if self.boundary_type in ('cyclic', 'cyclicAMI'):
            self.app[self.path + ' transform'] = value

    @property
    def match_tolerance(self):
        if self.boundary_type in ('cyclic', 'cyclicAMI'):
            return self.app[self.path + ' matchTolerance']

    @match_tolerance.setter
    def match_tolerance(self, value):
        if self.boundary_type in ('cyclic', 'cyclicAMI'):
            self.app[self.path + ' matchTolerance'] = value

    @property
    def low_weight_correction(self):
        if (self.boundary_type in ('cyclic', 'cyclicAMI') 
                and self.low_weight_correction_enable):
            return self.app[self.path + ' lowWeightCorrection']

    @low_weight_correction.setter
    def low_weight_correction(self, value):
        if (self.boundary_type in ('cyclic', 'cyclicAMI')
                and self.low_weight_correction_enable):
            self.app[self.path + ' lowWeightCorrection'] = value

    @property
    def low_weight_correction_enable(self):
        if self.boundary_type in ('cyclic', 'cyclicAMI'):
            return self.app[self.path + ' lowWeightCorrection'] is not None

    @low_weight_correction_enable.setter
    def low_weight_correction_enable(self, value):
        if self.boundary_type in ('cyclic', 'cyclicAMI'):
            if value and not self.low_weight_correction_enable:
                self.app[self.path + ' lowWeightCorrection'] = 0.2
            elif not value and  self.low_weight_correction_enable:
                self.app[self.path + ' lowWeightCorrection'] = None

    @property
    def pressure_boundary_condition_type(self):
        path = 'foam:0/p boundaryField ' + self.name + ' type'
        condition_type = self.app[path]
        if condition_type == 'fixedValue':
            return 'Fixed Value'
        elif condition_type == 'totalPressure':
            return 'Total Pressure'
        elif condition_type == 'zeroGradient':
            return 'Zero Gradient'
        elif condition_type == 'slip':
            return 'Slip'
        elif condition_type == 'symmetry':
            return 'Symmetry'

    @pressure_boundary_condition_type.setter
    def pressure_boundary_condition_type(self, value):
        path = 'foam:0/p boundaryField ' + self.name
        default_pressure_value = 0
        if value == 'Fixed Value':
            self.app[path] = {
                'type': 'fixedValue',
                'value': Field(default_pressure_value)
            }
        elif value == 'Total Pressure':
            self.app[path] = {
                'type': 'totalPressure',
                'p0': Field(default_pressure_value),
                'U': 'U',
                'phi': 'phi',
                'rho': 'none',
                'psi': 'none',
                'gamma': 1,
                'value': Field(default_pressure_value)
            }
        elif value == 'Zero Gradient':
            self.app[path] = {
                'type': 'zeroGradient'
            }
        elif value == 'Slip':
            self.app[path] = {
                'type': 'slip'
            }
        elif value == 'Symmetry':
            self.app[path] = {
                'type': 'symmetry'
            }

    @property
    def pressure_field_value(self):
        path = 'foam:0/p boundaryField ' + self.name + ' value'
        return self.app[path]

    @pressure_field_value.setter
    def pressure_field_value(self, value):
        path = 'foam:0/p boundaryField ' + self.name + ' value'
        if self.app[path] is not None:
            self.app[path] = Field(value)

    @property
    def velocity_boundary_condition_type(self):
        path = 'foam:0/U boundaryField ' + self.name + ' type'
        condition_type = self.app[path]
        if condition_type == 'fixedValue':
            return 'Fixed Value'
        elif condition_type == 'zeroGradient':
            return 'Zero Gradient'
        elif condition_type == 'inletOutlet':
            return 'Inlet Outlet'
        elif condition_type == 'slip':
            return 'Slip'
        elif condition_type == 'symmetry':
            return 'Symmetry'

    @velocity_boundary_condition_type.setter
    def velocity_boundary_condition_type(self, value):
        path = 'foam:0/U boundaryField ' + self.name
        default_velocity_vector = Vector(0, 0, 0)
        if value == 'Fixed Value':
            self.app[path] = {
                'type': 'fixedValue',
                'value': Field(default_velocity_vector)
            }
        elif value == 'Zero Gradient':
            self.app[path] = {
                'type': 'zeroGradient'
            }
        elif value == 'Inlet Outlet':
            self.app[path] = {
                'type': 'inletOutlet',
                'inletValue': Field(default_velocity_vector),
                'value': '$internalField'
            }
        elif value == 'Slip':
            self.app[path] = {
                'type': 'slip'
            }
        elif value == 'Symmetry':
            self.app[path] = {
                'type': 'symmetry'
            }

    @property
    def velocity_field_value(self):
        path = 'foam:0/U boundaryField ' + self.name + ' value'
        return self.app[path]

    @velocity_field_value.setter
    def velocity_field_value(self, value):
        path = 'foam:0/U boundaryField ' + self.name + ' value'
        if self.app[path] is not None:
            self.app[path] = Field(Vector(*value))

    @property
    def velocity_inlet_value(self):
        path = 'foam:0/U boundaryField ' + self.name + ' inletValue'
        return self.app[path]

    @velocity_inlet_value.setter
    def velocity_inlet_value(self, value):
        path = 'foam:0/U boundaryField ' + self.name + ' inletValue'
        if self.app[path] is not None:
            self.app[path] = Field(Vector(*value))

    @property
    def omega_boundary_condition_type(self):
        path = 'foam:0/omega boundaryField ' + self.name + ' type'
        condition_type = self.app[path]
        if condition_type == 'fixedValue':
            return 'Fixed Value'
        elif condition_type == 'zeroGradient':
            return 'Zero Gradient'
        elif condition_type == 'turbulentMixingLengthFrequencyInlet':
            return 'Turbulent Mixing Length Frequency Inlet'
        elif condition_type == 'symmetry':
            return 'Symmetry'
        elif condition_type == 'slip':
            return 'Slip'
            
    @omega_boundary_condition_type.setter
    def omega_boundary_condition_type(self, value):
        path = 'foam:0/omega boundaryField ' + self.name
        default_value = 1.0
        if value == 'Fixed Value':
            self.app[path] = {
                'type': 'fixedValue',
                'value': Field(default_value)
            }
        elif value == 'Zero Gradient':
            self.app[path] = {
                'type': 'zeroGradient'
            }
        elif value == 'Turbulent Mixing Length Frequency Inlet':
            self.app[path] = {
                'type': 'turbulentMixingLengthFrequencyInlet',
                'value': Field(default_value),
                'mixingLength': 0.001
            }
        elif value == 'Symmetry':
            self.app[path] = {
                'type': 'symmetry'
            }
        elif value == 'Slip':
            self.app[path] = {
                'type': 'slip'
            }

    @property
    def omega_field_value(self):
        path = 'foam:0/omega boundaryField ' + self.name + ' value'
        return self.app[path]

    @omega_field_value.setter
    def omega_field_value(self, value):
        path = 'foam:0/omega boundaryField ' + self.name + ' value'
        if self.app[path] is not None:
            self.app[path] = Field(value)

    @property
    def omega_mixing_length_value(self):
        path = 'foam:0/omega boundaryField ' + self.name + ' mixingLength'
        return self.app[path]

    @omega_mixing_length_value.setter
    def omega_mixing_length_value(self, value):
        path = 'foam:0/omega boundaryField ' + self.name + ' mixingLength'
        if self.app[path] is not None:
            self.app[path] = value

    @property
    def k_boundary_condition_type(self):
        path = 'foam:0/k boundaryField ' + self.name + ' type'
        condition_type = self.app[path]
        if condition_type == 'fixedValue':
            return 'Fixed Value'
        elif condition_type == 'zeroGradient':
            return 'Zero Gradient'
        elif condition_type == 'turbulentIntensityKineticEnergyInlet':
            return 'Turbulent Intensity Kinetic Energy Inlet'
        elif condition_type == 'symmetry':
            return 'Symmetry'
        elif condition_type == 'slip':
            return 'Slip'

    @k_boundary_condition_type.setter
    def k_boundary_condition_type(self, value):
        path = 'foam:0/k boundaryField ' + self.name
        default_value = 1.0
        if value == 'Fixed Value':
            self.app[path] = {
                'type': 'fixedValue',
                'value': Field(default_value)
            }
        elif value == 'Zero Gradient':
            self.app[path] = {
                'type': 'zeroGradient'
            }
        elif value == 'Turbulent Intensity Kinetic Energy Inlet':
            self.app[path] = {
                'type': 'turbulentIntensityKineticEnergyInlet',
                'value': Field(default_value),
                'intensity': 0.05
            }
        elif value == 'Symmetry':
            self.app[path] = {
                'type': 'symmetry'
            }
        elif value == 'Slip':
            self.app[path] = {
                'type': 'slip'
            }

    @property
    def k_field_value(self):
        path = 'foam:0/k boundaryField ' + self.name + ' value'
        return self.app[path]

    @k_field_value.setter
    def k_field_value(self, value):
        path = 'foam:0/k boundaryField ' + self.name + ' value'
        if self.app[path] is not None:
            self.app[path] = Field(value)

    @property
    def k_intensity_value(self):
        path = 'foam:0/k boundaryField ' + self.name + ' intensity'
        return self.app[path]

    @k_intensity_value.setter
    def k_intensity_value(self, value):
        path = 'foam:0/k boundaryField ' + self.name + ' intensity'
        if self.app[path] is not None:
            self.app[path] = value

    @property
    def epsilon_boundary_condition_type(self):
        path = 'foam:0/epsilon boundaryField ' + self.name + ' type'
        condition_type = self.app[path]
        if condition_type == 'fixedValue':
            return 'Fixed Value'
        elif condition_type == 'zeroGradient':
            return 'Zero Gradient'
        elif condition_type == 'turbulentMixingLengthDissipationRateInlet':
            return 'Turbulent Mixing Length Inlet'
        elif condition_type == 'symmetry':
            return 'Symmetry'
        elif condition_type == 'slip':
            return 'Slip'

    @epsilon_boundary_condition_type.setter
    def epsilon_boundary_condition_type(self, value):
        path = 'foam:0/epsilon boundaryField ' + self.name
        default_value = 1.0
        if value == 'Fixed Value':
            self.app[path] = {
                'type': 'fixedValue',
                'value': Field(default_value)
            }
        elif value == 'Zero Gradient':
            self.app[path] = {
                'type': 'zeroGradient'
            }
        elif value == 'Turbulent Mixing Length Inlet':
            self.app[path] = {
                'type': 'turbulentMixingLengthDissipationRateInlet',
                'value': Field(default_value),
                'mixingLength': 0.001
            }
        elif value == 'Symmetry':
            self.app[path] = {
                'type': 'symmetry'
            }
        elif value == 'Slip':
            self.app[path] = {
                'type': 'slip'
            }

    @property
    def epsilon_field_value(self):
        path = 'foam:0/epsilon boundaryField ' + self.name + ' value'
        return self.app[path]

    @epsilon_field_value.setter
    def epsilon_field_value(self, value):
        path = 'foam:0/epsilon boundaryField ' + self.name + ' value'
        if self.app[path] is not None:
            self.app[path] = Field(value)

    @property
    def epsilon_mixing_length_value(self):
        path = 'foam:0/epsilon boundaryField ' + self.name + ' mixingLength'
        return self.app[path]

    @epsilon_mixing_length_value.setter
    def epsilon_mixing_length_value(self, value):
        path = 'foam:0/epsilon boundaryField ' + self.name + ' mixingLength'
        if self.app[path] is not None:
            self.app[path] = value

    @property
    def temperature_boundary_condition_type(self):
        path = 'foam:0/T boundaryField ' + self.name + ' type'
        condition_type = self.app[path]
        if condition_type == "fixedValue":
            return "Fixed Value"
        elif condition_type == "zeroGradient":
            return "Zero Gradient"
        elif condition_type == "empty":
            return "Empty"
        elif condition_type == 'symmetry':
            return 'Symmetry'

    @temperature_boundary_condition_type.setter
    def temperature_boundary_condition_type(self, value):
        path = 'foam:0/T boundaryField ' + self.name
        default_pressure_value = 0
        if value == "Fixed Value":
            self.app[path] = {
                "type": "fixedValue",
                "value": Field(default_pressure_value)
            }
        elif value == "Zero Gradient":
            self.app[path] = {
                "type": "zeroGradient"
            }
        elif value == "Empty":
            self.app[path] = {
                "type": "empty"
            }
        elif value == 'Symmetry':
            self.app[path] = {
                'type': 'symmetry'
            }
            
    @property
    def temperature_boundary_condition_type_list(self):
        if self.boundary_type == "empty":
            return ["Empty"]
        else:
            return ["Fixed Value", "Zero Gradient", "Empty"]

    @property
    def temperature_field_value(self):
        path = 'foam:0/T boundaryField ' + self.name + ' value'
        return self.app[path]


    @temperature_field_value.setter
    def temperature_field_value(self, value):
        path = 'foam:0/T boundaryField ' + self.name + ' value'
        if self.app[path] is not None:
            self.app[path] = Field(value)


class BoundaryApp:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__boundaries_model = standard_model(Boundary, BoundaryGroup)
        self.__boundary_items = []
        self.__boundary_names = []
        self.__boundaries_props = []
        self.__reader = None
        wizard.subscribe(self, self.__boundaries_model)
        wizard.subscribe(self.w_geometry_object_clicked)

    def load_boundary(self, boundary_props, input_data):

        self.__boundaries_model.root_elements.clear()

        if self.__reader:
            for v in self.__reader.patches:
                self.vis_remove_object(v)

        config_boundary_path = self.config_path("constant", "polyMesh")
        has_input = True

        self.__input_data = input_data
        foam_mesh = self.__input_data.get('foam_mesh', {})
        for app, paths in foam_mesh.items():
            for path in paths:
                path = self.workflow_path(path, "constant", "polyMesh")
                modified = os.stat(os.path.join(path, 'boundary')).st_mtime
                if modified != self.config.get('modified'):
                    if os.path.exists(config_boundary_path):
                        shutil.rmtree(config_boundary_path)
                    self.copy_folder_content(path, config_boundary_path)
                    self.config['modified'] = modified
                    self.config.write()
            break
        else:
            # no input, clear and return
            self.__reader = None
            self.__boundary = None
            self.foam_file('constant/polyMesh/boundary', None)
            if os.path.exists(config_boundary_path):
                shutil.rmtree(config_boundary_path)
            return

        self.__boundary = ParsedBoundaryDict(self.config_path(
            'constant', 'polyMesh', 'boundary'))

        self.foam_file('constant/polyMesh/boundary', self.__boundary)
        
        boundary_names = set(self['foam:constant/polyMesh/boundary'])

        for path, prop in boundary_props.items():
            for v in list(self[path]):
                if v not in boundary_names:
                    self[path + ' ' + v] = None

            for v in boundary_names:
                if v not in self[path]:
                    self[path + ' ' + v] = prop

        wizard.w_idle()
        
        self.__reader = FoamReader(self.config_path(), cells=False)

        for v in self.__reader.patches:
            self.vis_add_object(v)
            if v.name in boundary_names:
                item = Boundary(v, self)
                self.__boundary_items.append(item)
                if item.neighbour_patch:
                    for v in self.__boundaries_model.elements_of(BoundaryGroup):
                        for vv in v.elements:
                            if vv.name == item.neighbour_patch:
                                v.elements.append(item)
                                break
                        else:
                            continue
                        break
                    else:
                        self.__boundaries_model.root_elements.append(BoundaryGroup([item]))
                else:
                    self.__boundaries_model.root_elements.append(item)
                color = [random.uniform(0.3, 0.7),
                    random.uniform(0.6, 1.0), random.uniform(0.6, 1.0)]
                v.opacity=0.8
                v.color = color
            else:
                v.visible=False

        self.__boundary_names = [''] + list(boundary_names)
        self.boundary_names_changed()

    @diceSlot('QVariant', name='filterBoundaries')
    def filter_boundaries(self, text):
        self.__boundaries_model.root_elements.clear()
        if text:
            for v in self.__boundary_items:
                if text.lower() in v.name.lower():
                    self.__boundaries_model.root_elements.append(v)
        else:
            self.__boundaries_model.root_elements.extend(self.__boundary_items)

    @diceProperty('QVariant', name='boundariesModel')
    def boundaries_model(self):
        return self.__boundaries_model

    boundary_names_changed = diceSignal(name='boundaryNamesChanged')
    @diceProperty('QVariantList', name='boundaryNames', notify=boundary_names_changed)
    def boundary_names(self):
        return self.__boundary_names

    selection_changed = diceSignal(name='selectionChanged')

    @diceProperty('QVariant', name='canGroup', notify=selection_changed)
    def can_group(self):
        if len(self.__boundaries_model.selection) != 2:
            return False
        for v in self.__boundaries_model.selection:
            for vv in self.__boundaries_model.elements_of(BoundaryGroup):
                if v == vv or v in vv.elements:
                    return False
        return True

    @diceSlot(name='makeGroup')
    def make_group(self):
        if self.can_group:
            for v in self.__boundaries_model.selection:
                self.__boundaries_model.root_elements.remove(v)
            group = BoundaryGroup(self.__boundaries_model.selection)
            group.boundary_group_type = 'cyclic'
            self.__boundaries_model.root_elements.append(group)
            self.__boundaries_model.current_item = group
            signal('boundary:*')

    @diceSlot(name='breakGroup')
    def break_group(self):
        for v in self.__boundaries_model.selection:
            if isinstance(v, BoundaryGroup):
                self.__boundaries_model.root_elements.remove(v)
                for vv in v.elements:
                    vv.boundary_type = 'patch'
                    self.__boundaries_model.root_elements.append(vv)
        signal('boundary:*')

    @diceSync('boundary:')
    def __boundary_sync(self, path):
        if path == 'is_cyclic':
            for s in self.boundaries_model.selection:
                if hasattr(s, 'boundary_type'):
                    if s.boundary_type in ("cyclic", "cyclicAMI"):
                        return True
            return False

        result = None
        for s in self.boundaries_model.selection:
            if hasattr(s, path):
                value = getattr(s, path)
                if value is not None:
                    if result is None:
                        result = value
                    elif result != value:
                        return None
        return result

    @__boundary_sync.setter
    def __boundary_sync(self, path, value):
        for s in self.boundaries_model.selection:
            if hasattr(s, path):
                if getattr(s, path) is not None:
                    setattr(s, path, value)
        signal('boundary:*')
        return True


    def w_model_selection_changed(self, model, selected, deselected):
        for v in deselected:
            if hasattr(v, 'vis'):
                v.vis.set_selected(False)
                v.vis.opacity=0.8
        for v in selected:
            if hasattr(v, 'vis'):
                v.vis.set_selected(True)
                v.vis.opacity=1
        props = set()
        for v in self.__boundaries_model.selection:
            if isinstance(v, Boundary):
                props.add('boundary')
            elif isinstance(v, BoundaryGroup):
                props.add('group')
        self.__boundaries_props = sorted(props)
        self.selection_changed()
        signal('boundary:*')

    def w_geometry_object_clicked(self, obj, *args, **kwargs):
        if obj is None:
            self.__boundaries_model.current_item = None

    @diceProperty('QVariant', name='hasProps', notify=selection_changed)
    def has_props(self):
        return bool([v for v in self.boundaries_model.selection if isinstance(v, Boundary)])

    @diceProperty('QVariantList', name='boundaryPropsModel',  notify=selection_changed)
    def boundary_props_model(self):
        return self.__boundaries_props
