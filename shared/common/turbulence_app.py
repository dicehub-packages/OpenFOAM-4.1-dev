import os

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile, ParsedBoundaryDict
from PyFoam.Basics.DataStructures import Field, Vector

from dice_tools import *
from dice_tools.helpers.xmodel import *


class TurbulenceApp(DICEObject):
    def __init__(self, app, **kwargs):
        super().__init__(base_type='QObject', **kwargs)
        self.__app = app
        self.__boundary = None

        self.register_turbulence_files()

    @property
    def app(self):
        return self.__app

    @property
    def path(self):
        return "foam:constant/turbulenceProperties"

    model_changed = diceSignal(name='modelChanged')

    @diceProperty('QString', name='model', notify=model_changed)
    def model(self):
        if self.app[self.path + " simulationType"] == "laminar":
            return "laminar"
        elif self.app[self.path + " simulationType"] == "RAS":
            return self.app[self.path + " RAS RASModel"]

    @model.setter
    def model(self, value):
        if self.model != value:
            if value == "laminar":
                self.app[self.path + " simulationType"] = "laminar"
                self.app[self.path + " RAS"] = {}
            elif value == "kOmegaSST":
                self.app[self.path + " simulationType"] = "RAS"
                self.app[self.path + " RAS"] = {
                    'RASModel': 'kOmegaSST',
                    'kOmegaSSTCoeffs': {
                        'F3': False,
                        'a1': 0.31,
                        'alphaK1': 0.85,
                        'alphaK2': 1.0,
                        'alphaOmega1': 0.5,
                        'alphaOmega2': 0.856,
                        'b1': 1.0,
                        'beta1': 0.075,
                        'beta2': 0.0828,
                        'betaStar': 0.09,
                        'c1': 10.0,
                        'gamma1': 0.5532,
                        'gamma2': 0.4403
                    },
                    'printCoeffs': True,
                    'turbulence': True
                }
            elif value == "kEpsilon":
                self.app[self.path + " simulationType"] = "RAS"
                self.app[self.path + " RAS"] = {
                    'RASModel': 'kEpsilon',
                    'kEpsilonCoeffs': {
                        "Cmu": 0.09,
                        "C1": 1.44,
                        "C2": 1.92,
                        "C3": -0.33,
                        "sigmak": 1,
                        "sigmaEps": 1.3
                    },
                    'printCoeffs': True,
                    'turbulence': True
                }
            self.model_changed()
            wizard.w_turbulence_model_changed()
            self.register_turbulence_files()

    @property
    def turbulence_fields(self):
        if self.model == 'kOmegaSST':
            return 'k', 'omega', 'nut'
        elif self.model == 'kEpsilon':
            return 'k', 'epsilon', 'nut'
        elif self.model == 'laminar':
            return None

    def register_turbulence_files(self):
        print(">>>> loading files ...", self.model)

        # Fall back to default main fields
        for f in os.scandir(self.app.config_path('0')):
            if f.is_file() and f.name not in self.app.main_fields:
                os.unlink(f.path)
                self.app.foam_file('0/' + f.name, None)

        # Copy and update boundaries for turbulence template files
        if self.model != 'laminar':
            [print(t) for t in self.turbulence_fields]

            for field_name in self.turbulence_fields:
                if os.path.exists(self.app.config_path('0/turbulence_templates/' + field_name)):
                    self.app.copy(self.app.config_path('0/turbulence_templates/' + field_name),
                                  self.app.config_path('0/'))
                    f_dict = ParsedParameterFile(self.app.config_path('0/' + field_name))
                    self.app.foam_file('0/' + field_name, f_dict)
                else:
                    notify("Template for turbulent field {0} not "
                           "found !".format(field_name), type="ERROR")
            self.update_boundaries()

    def update_boundaries(self):
        if os.path.exists(self.app.config_path('constant', 'polyMesh', 'boundary')):
            # default_boundary_props = {
            #     'foam:0/k boundaryField': {
            #         "type": "turbulentIntensityKineticEnergyInlet",
            #         "value": Field(1.0),
            #         "intensity": 0.05
            #     },
            #     'foam:0/nut boundaryField': {
            #         "type": "calculated",
            #         "value": Field(1.0)
            #     },
            #     'foam:0/omega boundaryField': {
            #         "type": "turbulentMixingLengthFrequencyInlet",
            #         "value": Field(1.0),
            #         "mixingLength": 0.001
            #     },
            #     'foam:0/epsilon boundaryField': {
            #         "type": "turbulentMixingLengthDissipationRateInlet",
            #         "value": Field(1.0),
            #         "mixingLength": 0.001
            #     }
            # }
            default_boundary_props = {
                'k': {
                    "type": "fixedValue",
                    "value": Field(1.0)
                },
                'nut': {
                    "type": "calculated",
                    "value": Field(1.0)
                },
                'omega': {
                    "type": "fixedValue",
                    "value": Field(1.0)
                },
                'epsilon': {
                    "type": "fixedValue",
                    "value": Field(1.0)
                }
            }

            self.__boundary = ParsedBoundaryDict(self.app.config_path(
                'constant', 'polyMesh', 'boundary'))
            self.app.foam_file('constant/polyMesh/boundary', self.__boundary)
            boundary_names = set(self.app['foam:constant/polyMesh/boundary'])

            for field_name, prop in default_boundary_props.items():
                path = 'foam:0/{0} boundaryField'.format(field_name)
                if self.app[path] is not None:
                    for v in list(self.app[path]):
                        if v not in boundary_names:
                            self.app[path + ' ' + v] = None

                    for v in boundary_names:
                        if v not in self.app[path]:
                            self.app[path + ' ' + v] = self.__get_smart_boundary_props(prop, field_name, boundary_name=v)

    @staticmethod
    def __get_smart_boundary_props(prop, field_name, boundary_name):
        if 'inlet' in boundary_name:
            if field_name == 'k':
                return {
                    "type": "turbulentIntensityKineticEnergyInlet",
                    "value": Field(1.0),
                    "intensity": 0.05
                }
            elif field_name == 'nut':
                return {
                    "type": "calculated",
                    "value": Field(1.0)
                }
            elif field_name == 'omega':
                return {
                    "type": "turbulentMixingLengthFrequencyInlet",
                    "value": Field(1.0),
                    "mixingLength": 0.001
                }
            elif field_name == 'epsilon':
                return {
                    "type": "turbulentMixingLengthDissipationRateInlet",
                    "value": Field(1.0),
                    "mixingLength": 0.001
                }
        elif 'symmetry' in boundary_name:
            return {
                "type": "symmetry"
            }
        elif 'wall' in boundary_name:
            if field_name == 'k':
                return {
                    "type": "kqRWallFunction",
                    "value": Field(1.0)
                }
            elif field_name == 'omega':
                return {
                    "type": "omegaWallFunction",
                    "value": Field(1.0)
                }
        else:
            return prop
