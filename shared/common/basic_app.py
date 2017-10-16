from dice_tools.helpers import FileOperations, JsonOrderedDict
import os
from dice_tools import notify, diceSync, wizard, signal

class BasicApp(FileOperations):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__read_config()
        self.__copy_template_folder()
        self.__config_modified = False
        wizard.subscribe('w_idle', self.__w_idle)

    def __w_idle(self):
        if self.__config_modified:
            self.config.write()
            self.__config_modified = False

    @diceSync('config:')
    def __config_sync(self, path):
        return self.config[path]

    @__config_sync.setter
    def __config_sync(self, path, value):
        self.config[path]=value
        self.__config_modified = True
        signal('config:*')
        return True

    def __read_config(self):

        def __copy_init_conf_file():
            """
            Copy config.json to config folder and throw an Error
            notification if config.json does not exist.
            :return:
            """
            try:
                self.copy("config.json", self.config_path())
            except FileNotFoundError:
                notify("File config.json not found !", type="ERROR")

        conf_path = self.config_path("config.json")
        if not os.path.exists(conf_path):
            __copy_init_conf_file()
        self.config = JsonOrderedDict(conf_path)

    def __copy_template_folder(self):
        """
        Copy template folder with snappyHexMesh and blockMesh configurations
        to config-DIR in $WORKFLOW_DIR.
        """
        if os.path.exists("template/"):
            # copy only if not copied yet
            if not os.path.exists(self.config_path("template")):
                self.copy_folder_content("template/", self.config_path())
        else:
            notify("Template folder not found !", type="ERROR")