from PyFoam.Basics.DataStructures import Field


class Pressure:

    def __init__(self, app):
        self.app = app
        self.name = self.app.name

    @property
    def pressure_boundary_condition_type(self):
        path = 'foam:0/p boundaryField ' + self.name + ' type'
        condition_type = self.app[path]
        if condition_type == 'fixedValue':
            return 'Fixed Value'
        elif condition_type == 'totalPressure':
            return 'Total Pressure'
        elif condition_type == 'zeroGradient':
            return 'Zero Gradient'
        elif condition_type == 'slip':
            return 'Slip'
        elif condition_type == 'symmetry':
            return 'Symmetry'

    @pressure_boundary_condition_type.setter
    def pressure_boundary_condition_type(self, value):
        path = 'foam:0/p boundaryField ' + self.name
        default_pressure_value = 0
        if value == 'Fixed Value':
            self.app[path] = {
                'type': 'fixedValue',
                'value': Field(default_pressure_value)
            }
        elif value == 'Total Pressure':
            self.app[path] = {
                'type': 'totalPressure',
                'p0': Field(default_pressure_value),
                'U': 'U',
                'phi': 'phi',
                'rho': 'none',
                'psi': 'none',
                'gamma': 1,
                'value': Field(default_pressure_value)
            }
        elif value == 'Zero Gradient':
            self.app[path] = {
                'type': 'zeroGradient'
            }
        elif value == 'Slip':
            self.app[path] = {
                'type': 'slip'
            }
        elif value == 'Symmetry':
            self.app[path] = {
                'type': 'symmetry'
            }

    @property
    def pressure_field_value(self):
        path = 'foam:0/p boundaryField ' + self.name + ' value'
        return self.app[path]

    @pressure_field_value.setter
    def pressure_field_value(self, value):
        path = 'foam:0/p boundaryField ' + self.name + ' value'
        if self.app[path] is not None:
            self.app[path] = Field(value)