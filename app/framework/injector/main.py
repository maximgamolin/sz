import os
from importlib import import_module
from warnings import warn

import yaml


class ClassDoesNotExists(Exception):
    pass


class ClassExists(Exception):
    pass


class InjectorLine:

    def __init__(self, path):
        self.path = path

    def module(self) -> str:
        return '.'.join(self.path.split('.')[:-1])

    def class_name(self) -> str:
        return self.path.split('.')[-1]


class InjectorStorage:
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(InjectorStorage, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.map: dict[str: InjectorLine] = {}
        try:
            config_path = os.environ['INJECTION_CFG_PATH']
        except KeyError:
            warn('INJECTION_CFG_PATH in environ is not set')
            return
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
        for i in cfg['injections']['repo']:
            name = i['name']
            path = i['path']
            if name in self.map:
                raise ClassExists(f'Class for {name} was registered')
            self.map[name] = InjectorLine(path)

    def fetch_resource(self, name: str):
        if name not in self.map:
            raise ClassDoesNotExists(f'Class for {name} is not registered')
        return self.map[name]


class Wrapper:

    def __init__(self, name: str):
        storage = InjectorStorage()
        self._line = storage.fetch_resource(name)

    def __call__(self, *args, **kwargs):
        module = import_module(self._line.module())
        klass = getattr(module, self._line.class_name())
        return klass(*args, **kwargs)


def inject(name: str):
    return Wrapper(name)


storage = InjectorStorage()



