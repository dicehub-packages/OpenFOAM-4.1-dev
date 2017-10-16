
from PyFoam.Basics.DataStructures import Vector, TupleProxy, Field

# DICE modules
# ============
from dice_tools import diceSync, signal, wizard

class FoamApp:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__files = {}
        self.__modified = set()
        wizard.subscribe('w_idle', self.__w_idle)
        
    def __w_idle(self):
        if self.__modified:
            for v in self.__modified:
                v.writeFile()
            self.__modified = set()

    def foam_file(self, name, file):
        if file is None:
            if name in self.__files:
                del self.__files[name]
        else:
            self.__files[name] = file
    
    def __set_value(self, path, value):
        path = path.split(' ')
        if path[-1].startswith('%'):
            value_type = path.pop(-1)[1:]
        else:
            value_type = None

        item = self.__files
        for p in path[:-1]:
            if isinstance(item, (Vector, list)):
                p = int(p)
            item = item[p]

        key = path[-1]
        if isinstance(item, (Vector, list)):
            key = int(key)

        if value is None:
            del item[key]
        else:
            item[key] = self.__convert_to(value, value_type)
            
        self.__modified.add(self.__files[path[0]])
        signal('foam:%s*'%' '.join(path))
        wizard.w_foam(path)

    def __convert_to(self, value, value_type=None):
        if value_type == 'tuple':
            value = TupleProxy(value)
        elif value_type == 'field':
            value = Field(value)
        elif value_type == 'field_vector':
            value = Field(Vector(*value))
        elif value_type == 'vector':
            value = Vector(value)

        if type(value) == bool:
            return 'yes' if value else 'no'
        elif isinstance(value, list):
            for i, v in enumerate(value):
                value[i] = self.__convert_to(v)
        elif isinstance(value, dict):
            return {k: self.__convert_to(v) for k, v in value.items()}
        return value

    def __convert_from(self, value, value_type=None):
        if value == 'yes':
            return True
        elif value == 'no':
            return False
        elif isinstance(value, TupleProxy):
            if value_type is not None and value_type != 'tuple':
                return None
            return value
        elif isinstance(value, Field):
            value = value.value()
            if isinstance(value, Vector):
                if value_type is not None and value_type != 'field_vector':
                    return None
                return [self.__convert_from(v) for v in value]
            else:
                if value_type is not None and value_type != 'field':
                    return None
                return value
        elif isinstance(value, Vector):
            if value_type is not None and value_type != 'vector':
                return None
            return [self.__convert_from(v) for v in value]
        elif isinstance(value, dict):
            return {k: self.__convert_from(v) for k, v in value.items()}

        if value_type is not None:
            return None

        return value

    def __get_value(self, path):
        path = path.split(' ')
        if path[-1].startswith('%'):
            value_type = path.pop(-1)[1:]
        else:
            value_type = None
        item = self.__files
        for p in path:
            if isinstance(item, (Vector, list)):
                p = int(p)
                if p >= len(item):
                    return None
            try:
                item = item[p]
            except (KeyError, TypeError, IndexError):
                return None
        return self.__convert_from(item, value_type)

    @diceSync('foam:')
    def __foam_sync(self, path):
        return self.__get_value(path)

    @__foam_sync.setter
    def __foam_sync(self, path, value):
        self.__set_value(path, value)
        return True

