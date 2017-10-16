from dice_tools import *
import os
import sys
import traceback

class PythonScript(Application):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__input_data = {}
        self.__internal_input_data = {}

        if os.path.exists(self.config_path('script.py')):
            with open(self.config_path('script.py')) as f:
                self.__script = f.read()
        else:
            with open('template.py') as f:
                self.__script = f.read()

    def input_changed(self, input_data):
        self.__input_data = input_data

    def internal_input_changed(self, input_data):
        self.__internal_input_data = input_data

    def behaviour_changed(self, behaviour):
        self.__behaviour = behaviour
        self.behaviour_changed_signal()

    def input_types_changed(self, input_types):
        self.__inputs = input_types
        self.input_type_changed()

    def internal_input_types_changed(self, input_types):
        self.__internal_inputs = input_types
        self.internal_input_type_changed()

    def output_types_changed(self, output_types):
        self.__outputs = output_types
        self.output_type_changed()

    def internal_output_types_changed(self, output_types):
        self.__internal_outputs = output_types
        self.internal_output_type_changed()

    saveRequest = diceSignal()

    @diceProperty('QString')
    def script(self):
        return self.__script

    @script.setter
    def script(self, value):
        self.__script = value

    input_type_changed = diceSignal()

    @diceProperty('QString', name='inputType', notify=input_type_changed)
    def input_type(self):
        for v in self.__inputs:
            return v
        return ''

    @input_type.setter
    def input_type(self, value):
        if value:
            self.__inputs = {value: 1}
        else:
            self.__inputs = {}
        self.input_type_changed()

    output_type_changed = diceSignal()

    @diceProperty('QString', name='outputType', notify=output_type_changed)
    def output_type(self):
        for v in self.__outputs:
            return v
        return ''

    @output_type.setter
    def output_type(self, value):
        if value:
            self.__outputs = [value]
        else:
            self.__outputs = []
        self.output_type_changed()

    internal_input_type_changed = diceSignal()

    @diceProperty('QString', name='internalInputType', notify=internal_input_type_changed)
    def internal_input_type(self):
        for v in self.__internal_inputs:
            return v
        return ''

    @internal_input_type.setter
    def internal_input_type(self, value):
        if value:
            self.__internal_inputs = {value: 1}
        else:
            self.__internal_inputs = {}
        self.internal_input_type_changed()

    internal_output_type_changed = diceSignal()

    @diceProperty('QString', name='internalOutputType', notify=internal_output_type_changed)
    def internal_output_type(self):
        for v in self.__internal_outputs:
            return v
        return ''

    @internal_output_type.setter
    def internal_output_type(self, value):
        if value:
            self.__internal_outputs = [value]
        else:
            self.__internal_outputs = []
        self.internal_output_type_changed()

    behaviour_changed_signal = diceSignal()

    @diceProperty('QString', name='behaviour', notify=behaviour_changed_signal)
    def behaviour(self):
        return self.__behaviour

    @behaviour.setter
    def behaviour(self, value):
        self.__behaviour = value
        self.behaviour_changed_signal()

    @diceSlot('QString')
    def save(self, script):
        self.set_input_types(self.__inputs)
        self.set_output_types(self.__outputs)
        self.set_behaviour(self.__behaviour)
        self.set_internal_input_types(self.__internal_inputs)
        self.set_internal_output_types(self.__internal_outputs)
        self.__script = script
        with open(self.config_path('script.py'), 'w') as f:
            f.write(self.__script)
        self.set_progress(0)

    @diceTask("Run Script")
    def run_script(self):
        env = {'app_input': None, 'app': self}
        for v in self.__input_data.values():
            env['app_input'] = v
            break
        try:
            try:
                exec(self.__script, env)
            except NameError as e:
                tb = sys.exc_info()[2]
                if tb.tb_next and tb.tb_next.tb_next is None:
                    self.log("Error: %s\n"%e.args[0])
                else:
                    raise
        except:
            exc = traceback.format_exc(chain=False).split('\n')
            self.log("Error:\n%s\n"%'\n'.join(exc[:1]+exc[3:]))
        if self.output_type and 'app_output' in env:
            self.set_output(self.output_type, env['app_output'])
        return True
