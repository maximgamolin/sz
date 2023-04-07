import os
from warnings import warn

import yaml


class ClassDoesNotExists(Exception):
    pass


class ClassExists(Exception):
    pass


class InjectorLine:

    def __init__(self, path):
        self.path = path


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
        return self.map[name].path


class Wrapper:

    def __init__(self, line: InjectorLine):
        self._line = line

    def __call__(self, *args, **kwargs):
        klass = __import__(self._line.path)
        return klass(*args, **kwargs)


def inject(name: str):
    storage = InjectorStorage()
    line = storage.fetch_resource(name)
    return Wrapper(line)


storage = InjectorStorage()



