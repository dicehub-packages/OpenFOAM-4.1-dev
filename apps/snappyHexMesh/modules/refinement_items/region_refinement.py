from dice_tools import wizard
from dice_tools.helpers.xmodel import modelRole, modelMethod, ModelItem
from .region_level import RegionLevel


class RegionRefinement(ModelItem):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def region_path(self):
        return 'foam:system/snappyHexMeshDict castellatedMeshControls refinementRegions '+self.name

    @property
    def mode_path(self):
        return self.region_path + ' mode'

    @property
    def levels_path(self):
        return self.region_path + ' levels'

    def setup_region(self, modes, default_mode):
        self.modes = modes
        if self.app[self.region_path] is not None:
            self.current_mode = self.app[self.mode_path]
        else:
            self.current_mode = default_mode

    @property
    def region_mode(self):
        return self.current_mode

    @region_mode.setter
    def region_mode(self, value):
        self.current_mode = value
        if self.app[self.region_path] is not None:
            self.app[self.mode_path] = value
        for v in self.elements:
            wizard.w_model_update_item(v)
        wizard.w_model_update_item(self)

    @property
    def levels_count(self):
        if self.app[self.region_path] is not None:
            return len(self.app[self.levels_path])
        return 0

    @property
    def can_add_level(self):
        return self.levels_count == 0 or self.region_mode == "distance"

    def add_region_level(self):
        if not self.can_add_level:
            return False
        # print('--->', self.app[self.region_path])
        if self.app[self.region_path] is None:
            level_data = [0, 0]
            self.app[self.region_path] = {
                "mode": self.region_mode,
                "levels": [level_data]
            }
        else:
            levels = self.app[self.levels_path]
            levels.append([0, 0])
            self.app[self.levels_path] = levels
        return True

    def clear_region_levels(self):
        for v in self.elements[:]:
            self.remove_region_level(v)

    def get_level_data(self, index):
        if self.app[self.region_path] is not None:
            if index < len(self.app[self.levels_path]):
                return self.app[self.levels_path][index]

    def set_level_data(self, index, value):
        self.app[self.levels_path + ' %i'%index] = value

    def remove_region_level(self, index):
        self.app[self.levels_path + ' %i'%index] = None
        # print(self.app[self.levels_path])
        if not self.app[self.levels_path]:
            self.app[self.region_path] = None

