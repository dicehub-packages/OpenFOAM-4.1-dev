from .api import Api
from modules.refinement_items import RegionRefinement

class RegionRefinementApi(Api):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def region_mode(self):
        return self._instance.region_mode

    @region_mode.setter
    def region_mode(self, value):
        self._instance.region_mode = value

    @property
    def region_levels_count(self):
        return self._instance.levels_count

    def add_region_level(self, data):
        instance = self._instance
        index = instance.levels_count
        if not instance.add_region_level():
            raise Exception("Can't add level")
        instance.set_level_data(index, data)

    def remove_region_level(self, index):
        self._instance.remove_region_level(index)

    def clear_region_levels(self):
        self._instance.clear_region_levels()

    def update_region_level(self, index, data):
        self._instance.set_level_data(index, data)

    def get_region_level(self, index):
        self._instance.get_level_data(index)

    @region_mode.setter
    def region_mode(self, value):
        self._instance.region_mode = value

    def dump(self, path):
        super().dump(path)
        instance = self._instance
        for i in range(instance.levels_count):
            print(path+'.add_region_level([%g, %g])'%tuple(instance.get_level_data(i)), '\n')
