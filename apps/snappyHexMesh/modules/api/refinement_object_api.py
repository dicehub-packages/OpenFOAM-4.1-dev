from .api import Api
from modules.refinement_items import RefinementObject
from .region_refinement_api import RegionRefinementApi

class RefinementObjectApi(RegionRefinementApi):

    def __init__(self, name, app, **kwargs):
        super().__init__(**kwargs)
        self.__app = app
        self.__name = name
        instance = self._instance

    @property
    def _app(self):
        return self.__app

    @property
    def _instance(self):
        for i in self.__app.refinement.model.elements_of(RefinementObject):
            if i.name == self.__name:
                return i
        raise Exception('geometry not found')

    @property
    def visible(self):
        return self._instance.visible

    @visible.setter
    def visible(self, value):
        self._instance.visible = value