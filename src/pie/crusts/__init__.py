import os as _os
from importlib import import_module as _import_module
submodules = next(_os.walk('src/pie/crusts'))[1]
for submodule in submodules:
    if not submodule.startswith("_"):
        print("importing", submodule)
        globals()[submodule] = _import_module("." + submodule, __name__)