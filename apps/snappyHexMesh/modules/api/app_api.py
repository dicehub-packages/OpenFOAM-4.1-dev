
from .api import RootApi
from .bounding_box_api import BoundingBoxApi
from .material_point_api import MaterialPointApi
from .refinement_api import RefinementApi

class AppApi(RootApi):
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.__app = app
        self.__bounding_box = BoundingBoxApi(app)
        self.__material_point = MaterialPointApi(app)
        self.__refinement = RefinementApi(app)
        
    @property
    def app(self):
        return self.__app

    @property
    def bounding_box(self):
        return self.__bounding_box

    @property
    def material_point(self):
        return self.__material_point

    @property
    def refinement(self):
        return self.__refinement