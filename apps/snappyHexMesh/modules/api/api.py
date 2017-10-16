
from abc import ABCMeta
import inspect

class ApiMeta(ABCMeta):

    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        props = {}
        ro_props = {}
        methods = {}
        for k, v in inspect.getmembers(cls):
            if k[0] != '_':
                if inspect.isdatadescriptor(v):
                        try:
                            v.__set__(None, None)
                        except AttributeError as err:
                            if "can't set attribute" in err.args:
                                ro_props[k] = v
                                continue
                        props[k] = v
                else:
                    methods[k] = v
                
        cls.__api_props__ = props
        cls.__api_ro_props__ = ro_props
        cls.__api_methods__ = methods
        cls.__api_attrs__ = props.keys() | ro_props.keys() | methods.keys()
        # print(cls.__name__, cls.__api_attrs__)
        return cls

class Api(metaclass=ApiMeta):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def dump(self, path=''):
        # print(self.__class__, self.__api_props__)
        for k in sorted(self.__api_props__):
            attr = self.__api_props__[k]
            if attr.__doc__:
                for doc in attr.__doc__.split('\n'):
                    print("# " + doc)
            v = getattr(self, k)
            if path:
                k = path + '.' + k
            print(k,'=', '"%s"'%v if isinstance(v, str) else v, '\n')

        for k in sorted(self.__api_ro_props__):
            v = getattr(self, k)
            if isinstance(v, Api):
                v.dump(k)

class RootApi(Api, dict):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getitem__(self, key):
        if key in self.__api_attrs__:
            return getattr(self, key)
        if key in self:
            return super().__getitem__(key)
        raise KeyError(key)

    def __setitem__(self, key, value):
        if key in self.__api_props__:
            setattr(self, key, value)
        else:
            super().__setitem__(key, value)

    def __delitem__(self, key):
        if hasattr(self, key):
            raise TypeError()
        super().__delitem__(key)