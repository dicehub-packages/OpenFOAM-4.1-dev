from .function_object import FunctionObject


class ForcesMonitor(FunctionObject):

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)

    @property
    def patches(self):
        return self.app[self.path + ' patches']

    @patches.setter
    def patches(self, value):
        self.app[self.path + ' patches'] = value

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
