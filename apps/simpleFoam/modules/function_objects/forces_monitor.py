from .function_object import FunctionObject
from dice_tools import *
from dice_tools.helpers.xmodel import *


class Patch:

    def __init__(self, name):
        super().__init__()
        self.__name = name

    @modelRole('name')
    def name(self):
        return self.__name


class ForcesMonitor(FunctionObject):

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)

        self.__patches_model = standard_model(Patch)
        self.load_patches_model()

        wizard.subscribe('w_model_selection_changed',
                         self.__w_boundary_selected,
                         model=self.app.boundaries_model)
        wizard.subscribe('w_model_selection_changed',
                         self.__w_monitored_patch_selected,
                         model=self.patches_model)
        wizard.subscribe("input_changed", self.__w_input_changed)

    # Monitored patches
    # =================

    @diceProperty('QVariant', name='patchesModel')
    def patches_model(self):
        return self.__patches_model

    @property
    def patches(self):
        return self.app[self.path + ' patches']

    @patches.setter
    def patches(self, value):
        self.app[self.path + ' patches'] = value
        self.load_patches_model()

    # Adding monitored patches
    # ========================

    def __w_input_changed(self):
        self.__clean_non_existing_patches()

    def __w_boundary_selected(self, model, selected, deselected):
        signal("functionObjects:*")

    def load_patches_model(self):
        self.patches_model.root_elements.clear()
        for patch in self.patches:
            self.__patches_model.root_elements.append(Patch(patch))

    def __clean_non_existing_patches(self):
        patches = self.patches
        boundary_names = [boundary.name for boundary in
                          self.app.boundaries_model]
        for patch in self.patches:
            if patch not in boundary_names and len(boundary_names) is not 0:
                patches.remove(patch)
                self.patches = patches

    def add_patches(self):
        patches = self.patches
        for s in self.app.function_objects.model.selection:
            for b in self.app.boundaries_model.selection:
                if b.name not in patches:
                    patches.append(b.name)
            self.patches = patches

    @property
    def can_add_patches(self):
        return len(self.app.boundaries_model.selection) > 0

    @property
    def can_open_select_patches_dialog(self):
        """
        Only show the select monitored patches dialog if only one monitor
        is selected. Multiple selection causes a conflict when adding patches
        in different function objects.
        """
        return len(self.app.function_objects.model.selection) == 1

    # Removing monitored patches
    # ==========================

    def __w_monitored_patch_selected(self, model, selected, deselected):
        signal("functionObjects:*")

    def remove_patches(self):
        patches = self.patches
        for s in self.app.function_objects.model.selection:
            for p in self.patches_model.selection:
                if p.name in patches:
                    patches.remove(p.name)
            self.patches = patches

    @property
    def can_remove_patches(self):
        return len(self.patches_model.selection) > 0

    # Properties
    # ==========

    @property
    def p_ref(self):
        return self.app[self.path + ' pRef']

    @p_ref.setter
    def p_ref(self, value):
        self.app[self.path + ' pRef'] = value

    @property
    def rho_inf(self):
        return self.app[self.path + ' rhoInf']

    @rho_inf.setter
    def rho_inf(self, value):
        self.app[self.path + ' rhoInf'] = value

    @property
    def porosity(self):
        return self.app[self.path + ' porosity']

    @porosity.setter
    def porosity(self, value):
        self.app[self.path + ' porosity'] = value

    @property
    def write_fields(self):
        return self.app[self.path + ' writeFields']

    @write_fields.setter
    def write_fields(self, value):
        self.app[self.path + ' writeFields'] = value

    @property
    def cofr(self):
        """
        Centre of rotation for moment calculations
        :return: centre of rotation vector (x y z)
        """
        return self.app[self.path + ' CofR']

    @cofr.setter
    def cofr(self, value):
        self.app[self.path + ' CofR'] = value

    @property
    def pitch_axis(self):
        """
        Pitch axis
        """
        return self.app[self.path + ' pitchAxis']

    @pitch_axis.setter
    def pitch_axis(self, value):
        self.app[self.path + ' pitchAxis'] = value

