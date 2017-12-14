import os

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

from dice_tools import *
from dice_tools.helpers.xmodel import *
from .cell_zone_objects import *


class CellZonesApp:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__cell_zones_model = standard_model(CellZone)
        self.__mrf_zones_model = standard_model(MRFZone)
        self.__non_rotating_patches_model = standard_model(NonRotatingPatch)

        wizard.subscribe(self, self.__cell_zones_model)
        wizard.subscribe("w_model_selection_changed",
                         self.__w_model_selection_changed,
                         model=self.cell_zones_model)
        wizard.subscribe("w_model_selection_changed",
                         self.__w_non_rotating_patches_model_selection_changed,
                         model=self.non_rotating_patches_model)

    @property
    def path(self):
        return "foam:constant/polyMesh/cellZones"

    @diceProperty('QVariant', name='cellZonesModel')
    def cell_zones_model(self):
        return self.__cell_zones_model

    def load_cell_zone_model(self):
        self.__cell_zones_model.root_elements.clear()

        cell_zone_file_path = self.config_path("constant",
                                               "polyMesh", "cellZones")

        if os.path.exists(cell_zone_file_path):
            cell_zone_file = ParsedParameterFile(
                cell_zone_file_path, listDictWithHeader=True)
            if len(cell_zone_file) > 1:
                for name in cell_zone_file[1]:
                    if isinstance(name, str):
                        self.__cell_zones_model.root_elements.append(CellZone(self, name))

    cell_zone_selection_changed = diceSignal(name='cellZoneSelectionChanged')

    @diceProperty('QVariant', name='hasMrfProps', notify=cell_zone_selection_changed)
    def has_mrf_props(self):
        return bool([v for v in self.cell_zones_model.selection if isinstance(v, CellZone)])

    def __w_model_selection_changed(self, model, selected, deselected):
        self.cell_zone_selection_changed()
        signal('mrf:*')

    @diceProperty('QVariant', name='mrfIsEnabled', notify=cell_zone_selection_changed)
    def mrf_is_enabled(self):
        mrf_names = [mrf.name for mrf in self.__mrf_zones_model]
        cell_zone_names = [cellzone.name for cellzone in
                           self.__cell_zones_model.selection]
        if len(cell_zone_names) == len(mrf_names) \
                and set(cell_zone_names) == set(mrf_names):
            return True
        elif len(self.__cell_zones_model.selection) != 1:
            return False
        for v in self.__cell_zones_model.selection:
            for vv in self.mrf_zones_model.elements_of(MRFZone):
                if v.name == vv.name:
                    return True
        return False

    @mrf_is_enabled.setter
    def mrf_is_enabled(self, value):
        mrf_names = [mrf.name for mrf in self.__mrf_zones_model]
        cell_zone_names = [cellzone.name for cellzone in
                           self.__cell_zones_model.selection]

        for name in cell_zone_names:
            if name not in mrf_names and value:
                self["foam:constant/MRFProperties " + name] = {
                    'cellZone': name,
                    'active': True,
                    'nonRotatingPatches': [],
                    'origin': [0,0,0],
                    'axis': [0,0,1],
                    'omega': 1
                }
            elif name in mrf_names and not value:
                self["foam:constant/MRFProperties " + name] = None
        self.load_mrf_zones()
        signal('mrf:*')

    @diceSync('mrf:')
    def __mrf_sync(self, path):
        cell_zone_names = [cellzone.name for cellzone in
                           self.__cell_zones_model.selection]

        result = None
        for name in cell_zone_names:
            for mrf in self.mrf_zones_model:
                if name == mrf.name and hasattr(mrf, path):
                    value = getattr(mrf, path)
                    if value is not None:
                        if result is None:
                            result = value
                        elif result != value:
                            return None
        return result

    @__mrf_sync.setter
    def __mrf_sync(self, path , value):
        cell_zone_names = [cellzone.name for cellzone in
                           self.__cell_zones_model.selection]

        for name in cell_zone_names:
            for mrf in self.mrf_zones_model:
                if name == mrf.name and hasattr(mrf, path):
                    if getattr(mrf, path) is not None:
                        setattr(mrf, path, value)
        signal('mrf:*')

    @diceProperty('QVariant', name="mrfZonesModel")
    def mrf_zones_model(self):
        return self.__mrf_zones_model

    def load_mrf_zones(self):
        self.__mrf_zones_model.root_elements.clear()

        if len(self.mrf_props) > 0:
            for name in self.mrf_props:
                self.__mrf_zones_model.root_elements.append(
                    MRFZone(self, name)
                )
        self.__clean_non_existing_mrfs()

    def __clean_non_existing_mrfs(self):
        cell_zone_names = [cellzone.name for cellzone in
                           self.__cell_zones_model]

        for mrf in self.__mrf_zones_model:
            if mrf.name not in cell_zone_names:
                self["foam:constant/MRFProperties " + mrf.name] = None
                self.__mrf_zones_model.root_elements.remove(mrf)

    # Non Rotating Patches for MRF
    # ============================

    non_rotating_patches_selection_changed = diceSignal(name='nonRotatingPatchesSelectionChanged')

    def __w_non_rotating_patches_model_selection_changed(self, model, selected, deselected):
        self.non_rotating_patches_selection_changed()

    @diceProperty('QVariant', name="nonRotatingPatchesModel",
                  notify=cell_zone_selection_changed)
    def non_rotating_patches_model(self):
        return self.__non_rotating_patches_model

    @diceSlot(name="loadNonRotatingPatchesModel")
    def load_non_rotating_patches_model(self):
        self.__non_rotating_patches_model.root_elements.clear()

        if len(self.cell_zones_model.selection) != 1:
            return []

        for s in self.cell_zones_model.selection:
            for mrf in self.mrf_zones_model:
                if s.name == mrf.name:
                    for name in self['foam:constant/MRFProperties '
                            + mrf.name + ' nonRotatingPatches']:
                        self.__non_rotating_patches_model.root_elements.append(
                            NonRotatingPatch(self, name)
                        )

    @diceProperty('QVariant', name='singleCellZoneSelection',
                  notify=cell_zone_selection_changed)
    def single_cell_zone_selection(self):
        return len(self.__cell_zones_model.selection) == 1

    @diceProperty('QVariant', name='nonRotatingPatchSelected',
                  notify=non_rotating_patches_selection_changed)
    def __non_rotating_patch_selected(self):
        return bool([v for v in self.non_rotating_patches_model.selection if
                     isinstance(v, NonRotatingPatch)])

    @diceSlot(name="addNonRotatingPatches")
    def add_non_rotating_patches(self):
        if not self.single_cell_zone_selection:
            return
        else:
            for selected_zone in self.cell_zones_model.selection:
                mrf_name = selected_zone.name
            value = self['foam:constant/MRFProperties ' + mrf_name + ' nonRotatingPatches']
            for s in self.boundaries_model.selection:
                if s.name not in value:
                    value.append(s.name)
            self['foam:constant/MRFProperties ' + mrf_name + ' nonRotatingPatches'] = value
            self.load_non_rotating_patches_model()

    @diceSlot(name="removeNonRotatingPatches")
    def remove_non_rotating_patches(self):
        if not self.single_cell_zone_selection:
            return
        else:
            for selected_zone in self.cell_zones_model.selection:
                mrf_name = selected_zone.name
            value = self['foam:constant/MRFProperties ' + mrf_name + ' nonRotatingPatches']
            for s in self.non_rotating_patches_model.selection:
                if s.name in value:
                    value.remove(s.name)
            self['foam:constant/MRFProperties ' + mrf_name + ' nonRotatingPatches'] = value
            self.load_non_rotating_patches_model()