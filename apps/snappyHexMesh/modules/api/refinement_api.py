from .api import Api
from .geometry_api import GeometryApi
from .searchable_box_api import SearchableBoxApi
from .searchable_sphere_api import SearchableSphereApi
from modules.refinement_items import *

_refinement_object_types = {
    SearchableBox: SearchableBoxApi,
    SearchableSphere: SearchableSphereApi,
}

class RefinementApi(Api):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.__app = app

    def get_geometry(self, name):
        return GeometryApi(name, self.__app)

    def clear_refinement_objects(self):
        for i in list(self.__app.refinement.model.elements_of(RegionRefinement)):
            i.remove_refinement()

    def create_refinement_object(self, type_name, name):
        for i in self.__app.refinement.model.elements_of(RegionRefinement):
            if i.name == name:
                i.remove_refinement()
        self.__app.refinement.add_refinement_object(type_name, name)

    def refinement_object(self, name):
        for i in self.__app.refinement.model.elements_of(RegionRefinement):
            if i.name == name:
                return _refinement_object_types[type(i)](name=name, app=self.__app)
        raise Exception('refinement object not found')

    def dump(self, path):
        super().dump(path)
        print(path+'.clear_refinement_objects()', '\n')
        for i in self.__app.refinement.model.elements_of(RegionRefinement):
            print(path+'.create_refinement_object("%s", "%s")'%(i.template_name, i.name), '\n')
            # print(self.refinement_object(i.name))
            self.refinement_object(i.name).dump(path+'.refinement_object("%s")'%i.name)