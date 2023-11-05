import os as _os
from importlib import import_module as _import_module
import inspect as _inspect
submodules = next(_os.walk(_os.path.join(_os.path.dirname(_os.path.abspath(_inspect.getfile(_inspect.currentframe()))))))[1]
for submodule in submodules:
    if not submodule.startswith("_"):
        globals()[submodule] = _import_module("." + submodule, __name__)