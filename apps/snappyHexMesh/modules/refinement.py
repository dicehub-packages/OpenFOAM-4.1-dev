"""
Refinement Objects
==================
"""
from dice_tools import DICEObject, diceSlot, diceProperty, diceSignal, wizard, signal
from dice_vtk.geometries import *
from dice_tools.helpers.xmodel import standard_model, modelRole
from .refinement_items import *
import copy

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

class Refinement(DICEObject):

    ref_obj_types = {
        "searchableBox": SearchableBox,
        "searchableSphere": SearchableSphere,
        # "searchableCylinder": Tube,
        # "searchablePlate": Plane,
        # "searchablePlane": Plane,
        # "searchableDisk": Disk
    }

    ref_object_templates = {
        "refinementBox": {
            "type": "searchableBox",
            "min": [0, 0, 0],
            "max": [1, 1, 1]
        },
        "refinementSphere": {
            "type": "searchableSphere",
            "centre": [0, 0, 0],
            "radius": 1
        },
        "refinementCylinder": {
            "type": "searchableCylinder",
            "point1": [0, 0, 0],
            "point2": [1, 0, 0],
            "radius": 1
        },
        "refinementPlate": {
            "type": "searchablePlate",
            "origin": [0, 0, 0],
            "span": [1, 2, 0]
        },
        "refinementPlanePaN": {
            "type": "searchablePlane",
            "planeType": "pointAndNormal",
            "pointAndNormalDict": {
                "basePoint": [0, 0, 0],
                "normalVector": [1, 0, 0]
            }
        },
        "refinementPlane3P": {
            "type": "searchablePlane",
            "planeType": "embeddedPoints",
            "embeddedPointsDict": {
                "point1": [0, 0, 0],
                "point2": [1, 0, 1],
                "point3": [1, 0, 2]
            }
        },
        "refinementDisk": {
            "type": "searchableDisk",
            "origin": [0, 0, 0],
            "normal": [0, 0, 1],
            "radius": 1
        }
    }

    geometry_path = 'foam:system/snappyHexMeshDict geometry'

    def __init__(self, app, **kwargs):
        super().__init__(base_type='QObject', **kwargs)
        print("Initialize refinement objects")
        self.__app = app

        # Load refinementObjects
        # ======================

        self.__refinement = {}

        self.__model = standard_model(
            TreeNode,
            Surface,
            SurfaceRegion,
            SearchableBox,
            SearchableSphere,
            RegionLevel,
            Boundary,
            BoundariesNode,
            RegionRefinement
        )

        self.__props_model = standard_model(PropertyItem)

        self.__geometry_node = TreeNode('Geometry')
        self.__refinement_node = TreeNode('Refinement')
        self.__boundaries_node = BoundariesNode('Boundary', self.__app)

        for v in self.__app.bounding_box.boundaries_model.root_elements:
            self.__boundaries_node.elements.append(v)

        self.__model.root_elements.append(self.__geometry_node)
        self.__model.root_elements.append(self.__refinement_node)
        self.__model.root_elements.append(self.__boundaries_node)

        wizard.subscribe(self.w_geometry_created)
        wizard.subscribe(self.w_geometry_removed)
        wizard.subscribe(self.w_refinement_created)
        wizard.subscribe(self.w_refinement_removed)
        wizard.subscribe(self.w_geometry_object_clicked)
        wizard.subscribe(self, self.__model)
        wizard.subscribe(self, self.__app.bounding_box.vis_obj)

        for k, v in self.app[self.geometry_path].items():
            if v['type'] in self.ref_obj_types:
                refinement_type = v['type']
                self.ref_obj_types[refinement_type](k, app=self.__app)

    def w_multipatchbox_face_clicked(self, obj, index):
        self.__model.current_item = \
                self.__boundaries_node.elements[index]

    @property
    def app(self):
        return self.__app

    @property
    def geometry_node(self):
        return self.__geometry_node

    @property
    def refinement_node(self):
        return self.__refinement_node

    def w_geometry_object_clicked(self, obj, *args, **kwargs):
        if obj == None:
            self.__model.current_item = None

    def w_geometry_created(self, item):
        self.__geometry_node.elements.append(item)

    def w_geometry_removed(self, item):
        self.__geometry_node.elements.remove(item)

    def w_refinement_created(self, item):
        self.__refinement_node.elements.append(item)

    def w_refinement_removed(self, item):
        self.__refinement_node.elements.remove(item)

    @diceProperty('QVariant', name='model')
    def model(self):
        return self.__model

    @diceProperty('QVariant', name='properties')
    def properties(self):
        return self.__props_model
        
    def w_model_selection_changed(self, model, selected, deselected):

        for v in deselected:
            if isinstance(v, Surface):
                for m in v.elements:
                    if hasattr(m, 'vtk_obj'):
                        m.vtk_obj.set_selected(False)
            elif hasattr(v, 'vtk_obj'):
                v.vtk_obj.set_selected(False)
            elif isinstance(v, Boundary):
                s = self.__app.bounding_box.vis_obj.selected_faces
                if v.face in s:
                    s.remove(v.face)
                    wizard.unsubscribe(self, self.__app.bounding_box.vis_obj)
                    self.__app.bounding_box.vis_obj.selected_faces = s
                    wizard.subscribe(self, self.__app.bounding_box.vis_obj)

        for v in selected:
            if isinstance(v, Surface):
                for m in v.elements:
                    if hasattr(m, 'vtk_obj'):
                        m.vtk_obj.set_selected(True)
            elif hasattr(v, 'vtk_obj'):
                v.vtk_obj.set_selected(True)
            elif isinstance(v, Boundary):
                s = self.__app.bounding_box.vis_obj.selected_faces
                if v.face not in s:
                    s.append(v.face)
                    wizard.unsubscribe(self, self.__app.bounding_box.vis_obj)
                    self.__app.bounding_box.vis_obj.selected_faces = s
                    wizard.subscribe(self, self.__app.bounding_box.vis_obj)

        properties = [
            ('Surface', Surface, 'Surface.qml'),
            ('Region', SurfaceRegion, 'SurfaceRegion.qml'),
            ('Layers', SurfaceRegion, 'Layers.qml'),
            ('Levels', RegionRefinement, 'RegionRefinement.qml'),
            ('Feature', Surface, 'Feature.qml'),
            ('Region Level', RegionLevel, 'RegionLevel.qml'),
            ('Boundary', Boundary, 'Boundary.qml'),
            ('SearchableBox', SearchableBox, 'SearchableBox.qml'),
            ('SearchableSphere', SearchableSphere, 'SearchableSphere.qml'),
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
        signal('refinement*')

    @diceSlot('QString', name='addRefinementObject')
    def add_refinement_object(self, type_name, obj_name=None):
        if not obj_name:
            obj_name = type_name
            count = 0
            while obj_name in self.app[self.geometry_path]:
                count += 1
                obj_name = '%s_%i'%(type_name, count)
        elif obj_name in self.app[self.geometry_path]:
            raise Exception("can't create refinement object")
        template = self.ref_object_templates[type_name]
        self.app[self.geometry_path + ' ' + obj_name] = copy.deepcopy(template)
        self.ref_obj_types[template['type']](obj_name, app=self.__app)
        wizard.w_modified('snappy_hex_mesh_dict')
        return obj_name

    @diceSlot(name='addRegionLevel')
    def add_region_level(self):
        for s in self.__model.selection:
            if isinstance(s, RegionRefinement):
                s.add_region_level()
        signal('refinement*')

    @diceSlot('int', name='removeRegionLevel')
    def remove_region_level(self, index):
        for s in self.__model.selection:
            if isinstance(s, RegionRefinement):
                s.remove_region_level(index)
        signal('refinement*')

    def refinement_get(self, path):
        if path == 'RegionRefinement.region_modes_list':
            result = None
            for s in self.__model.selection:
                if isinstance(s, RegionRefinement):
                    if result is None:
                        result = set(s.modes)
                    else:
                        result = result & set(s.modes)
            if result:
                return [v for v in result]
            else:
                return []
        elif path.startswith('RegionRefinement.level.'):
            level = int(path.rsplit('.', maxsplit=1)[-1])
            result = None
            for s in self.__model.selection:
                if isinstance(s, RegionRefinement):
                    value = s.get_level_data(level)
                    if value is not None:
                        if result is None:
                            result = value
                        else:
                            for i, x in enumerate(value):
                                if x != result[i]:
                                    result[i] = None   
            return result

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

    def refinement_set(self, path, value):
        print('zzzzzzzzzzzzzzzzzzzzzzz')
        if path.startswith('RegionRefinement.level.'):
            level = int(path.rsplit('.', maxsplit=1)[-1])
            for s in self.__model.selection:
                if isinstance(s, RegionRefinement):
                    v = s.get_level_data(level)
                    for i, x in enumerate(value):
                        if value[i] is not None:
                            v[i] = value[i]
                    s.set_level_data(level, v)
            signal('refinement*')
            return False

        p = path.split('.')
        prop_class, prop = globals()[p[0]], p[1]
        for s in self.__model.selection:
            print (s, path, prop_class, prop)
            if isinstance(s, prop_class):
                try:
                    v = getattr(s, prop)
                    for i, x in enumerate(value):
                        if value[i] is not None:
                            v[i] = value[i]
                    setattr(s, prop, v)
                except TypeError:
                    print('invoke set',getattr(s, prop))
                    setattr(s, prop, value)
                    print('gfhfgh->>',getattr(s, prop))
        signal('refinement*')
        return False