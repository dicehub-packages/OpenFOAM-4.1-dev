from dice_tools import wizard
from dice_tools.helpers.xmodel import modelRole, modelMethod


class Boundary:
    """
    Boundary for the blockMeshDict file.
    """

    def __init__(self, app, face, index):
        self.app = app
        self.face = face
        self.index = 2*index

    @property
    def __name_path(self):
        return 'foam:system/blockMeshDict boundary %i'%self.index

    @property
    def __type_path(self):
        return 'foam:system/blockMeshDict boundary %i type'%(self.index+1)

    @property
    def name(self):
        return self.app[self.__name_path]

    @name.setter
    def name(self, value):
        self.app[self.__name_path] = value
        wizard.w_model_update_item(self)

    @property
    def type(self):
        return self.app[self.__type_path]

    @type.setter
    def type(self, value):
        self.app[self.__type_path] = value
        wizard.w_model_update_item(self)

    @modelRole('label')
    def label(self):
        return self.name

    @modelMethod('showInScene')
    def show_in_scene(self):
        wizard.w_reset_camera_to_object([self.app.bounding_box.vis_obj])
