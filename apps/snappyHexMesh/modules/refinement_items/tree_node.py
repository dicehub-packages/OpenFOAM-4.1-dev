from dice_tools.helpers.xmodel import modelRole, modelMethod, ModelItem
from dice_tools import wizard
from dice_vtk.geometries import *


class TreeNode(ModelItem):

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.__name = name
        self.__is_expanded = True
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
        return '%s (%i)'%(self.name, self.count)

    @modelRole('count')
    def count(self):
        return len(self.elements)

    @modelRole('isVisible')
    def visible(self):
        for v in self.elements:
            if v.visible:
                return True
        return False
    
    @visible.setter
    def visible(self, value):
        for v in self.elements:
            v.visible = value

    @modelMethod('showInScene')
    def show_in_scene(self):
        pass