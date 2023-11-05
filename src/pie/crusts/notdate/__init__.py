import os as _os
from importlib import import_module as _import_module
submodules = _os.walk('src/pie/crusts')
for submodule in submodules:
    if not submodule.startswith("_"):
        print("importing", submodule)
        globals()[submodule] = _import_module(value)
from . import *