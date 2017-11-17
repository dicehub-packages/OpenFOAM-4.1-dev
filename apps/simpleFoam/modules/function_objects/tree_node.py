from dice_tools.helpers.xmodel import modelRole, modelMethod, ModelItem
from dice_tools import wizard
from dice_vtk.geometries import *


class TreeNode(ModelItem):

    def __init__(self, name, node_type, **kwargs):
        super().__init__(**kwargs)
        self.__name = name
        self.__node_type = node_type
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
        return '{0} ({1})'.format(self.name, self.count)

    @modelRole('count')
    def count(self):
        return len(self.elements)

    @modelRole('type')
    def type(self):
        return "TreeNode"

    @modelRole('nodeType')
    def node_type(self):
        return self.__node_type