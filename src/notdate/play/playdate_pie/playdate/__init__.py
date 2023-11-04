from shutil import copytree
import inspect, os
from subprocess import Popen
from json import load, dump

class Chdir:
    def __init__(self, directory):
        self._previous_dir = os.path.abspath(os.curdir)
        self.new_directory = directory
     
    def __enter__(self):
        os.chdir(self.new_directory)
 
    def __exit__(self, *args):
        os.chdir(self._previous_dir)

class InvalidLanguageError(Exception):
    pass

class MissingSkeletonError(Exception):
    pass

class NoCompilerError(Exception):
    pass

class Project:
    def __init__(self, directory, name, language="lua"):
        if language not in ["c", "lua"]:
            raise InvalidLanguageError("Invalid language for Playdate! Language must be in [\"c\", \"lua\"]")
        self._directory = directory
        self._language = language
        self._name = name
        self._skeleton = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    def copy_skeleton(self):
        if self._language not in ["c", "lua"]:
            raise InvalidLanguageError("Invalid language for Playdate! Language must be in [\"c\", \"lua\"]")
        skelepath = os.path.join(self._skeleton, f"{self._language}skeleton")
        if not os.path.exists(skelepath):
            raise MissingSkeletonError(f"Can't find the skeleton where it should be! Path {skelepath} is nonexistent")
        copytree(skelepath, self._directory)
        os.mkdir(os.path.join(self._directory, "build"))
    def compile(self):
        if self._language not in ["c", "lua"]:
            raise NoCompilerError(f"No compiler for language {self.language}")
        elif self._language == "lua":
            self._compile_lua()
        elif self._language == "c":
            self._compile_c() 
    def _compile_lua(self):
        Popen(["pdc", "-k", "src", os.path.join("build", f"{self._name}.pdx")])
    def _compile_c(self):
        with Chdir("build"):
            Popen(["cmake", ".."])
            Popen(["make"])
    def save_project(self, file):
        # TODO: What else do we need to save?
        serialized = {
            "version": 1,
            "language": self._language,
            "name": self._name
        }
        with open(file, mode="w") as f:
            dump(serialized, f)
    @classmethod
    def load_project(cls, file):
        with open(file, mode="r") as f:
            meta = load(f)
        return cls(None, meta["name"], language=meta["language"])




    
        