
from .api import Api
from modules.refinement_items import Surface

class GeometryApi(Api):

    def __init__(self, name, app, **kwargs):
        super().__init__(**kwargs)
        self.__name = name
        self.__app = app
        self.__get()

    def __get(self):
        for i in self.__app.refinement.model.elements_of(Surface):
            if i.name == self.__name:
                return i
        raise Exception('geometry not found')