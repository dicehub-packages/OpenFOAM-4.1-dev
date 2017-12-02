import copy

from dice_tools import *
from dice_tools.helpers.xmodel import *
from .function_objects import *


class PropertyItem:
    def __init__(self, title, source):
        self.__title = title
        self.__source = source

    @modelRole("title")
    def title(self):
        return self.__title

    @modelRole("source")
    def source(self):
        return self.__source


class FunctionObjectsApp(DICEObject):

    function_obj_types = {
        "forces": ForcesMonitor,
        "forceCoeffs": ForceCoeffsMonitor
    }

    function_object_templates = {
        "forces": {
            "type": "forces",
            "libs": ["\"libforces.so\""],
            "patches": [],
            "p": "p",
            "U": "U",
            "rho": "rhoInf",
            "rhoInf": 1,
            "pRef": 0,
            "porosity": False,
            "writeFields": True,
            "writeControl": "timeStep",
            "timeInterval": 1,
            "log": True,
            "CofR": [0, 0, 0],
            "pitchAxis": [0, 1, 0]
        },
        "forceCoeffs": {
            "type": "forceCoeffs",
            "libs": ["\"libforces.so\""],
            "patches": [],
            "p": "p",
            "U": "U",
            "rho": "rhoInf",
            "rhoInf": 1,
            "liftDir": [0, 0, 1],
            "dragDir": [1, 0, 0],
            "CofR": [0, 0, 0],
            "pitchAxis": [0, 1, 0],
            "magUInf": 0,
            "lRef": 1,
            "Aref": 1
        }
    }

    def __init__(self, app, **kwargs):
        super().__init__(base_type='QObject', **kwargs)
        self.__app = app
        self.__function_objects_dict = self.app.function_objects_dict

        self.__model = standard_model(
            TreeNode,
            ForcesMonitor,
            ForceCoeffsMonitor
        )

        self.__props_model = standard_model(PropertyItem)

        self.__forces_node = TreeNode('Forces', node_type='forces')
        self.__force_coeffs_node = TreeNode('Force Coefficients',
                                            node_type='forceCoeffs')

        self.__model.root_elements.append(self.__forces_node)
        self.__model.root_elements.append(self.__force_coeffs_node)

        wizard.subscribe(self, self.__model)
        wizard.subscribe(self.w_function_object_created)
        wizard.subscribe(self.w_function_object_removed)
        wizard.subscribe(self.w_function_object_changed)

        self.load_model()

    @property
    def app(self):
        return self.__app

    @property
    def path(self):
        return "foam:system/functionObjects"

    @diceProperty('QVariant', name='model')
    def model(self):
        return self.__model

    def load_model(self):
        for f_name in self.__function_objects_dict:
            function_object_type = self.__function_objects_dict[f_name]['type']
            if function_object_type in self.function_obj_types:
                self.function_obj_types[function_object_type](f_name, app=self.app)

    @diceProperty('QVariant', name='properties')
    def properties(self):
        return self.__props_model

    def w_model_selection_changed(self, model, selected, deselected):
        properties = [
            ('default', TreeNode, 'Default.qml'),
            ('forces', ForcesMonitor, 'Forces.qml'),
            ('forceCoeffs', ForceCoeffsMonitor, 'ForceCoeffs.qml')
        ]

        result_props = []

        for title, tp, source in properties:
            for s in self.__model.selection:
                if isinstance(s, tp):
                    result_props.append(PropertyItem(
                        title, source))
                    break
        for v in self.__props_model.root_elements[:]:
            for p in result_props:
                if p.title == v.title:
                    break
            else:
                self.__props_model.root_elements.remove(v)

        elements = self.__props_model.root_elements
        for i, p in enumerate(result_props):
            if i < len(elements):
                v = elements[i]
                if v.title != p.title:
                    elements.insert(i, p)
            else:
                elements.append(p)
        signal('functionObjects:*')

    def w_function_object_created(self, item):
        if item.type == "forces":
            self.__forces_node.elements.append(item)
        elif item.type == "forceCoeffs":
            self.__force_coeffs_node.elements.append(item)
        self.app.plots.add_function_objects_plot(item)

    def w_function_object_removed(self, item, type):
        if type == "forces":
            self.__forces_node.elements.remove(item)
        elif type == "forceCoeffs":
            self.__force_coeffs_node.elements.remove(item)
        self.app.plots.remove_function_objects_plot(item)

    def w_function_object_changed(self, item, **kwargs):
        if "new_name" and "old_name" in kwargs:
            for it in self.app.plots.model.root_elements:
                if it.name == kwargs["old_name"]:
                    it.name = kwargs["new_name"]
                    break

    @diceSlot('QString', name='addFunctionObject')
    def add_function_object(self, node_type, obj_name=None):
        if not obj_name:
            obj_name = node_type
            count = 0
            while obj_name in self.app[self.path]:
                count += 1
                obj_name = '{0}_{1}'.format(node_type, count)
        elif obj_name in self.app[self.path]:
            raise Exception("can't create functionObject")

        template = self.function_object_templates[node_type]
        self.app[self.path + ' ' + obj_name] = copy.deepcopy(template)

        self.function_obj_types[template['type']](obj_name, app=self.__app)

    def function_objects_get(self, path):
        p = path.split('.')
        prop_class, prop = globals()[p[0]], p[1]
        result = None
        for s in self.__model.selection:
            if isinstance(s, prop_class):
                value = getattr(s, prop)
                if value is not None:
                    if result is None:
                        result = value
                    else:
                        try:
                            for i, x in enumerate(value):
                                if x != result[i]:
                                    result[i] = None
                        except TypeError:
                            if result != value:
                                return None
        return result

    def function_objects_set(self, path, value):
        p = path.split('.')
        prop_class, prop = globals()[p[0]], p[1]
        for s in self.__model.selection:
            print(s, path, prop_class, prop)
            if isinstance(s, prop_class):
                try:
                    v = getattr(s, prop)
                    for i, x in enumerate(value):
                        if value[i] is not None:
                            v[i] = value[i]
                    setattr(s, prop, v)
                except TypeError:
                    # print('invoke set', getattr(s, prop))
                    setattr(s, prop, value)
        signal('functionObjects:*')
        return False

    @diceSlot('QString')
    def call(self, f_name):
        for s in self.__model.selection:
            if hasattr(s, f_name):
                getattr(s, f_name)()
