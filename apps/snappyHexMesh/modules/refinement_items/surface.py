import os

from dice_tools import wizard
from dice_tools.helpers.xmodel import modelRole, modelMethod, ModelItem
from stl.mesh import Mesh
from .region_refinement import RegionRefinement
from .surface_region import SurfaceRegion


class Surface(RegionRefinement):

    default_region_mode = "inside"
    region_modes_list = ["inside", "outside", "distance"]

    def __init__(self, path, app, **kwargs):
        super().__init__(**kwargs)
        self.__app = app
        self.__path = path
        self.__load()

    @property
    def path(self):
        return self.__path

    @property
    def file_name(self):
        return os.path.splitext(self.__name)[0]

    @property
    def app(self):
        return self.__app

    @property
    def geometry_path(self):
        return 'foam:system/snappyHexMeshDict geometry ' + self.name
    
    @property
    def refinement_path(self):
        return 'foam:system/snappyHexMeshDict castellatedMeshControls refinementSurfaces ' + self.name

    def __load(self):
        # load stl files and create objects in view
        self.__visible = True
        self.__name = os.path.basename(self.__path)

        if self.app[self.geometry_path] is None:
            self.app[self.geometry_path] = {
                'type': 'triSurfaceMesh',
                'regions': {}
            }

        if self.app[self.refinement_path] is None:
            self.app[self.refinement_path] = {
                'level': [0, 0],
                'regions': {}
            } 

        self.setup_region(["inside", "outside", "distance"], "inside")

        for m in Mesh.from_multi_file(self.__path):

            # Add regions as children to this element
            # =======================================
            self.elements.append(SurfaceRegion(self, m, app=self.app))

        # Add this element to root
        # ========================
        wizard.w_geometry_created(self)

    @property
    def is_surface(self):
        return True

    @property
    def is_region(self):
        return False

    @property
    def name(self):
        # readonly role, renaming in stl import app
        return os.path.basename(self.__path)

    @modelRole('isVisible')
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, value):
        self.__visible = value
        for v in self.elements:
            if hasattr(v, 'visible'):
                v.visible = value

    def remove(self):
        for v in self.elements:
            if hasattr(v, 'remove_vis'):
                v.remove_vis()
        wizard.w_geometry_removed(self)

    @property
    def surface_level(self):
        return list(self.app[self.refinement_path + ' level'])

    @surface_level.setter
    def surface_level(self, value):
        self.app[self.refinement_path + ' level'] = [value[0], int(value[1])]

    @property
    def cell_zone_inside(self):
        if self.is_region:
            return self.app[self.refinement_path + ' cellZoneInside']
        return -1

    @cell_zone_inside.setter
    def cell_zone_inside(self, value):
        if self.is_region:
            self.app[self.refinement_path + ' cellZoneInside'] = value

    @property
    def face_type(self):
        if self.is_region:
            return self.app[self.refinement_path + ' faceType']

    @face_type.setter
    def face_type(self, value):
        if self.is_region:
            self.app[self.refinement_path + ' faceType'] = value

    @property
    def is_region(self):
        return self.app[self.refinement_path + ' faceZone'] is not None

    @is_region.setter
    def is_region(self, value):
        if value:
            if self.app[self.refinement_path + ' faceZone'] is None:
                self.app[self.refinement_path + ' faceZone'] = self.__name
                self.app[self.refinement_path + ' cellZone'] = self.__name
                self.app[self.refinement_path + ' cellZoneInside'] = "inside"
                self.app[self.refinement_path + ' faceType'] = "internal"
        else:
            if self.app[self.refinement_path + ' faceZone'] is not None:
                self.app[self.refinement_path + ' faceZone'] = None
                self.app[self.refinement_path + ' cellZone'] = None
                self.app[self.refinement_path + ' cellZoneInside'] = None
                self.app[self.refinement_path + ' faceType'] = None

    @modelRole('label')
    def label(self):
        return self.name

    @modelMethod('showInScene')
    def show_in_scene(self):
        objs = []
        for v in self.elements:
            objs.append(v.vtk_obj)
        wizard.w_reset_camera_to_object(objs)

    @property
    def file_index(self):
        file_name_e_mesh = '"{0}.eMesh"'.format(self.file_name)
        features = self.app['foam:system/snappyHexMeshDict castellatedMeshControls features']
        for index, feature_dict in enumerate(features):
            if feature_dict["file"] == file_name_e_mesh:
                return index

    @modelRole('featureLevel')
    def feature_level(self):
        file_name_e_mesh = '"{0}.eMesh"'.format(self.file_name)
        features = self.app['foam:system/snappyHexMeshDict castellatedMeshControls features']
        for feature_dict in features:
            if feature_dict["file"] == file_name_e_mesh:
                return feature_dict['level']

    @feature_level.setter
    def feature_level(self, value):
        file_name_e_mesh = '"{0}.eMesh"'.format(self.file_name)
        features = self.app['foam:system/snappyHexMeshDict castellatedMeshControls features']
        for index, feature_dict in enumerate(features):
            if feature_dict["file"] == file_name_e_mesh:
                p = 'foam:system/snappyHexMeshDict castellatedMeshControls features %i level'%index
                self.app[p] = value

    @property
    def has_feature(self):
        file_name_e_mesh = '"{0}.eMesh"'.format(self.file_name)
        features = self.app['foam:system/snappyHexMeshDict castellatedMeshControls features']
        for feature_dict in features:
            if feature_dict["file"] == file_name_e_mesh:
                return True
        return False

    @has_feature.setter
    def has_feature(self, value):
        file_name_e_mesh = '"{0}.eMesh"'.format(self.file_name)
        features_path = 'foam:system/snappyHexMeshDict castellatedMeshControls features'
        extract_path = 'foam:system/surfaceFeatureExtractDict ' + self.name
        features = self.app[features_path]

        if value:
            if self.has_feature:
                return

            features.append(
                {
                    "file": file_name_e_mesh,
                    "level": 0
                }
            )

            self.app[features_path] = features

            if self.app[extract_path] is not None:
                return

            self.app[extract_path] = {
                "extractionMethod": "extractFromSurface",
                "extractFromSurfaceCoeffs": {
                    "includedAngle": 0
                },
                "subsetFeatures": {
                    "nonManifoldEdges": False,
                    "openEdges": True,
                    "insideBox": '(0 0 0) (1 1 1)'
                },
                "writeObj": True
            }

        else:
            index = self.file_index
            if index is not None:
                self.app[features_path + ' %i'%index] = None
            self.app[extract_path] = None

    @property
    def included_angle(self):
        if self.has_feature:
            path = 'foam:system/surfaceFeatureExtractDict ' + self.name + ' extractFromSurfaceCoeffs includedAngle'
            return self.app[path]

    @included_angle.setter
    def included_angle(self, value):
        if self.has_feature:
            path = 'foam:system/surfaceFeatureExtractDict ' + self.name + ' extractFromSurfaceCoeffs includedAngle'
            self.app[path] = value

    @property
    def extraction_method(self):
        if self.has_feature:
            path = 'foam:system/surfaceFeatureExtractDict ' + self.name + ' extractionMethod'
            return self.app[path]

    @extraction_method.setter
    def extraction_method(self, value):
        if self.has_feature:
            path = 'foam:system/surfaceFeatureExtractDict ' + self.name + ' extractionMethod'
            self.app[path] = value

    @property
    def write_obj(self):
        if self.has_feature:
            path = 'foam:system/surfaceFeatureExtractDict ' + self.name + ' writeObj'
            return bool(self.app[path])

    @write_obj.setter
    def write_obj(self, value):
        if self.has_feature:
            path = 'foam:system/surfaceFeatureExtractDict ' + self.name + ' writeObj'
            self.app[path] = value

    @property
    def non_manifold_edges(self):
        if self.has_feature:
            path = 'foam:system/surfaceFeatureExtractDict ' + self.name + ' subsetFeatures nonManifoldEdges'
            return bool(self.app[path])

    @non_manifold_edges.setter
    def non_manifold_edges(self, value):
        if self.has_feature:
            path = 'foam:system/surfaceFeatureExtractDict ' + self.name + ' subsetFeatures nonManifoldEdges'
            self.app[path] = value

    @property
    def open_edges(self):
        if self.has_feature:
            path = 'foam:system/surfaceFeatureExtractDict ' + self.name + ' subsetFeatures openEdges'
            return bool(self.app[path])

    @open_edges.setter
    def open_edges(self, value):
        if self.has_feature:
            path = 'foam:system/surfaceFeatureExtractDict ' + self.name + ' subsetFeatures openEdges'
            self.app[path] = value
