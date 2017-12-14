from dice_tools import *
from dice_tools.helpers.xmodel import *

from PyFoam.Basics.DataStructures import TupleProxy


class DivScheme:

    def __init__(self, app, name):
        super().__init__()
        self.app = app
        self.__name = name

        self.__expert_view_visible = False

        self.__centred_schemes = [
            "linear",
            "cubic",
            "midPoint"
        ]

        self.__upwinded_convection_schemes = [
            "upwind",
            "linearUpwind",
            # "filteredLinear2",
            "filteredLinear3",
            "cubicUpwindFit",
            "linearPureUpwindFit",
            "quadraticLinearUpwindFit",
            "quadraticUpwindFit",
            "LUST"
        ]

        # Total Variation Diminishing (TVD)
        self.__tvd_schemes = [
            "limitedLinear",
            "vanLeer",
            "MUSCL",
            "limitedCubic",
            "Minmod",
            "SuperBee",
            "UMIST"
        ]

        # Normalised Variable Diminishing (NVD)
        self.__nvd_schemes = [
            "SFCD",
            "Gamma"
        ]

        # Improved limitedSchemes for vector fields
        self.__v_allowed_schemes = [
            {"limitedLinear": "limitedLinearV"},
            {"vanLeer": "vanLeerV"},
            {"Gamma": "GammaV"},
            {"limitedCubic": "limitedCubicV"},
            {"SFCD": "SFCDV"},
            {"SuperBee": "SuperBeeV"},
            {"UMIST": "UMISTV"},
            {"MUSCL": "MUSCLV"},
            {"Minmod": "MinmodV"},
            {"filteredLinear3": "filteredLinear3V"}
        ]

        self.__all_schemes = self.__centred_schemes \
                      + self.__upwinded_convection_schemes \
                      + self.__tvd_schemes \
                      + self.__nvd_schemes

        self.__schemes_with_coeff = [
            "limitedLinear", "limitedLinearV",
            "filteredLinear3", "filteredLinear3V",
            "cubicUpwindFit",
            "linearPureUpwindFit",
            "quadraticLinearUpwindFit",
            "quadraticUpwindFit",
            "Gamma",
            "limitedCubic"
        ]

        self.__most_used_schemes = [
            "linear",
            "upwind",
            "linearUpwind",
            "limitedLinear",
            "vanLeer",
            "Minmod",
            "SFCD"
        ]

    @property
    def path(self):
        return 'foam:system/fvSchemes divSchemes ' + self.name

    @modelRole('name')
    def name(self):
        return self.__name

    @modelRole('alias')
    def alias(self):
        if self.name == "default":
            return "default"
        elif self.name == "div(phi,U)":
            return "Velocity"
        elif self.name == "div(phi,k)":
            return "k"
        elif self.name == "div(phi,omega)":
            return "Omega"
        elif self.name == "div(phi,epsilon)":
            return "Epsilon"
        else:
            return self.name

    @modelRole('fieldName')
    def field_name(self):
        if self.name == "default":
            return "default"
        elif self.name == "div(phi,U)":
            return "U"
        elif self.name == "div(phi,k)":
            return "k"
        elif self.name == "div(phi,omega)":
            return "omega"
        elif self.name == "div(phi,epsilon)":
            return "epsilon"
        else:
            return self.name.replace("div(phi,","").replace(")","")

    @modelRole('schemeValue')
    def scheme_value(self):
        return self.app[self.path]

    @scheme_value.setter
    def scheme_value(self, value):
        self.app[self.path] = value

    @modelRole('isBounded')
    def is_bounded(self):
        if self.scheme_value is not None:
            return "bounded" in self.scheme_value \
                    and self.scheme_value.index("bounded") == 0
        else:
            return False

    @is_bounded.setter
    def is_bounded(self, value):
        if self.scheme_value is not None:
            if value and "bounded" not in self.scheme_value:
                self.scheme_value.insert(0, "bounded")
            elif "bounded" in self.scheme_value:
                self.scheme_value.remove("bounded")
            self.app[self.path] = self.scheme_value

    @property
    def bounded(self):
        if "bounded" in self.scheme_value \
            and self.scheme_value.index("bounded") == 0:

            return "bounded"
        else:
            return ""

    @modelRole('useDefaultScheme')
    def use_default_scheme(self):
        return self.name not in self.app["foam:system/fvSchemes divSchemes"]

    @use_default_scheme.setter
    def use_default_scheme(self, value):
        if value and self.name in self.app["foam:system/fvSchemes divSchemes"]:
            self.scheme_value = None
        elif self.name not in self.app["foam:system/fvSchemes divSchemes"]:
            div_schemes = self.app["foam:system/fvSchemes divSchemes"]
            div_schemes[self.name] = TupleProxy(["bounded", "Gauss", "linear"])
            self.app["foam:system/fvSchemes divSchemes"] = div_schemes

    @modelRole('expertViewVisible')
    def expert_view_visible(self):
        return self.__expert_view_visible

    @expert_view_visible.setter
    def expert_view_visible(self, value):
        if self.__expert_view_visible != value:
            self.__expert_view_visible = value

    @modelRole('interpolationSchemesModel')
    def interpolation_schemes_model(self):
        model = []

        if self.__expert_view_visible:
            for scheme in self.__centred_schemes:
                model.append({"sectionName": "Centred Schemes", "name": scheme, "isVisible": True})
            for scheme in self.__upwinded_convection_schemes:
                model.append({"sectionName": "Upwinded Convection", "name": scheme, "isVisible": True})
            for scheme in self.__tvd_schemes:
                model.append({"sectionName": "TVD", "name": scheme, "isVisible": True})
            for scheme in self.__nvd_schemes:
                model.append({"sectionName": "NVD", "name": scheme, "isVisible": True})
        else:
            for scheme in self.__centred_schemes:
                if scheme in self.__most_used_schemes or scheme == self.interpolation_scheme.replace("V",""):
                    model.append({"sectionName": "Centred Schemes", "name": scheme, "isVisible": True})
                else:
                    model.append({"sectionName": "Centred Schemes", "name": scheme, "isVisible": False})
            for scheme in self.__upwinded_convection_schemes:
                if scheme in self.__most_used_schemes or scheme == self.interpolation_scheme.replace("V",""):
                    model.append({"sectionName": "Upwinded Convection", "name": scheme, "isVisible": True})
                else:
                    model.append({"sectionName": "Upwinded Convection", "name": scheme, "isVisible": False})
            for scheme in self.__tvd_schemes:
                if scheme in self.__most_used_schemes or scheme == self.interpolation_scheme.replace("V",""):
                    model.append({"sectionName": "TVD", "name": scheme, "isVisible": True})
                else:
                    model.append({"sectionName": "TVD", "name": scheme, "isVisible": False})
            for scheme in self.__nvd_schemes:
                if scheme in self.__most_used_schemes or scheme == self.interpolation_scheme.replace("V",""):
                    model.append({"sectionName": "NVD", "name": scheme, "isVisible": True})
                else:
                    model.append({"sectionName": "NVD", "name": scheme, "isVisible": False})

        return model

    @modelRole('currentInterpolationSchemeListIndex')
    def current_interpolation_scheme_list_index(self):
        if self.scheme_value is not None:
            if self.improved:
                return self.__all_schemes.index(self.interpolation_scheme[:-1])
            else:
                return self.__all_schemes.index(self.interpolation_scheme)
        else:
            return -1

    @current_interpolation_scheme_list_index.setter
    def current_interpolation_scheme_list_index(self, value):
        self.interpolation_scheme = self.__all_schemes[value]

    @modelRole('interpolationScheme')
    def interpolation_scheme(self):
        if self.scheme_value is not None:
            for i_scheme in self.__all_schemes:
                if i_scheme in self.scheme_value:
                    return i_scheme
                elif i_scheme + "V" in self.scheme_value:
                    return i_scheme+"V"
        return ""

    @interpolation_scheme.setter
    def interpolation_scheme(self, value):
        if self.scheme_value is not None:
            if value == "linear":
                new_value = TupleProxy([self.bounded, "Gauss", value])
            elif value in self.__schemes_with_coeff:
                new_value = TupleProxy((self.bounded, "Gauss", value, 1.0))
            elif value in ("linearUpwind", "LUST"):
                new_value = TupleProxy((self.bounded, "Gauss",
                                        value, "grad({0})".format(self.field_name)))
            else:
                new_value = TupleProxy([self.bounded, "Gauss", value])
            self.app[self.path] = new_value

    @modelRole("hasCoeff")
    def has_coeff(self):
        if self.scheme_value is not None:
            return self.interpolation_scheme in self.__schemes_with_coeff
        return False

    @modelRole("coeff")
    def coeff(self):
        if self.scheme_value is not None:
            if self.interpolation_scheme in self.__schemes_with_coeff:
                index = self.scheme_value.index(self.interpolation_scheme)
                return self.scheme_value[index + 1]

    @coeff.setter
    def coeff(self, value):
        if self.scheme_value is not None:
            if self.interpolation_scheme in self.__schemes_with_coeff:
                index = self.scheme_value.index(self.interpolation_scheme)
                if value == "":
                    self.scheme_value[index + 1] = 0.0
                else:
                    self.scheme_value[index + 1] = value
                self.app[self.path] = self.scheme_value

    @modelRole('improvementAllowed')
    def improvement_allowed(self):
        unimproved_schemes = set().union(*(d.keys() for d in self.__v_allowed_schemes))
        improved_schemes = set().union(*(d.values() for d in self.__v_allowed_schemes))

        return self.interpolation_scheme in unimproved_schemes | improved_schemes

    @modelRole('improved')
    def improved(self):
        unimproved_schemes = set().union(*(d.keys() for d in self.__v_allowed_schemes))
        improved_schemes = set().union(*(d.values() for d in self.__v_allowed_schemes))

        return self.interpolation_scheme in improved_schemes

    @improved.setter
    def improved(self, value):
        unimproved_schemes = set().union(*(d.keys() for d in self.__v_allowed_schemes))
        improved_schemes = set().union(*(d.values() for d in self.__v_allowed_schemes))

        if self.scheme_value is not None:
            new_value = TupleProxy([])
            if self.interpolation_scheme in unimproved_schemes and value:
                for v in self.scheme_value:
                    if isinstance(v, str):
                        new_value.append(
                            v.replace(self.interpolation_scheme,
                                      self.interpolation_scheme+"V")
                        )
                    else:
                        new_value.append(v)
            elif self.interpolation_scheme in improved_schemes and not value:
                for v in self.scheme_value:
                    if isinstance(v, str):
                        new_value.append(
                            v.replace(self.interpolation_scheme,
                                      self.interpolation_scheme[:-1])
                        )
                    else:
                        new_value.append(v)
            self.app[self.path] = new_value


class DivSchemesApp:

    def __init__(self):
        super().__init__()
        self.__div_schemes_model = standard_model(DivScheme)

        wizard.subscribe("w_turbulence_model_changed", self.load_schemes)

    @property
    def path(self):
        return "foam:system/fvSchemes divSchemes"

    @diceProperty('QVariant', name='divSchemesModel')
    def div_schemes_model(self):
        return self.__div_schemes_model

    def __schemes(self):
        main_schemes = ["default", "div(phi,U)"]
        k_epsilon_schemes = main_schemes + ["div(phi,k)", "div(phi,epsilon)"]
        k_omega_schemes = main_schemes + ["div(phi,k)", "div(phi,omega)"]

        if self.turbulence.model == "laminar":
            schemes = main_schemes
        elif self.turbulence.model == "kEpsilon":
            schemes = k_epsilon_schemes
        elif self.turbulence.model == "kOmegaSST":
            schemes = k_omega_schemes

        return schemes

    def load_schemes(self):
        self.__div_schemes_model.root_elements.clear()

        for scheme_name in self.__schemes():
            self.__div_schemes_model.root_elements.append(DivScheme(self, scheme_name))