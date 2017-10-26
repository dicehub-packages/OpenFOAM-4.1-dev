"""
Background Mesh with BlockMesh:
===============================
Module to create a bounding box for snappyHexMesh
"""

# DICE tools imports
# ==================
from dice_tools import diceSignal, wizard
from dice_tools.helpers.xmodel import standard_model

# DICE Libs
# =========
from dice_vtk.geometries import MultiPatchBox
from dice_tools import DICEObject, diceProperty, diceSlot, wizard
from vtk import vtkBoundingBox
from .refinement_items import SurfaceRegion
from contextlib import contextmanager
import stl
from .refinement_items import *


class BoundingBox(DICEObject):
    """
    Initial background Mesh of hexahedral cells that fills a region
    consisting of geometries.
    """
    bm_vertices_path = 'foam:constant/polyMesh/blockMeshDict vertices'
    bm_blocks_path = 'foam:constant/polyMesh/blockMeshDict blocks'
    bm_boundary_path = 'foam:constant/polyMesh/blockMeshDict boundary'

    def __init__(self, app, **kwargs):
        super().__init__(base_type='QObject', **kwargs)
        self.__app = app

        self.__bm_vertices = self.__app[self.bm_vertices_path]
        self.__bm_blocks = self.__app[self.bm_blocks_path]
        self.__bm_boundary = self.__app[self.bm_boundary_path]

        self.__cells_size_value = self.calculate_cells_size()
        self.__old_spacing = [0, 0, 0]
        self.__bm_vis = MultiPatchBox(name='Bounding box')

        self.__app.vis_add_object(self.__bm_vis)
        self.__bm_vis.min = self.bb_min
        self.__bm_vis.max = self.bb_max
        self.__bm_vis.resolution = self.cells_num

        self.__boundaries_model = standard_model(Boundary)
        
        indexes = 0, 2, 4, 1, 3, 5
        for k, i in enumerate(indexes):
            self.__boundaries_model.root_elements.append(Boundary(self.__app, k, i))

        wizard.subscribe(self, self.__bm_vis)

    @property
    def vis_obj(self):
        return self.__bm_vis

    def w_property_changed(self, obj, name, value):
        wizard.unsubscribe(self, self.__bm_vis)
        if name == 'minmax':
            self.bb_min = self.__bm_vis.min
            self.bb_max = self.__bm_vis.max
        wizard.subscribe(self, self.__bm_vis)

    @diceSlot(int, name='highlightFace')
    def highlight_face(self, num):
        self.__bm_vis.selected_faces = [num]

    def __update_verts(self):
        bb_min = self.bb_min
        bb_max = self.bb_max
        self.__bm_vertices[1] = [bb_max[0], bb_min[1], bb_min[2]]
        self.__bm_vertices[2] = [bb_max[0], bb_max[1], bb_min[2]]
        self.__bm_vertices[3] = [bb_min[0], bb_max[1], bb_min[2]]
        self.__bm_vertices[4] = [bb_min[0], bb_min[1], bb_max[2]]
        self.__bm_vertices[5] = [bb_max[0], bb_min[1], bb_max[2]]
        self.__bm_vertices[7] = [bb_min[0], bb_max[1], bb_max[2]]
        self.__app[self.bm_vertices_path] = self.__bm_vertices

    @diceProperty('QVariantList', name='boundingBoxMin')
    def bb_min(self):
        return list(self.__bm_vertices[0])

    @bb_min.setter
    def bb_min(self, value):
        self.__bm_vertices[0] = value
        self.__update_verts()
        self.__bm_vis.min = value
        self.update_cells()

    @diceProperty('QVariantList', name='boundingBoxMax')
    def bb_max(self):
        return list(self.__bm_vertices[6])

    @bb_max.setter
    def bb_max(self, value):
        self.__bm_vertices[6] = value
        self.__update_verts()
        self.__bm_vis.max = value
        self.update_cells()

    def update_cells(self):
        if self.__app["config:blockMesh-useCellSize"]:
            self.cells_num = self.calculate_n_cells()
        else:
            self.cells_size = self.calculate_cells_size()

    @diceProperty('QVariantList', name='cellsNum')
    def cells_num(self):
        return [int(v) for v in self.__bm_blocks[2]]
    
    @cells_num.setter
    def cells_num(self, value):
        self.__bm_blocks[2] = [int(v) for v in value]
        self.__app[self.bm_blocks_path] = self.__bm_blocks
        if not self.__app["config:blockMesh-useCellSize"]:
            self.cells_size = self.calculate_cells_size()
        self.__bm_vis.resolution = [int(v) for v in value]

    @diceProperty('QVariantList', name='cellsSize')
    def cells_size(self):
        return self.__cells_size_value

    @cells_size.setter
    def cells_size(self, value):
        self.__cells_size_value = value
        if self.__app["config:blockMesh-useCellSize"]:
            self.cells_num = self.calculate_n_cells()

    @diceProperty('QVariantList', name='additionalSpacing')
    def __spacing(self):
        return self.__app["config:blockMesh-spacing"]

    @__spacing.setter
    def __spacing(self, value):
        self.__app["config:blockMesh-spacing"] = value

    @diceProperty(bool, name='sizeOrNumber')
    def use_cell_size(self):
        return self.__app["config:blockMesh-useCellSize"]

    @use_cell_size.setter
    def use_cell_size(self, value):
        self.__app["config:blockMesh-useCellSize"] = value
        if value:
            self.cells_num = self.calculate_n_cells()
        else:
            self.cells_size = self.calculate_cells_size()

    @diceProperty('QVariant', name='boundariesModel')
    def boundaries_model(self):
        return self.__boundaries_model

    @diceSlot(name='calculateBoundingBox')
    def calculate_bounding_box(self):
        minx = maxx = miny = maxy = minz = maxz = None
        for o in self.__app.refinement.model.elements_of(SurfaceRegion):
            for p in o.mesh.points:
                # p contains (x, y, z)
                if minx is None:
                    minx = p[stl.Dimension.X]
                    maxx = p[stl.Dimension.X]
                    miny = p[stl.Dimension.Y]
                    maxy = p[stl.Dimension.Y]
                    minz = p[stl.Dimension.Z]
                    maxz = p[stl.Dimension.Z]
                else:
                    maxx = max(p[stl.Dimension.X], maxx)
                    minx = min(p[stl.Dimension.X], minx)
                    maxy = max(p[stl.Dimension.Y], maxy)
                    miny = min(p[stl.Dimension.Y], miny)
                    maxz = max(p[stl.Dimension.Z], maxz)
                    minz = min(p[stl.Dimension.Z], minz)

        bounds = minx, miny, minz, maxx, maxy, maxz

        # if bbox is valid update bounding mesh size
        if bounds[0] is not None:
            bounds = self.calculate_spacing(bounds)
            self.bb_min  = bounds[:3]
            self.bb_max  = bounds[3:]

    def calculate_spacing(self, bounds):
        # calculate spacing delta
        delta = list(map(lambda v: (v[1] - v[0]) * v[2] / 100,
            zip(bounds[:3], bounds[3:], self.__spacing)))

        # compute minimum
        bb_min = list(map(lambda v: round(v[0] - v[1], 4), 
            zip(bounds[:3], delta)))

        # compute maximum
        bb_max = list(map(lambda v: round(v[0] + v[1], 4), 
            zip(bounds[3:], delta)))

        return bb_min + bb_max

    def calculate_cells_size(self):
        def f(v):
            bb_min, bb_max, cell_n = v
            return (bb_max - bb_min) / cell_n if cell_n != 0 else 0
        return list(map(f, zip(self.bb_min, self.bb_max, self.cells_num)))

    def calculate_n_cells(self):
        def f(v):
            bb_min, bb_max, cell_size = v
            return (bb_max - bb_min) / cell_size if cell_size != 0 else 0
        return list(map(f, zip(self.bb_min, self.bb_max, self.cells_size)))
