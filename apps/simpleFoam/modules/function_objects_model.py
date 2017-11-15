import copy

from PyFoam.Basics.DataStructures import DictProxy

from dice_tools import *
from dice_tools.helpers.xmodel import *


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


class TreeNode(ModelItem):

    def __init__(self, name, node_type, **kwargs):
        super().__init__(**kwargs)
        self.__name = name
        self.__node_type = node_type
        wizard.subscribe(self, self)

    def w_model_remove_items(self, *args, **kwargs):
        wizard.w_model_update_item(self)

    def w_model_insert_items(self, *args, **kwargs):
        wizard.w_model_update_item(self)

    @modelRole('name')
    def name(self):
        return self.__name

    @modelRole('label')
    def label(self):
        return '{0} ({1})'.format(self.name, self.count)

    @modelRole('count')
    def count(self):
        return len(self.elements)

    @modelRole('type')
    def type(self):
        return "TreeNode"

    @modelRole('nodeType')
    def node_type(self):
        return self.__node_type


class FunctionObject:

    def __init__(self, name, app, **kwargs):
        self.__name = name
        self.__app = app

        print(">> ", app)
        print(">> ", name)

        wizard.w_function_object_created(self)

    @property
    def path(self):
        return 'foam:system/functionObjects ' + self.name

    @property
    def app(self):
        return self.__app

    @modelRole('name')
    def name(self):
        return self.__name

    @modelRole('label')
    def label(self):
        return self.name

    @modelRole('type')
    def type(self):
        return self.app[self.path + ' type']

    @modelMethod('remove')
    def remove_function_object(self):
        type = self.type
        self.app[self.path] = None
        wizard.w_function_object_removed(self, type)


class ForcesMonitor(FunctionObject):

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)


class ForceCoeffsMonitor(FunctionObject):

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)


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
            "libs": ["libforces.so"],
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
        self.__function_objects = self.app.function_objects

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
        for f_name in self.__function_objects:
            function_object_type = self.__function_objects[f_name]['type']
            if function_object_type in self.function_obj_types:
                self.function_obj_types[function_object_type](f_name, app=self.app)

    @diceProperty('QVariant', name='properties')
    def properties(self):
        return self.__props_model

    def w_model_selection_changed(self, model, selected, deselected):
        properties = [
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

    def w_function_object_created(self, item):
        print("created >>", item)
        if item.type == "forces":
            self.__forces_node.elements.append(item)
        elif item.type == "forceCoeffs":
            self.__force_coeffs_node.elements.append(item)

    def w_function_object_removed(self, item, type):
        print("removed >>", item)
        print("removed >>", item.type)
        # self.__forces_node.elements.remove(item)
        if type == "forces":
            self.__forces_node.elements.remove(item)
        elif type == "forceCoeffs":
            self.__force_coeffs_node.elements.remove(item)

    @diceSlot('QString', name='addFunctionObject')
    def add_function_object(self, node_type, obj_name=None):
        print("-->>>", node_type, obj_name)
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


    #     properties = [
    #         ('Forces', ForcesMonitor, 'Forces.qml'),
    #         ('ForcesCoeffs', ForcesCoeffsMonitor, 'ForcesCoeffs.qml')
    #     ]
    #
    #     result_props = []
    #
    #     for title, tp, source in properties:
    #         for s in self.__model.selection:
    #             if isinstance(s, tp):
    #                 result_props.append(PropertyItem(
    #                     title, source))
    #                 break
    #     for v in self.__props_model.root_elements[:]:
    #         for p in result_props:
    #             if p.title == v.title:
    #                 break
    #         else:
    #             self.__props_model.root_elements.remove(v)
    #
    #     elements = self.__props_model.root_elements
    #     for i, p in enumerate(result_props):
    #         if i < len(elements):
    #             v = elements[i]
    #             if v.title != p.title:
    #                 elements.insert(i, p)
    #         else:
    #             elements.append(p)
    #
    #     for i in result_props:
    #         print(">>>", i)