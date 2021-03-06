from dice_tools import *
from dice_tools.helpers.xmodel import *


class FunctionObject:

    def __init__(self, name, app, **kwargs):
        self.__name = name
        self.__app = app

        wizard.w_function_object_created(self)

    @property
    def path(self):
        return 'foam:system/functionObjects ' + self.name

    @property
    def app(self):
        return self.__app

    @modelRole('name')
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if self.name != value:
            v = self.app[self.path]
            self.app[self.path] = None
            wizard.w_function_object_changed(self, old_name=self.__name,
                                             new_name=value)
            self.__name = value
            self.app[self.path] = v

    @modelRole('label')
    def label(self):
        return self.name

    @modelRole('type')
    def type(self):
        return self.app[self.path + ' type']

    @modelMethod('remove')
    def remove_function_object(self):
        type = self.type
        self.app[self.path] = None
        wizard.w_function_object_removed(self, type)
