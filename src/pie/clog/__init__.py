from click import echo, style

import inspect

import os.path

try:
    from __main__ import __file__ as main_file
except ImportError:
    main_file = None

def caller_info(skip=1):
    """Get the name of a caller in the format module.class.method.
    Copied from: https://gist.github.com/techtonik/2151727
    :arguments:
        - skip (integer): Specifies how many levels of stack
                          to skip while getting caller name.
                          skip=1 means "who calls me",
                          skip=2 "who calls my caller" etc.
    :returns:
        - package (string): caller package.
        - module (string): caller module.
        - klass (string): caller classname if one otherwise None.
        - caller (string): caller function or method (if a class exist).
        - line (int): the line of the call.
        - An empty string is returned if skipped levels exceed stack height.
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ''
    parentframe = stack[start][0]

    # module and packagename.
    module_info = inspect.getmodule(parentframe)
    if module_info:
        mod = module_info.__name__.split('.')

    # class name.
    klass = None
    if 'self' in parentframe.f_locals:
        klass = parentframe.f_locals['self'].__class__.__name__

    # method or function name.
    caller = None
    if parentframe.f_code.co_name != '<module>':  # top level usually
        caller = parentframe.f_code.co_name

    # call line.
    line = parentframe.f_lineno

    # Remove reference to frame
    # See: https://docs.python.org/3/library/inspect.html#the-interpreter-stack
    del parentframe

    return mod

STDOUT = None # Readability counts
# I.e., Logger(log_file=None) might be confusing, 
# but Logger(log_file=clog.STDOUT) is much less
# odd to an outsider.

GET_MODULE_INFO_AUTOMATICALLY = True

ERROR = 0
WARNING = 1
INFO = 2
DEBUG = 3

level_to_str = {
    ERROR: "error",
    WARNING: "warning",
    INFO: "info",
    DEBUG: "debug"
}

str_to_level = {
    "error": ERROR,
    "warning": WARNING,
    "info": INFO,
    "debug": DEBUG
}

class LogFailure(BaseException):
    """
    Inherits from BaseException to stop it from being caught and sent to Logger.exception
    """

class Logger:
    def __init__(self,
        debug_color="blue",
        info_color="green",
        warning_color="yellow", 
        error_color="red",
        level=INFO,
        log_file=STDOUT,
        module_info=GET_MODULE_INFO_AUTOMATICALLY,
        module_info_format=" {module_info}: ",
        message_format="[{level}] {message}"
    ):
        self.debug_color = debug_color
        self.info_color = info_color
        self.warning_color = warning_color
        self.error_color = error_color
        self.level = level
        if type(self.level) == str:
            self.level = str_to_level[self.level]
        self.log_file = log_file
        self.module_info = module_info
        self.module_info_format = module_info_format
        self.message_format = message_format
    
    def get_module_info(self):
        module_info = None
        if self.module_info == GET_MODULE_INFO_AUTOMATICALLY:
            module_info = "".join(caller_info(skip=3)) # caller (module we want)
            # of caller (logging function) of caller (caller_info)
            if module_info == "__main__":
                module_info = os.path.basename(main_file)[:-3]
        elif type(self.module_info) == str:
            module_info = self.module_info # module info was passed to us, nice!
        elif hasattr(self.module_info, __file__):
            module_info = self.module_info.__name__
        elif self.module_info == None:
            module_info = ""
        else:
            raise LogFailure(f"Can't figure out how to handle module info {module_info} of type {type(module_info)}")
        return self.module_info_format.format(module_info=module_info)
    def exception(self, tb):
        raise NotImplementedError # how ironic...
    def set_level(self, level):
        self.level = level
        if type(self.level) == str:
            self.level = str_to_level[self.level]
    def log(self, message, level):
        error = False
        if level in level_to_str:
            level = level_to_str[level]
        
        match level.lower():
            case "debug":
                color = self.debug_color
            case "info":
                color = self.info_color
            case "warning":
                color = self.warning_color
            case "error":
                color = self.error_color
                error = True
            case _:
                raise LogFailure(f"Invalid log level: {level}")
        if str_to_level[level] <= self.level:
            echo(style(
                self.message_format.format(
                        level=level.upper(),
                        message=message, 
                        module_info=self.get_module_info()
                    ), fg=color
                ), err=error, file=self.log_file
            )

logger = Logger(module_info=None)
        