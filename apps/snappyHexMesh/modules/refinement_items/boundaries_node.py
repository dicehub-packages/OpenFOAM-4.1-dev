from .tree_node import TreeNode
from dice_tools.helpers.xmodel import modelRole, modelMethod, ModelItem
from dice_tools import wizard

class BoundariesNode(TreeNode):

    def __init__(self, name, app, **kwargs):
        super().__init__(name = name, **kwargs)
        self.app = app

    @modelMethod('showInScene')
    def show_in_scene(self):
        wizard.w_reset_camera_to_object([self.app.bounding_box.vis_obj])

    @modelRole('isVisible')
    def visible(self):
        return self.app.bounding_box.vis_obj.visible
    
    @visible.setter
    def visible(self, value):
        self.app.bounding_box.vis_obj.visible = value