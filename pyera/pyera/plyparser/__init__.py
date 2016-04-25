from .common import *
import contextlib

def parse(module, input, warning_handler = default_warning_handler, error_handler = default_error_handler):
    @contextlib.contextmanager
    def set_error_handler():
        old_warning_handler = module.warning
        old_error_handler = module.error
        module.warning = warning_handler
        module.error = error_handler
        yield
        module.warning = old_warning_handler
        module.error = old_error_handler
    with set_error_handler():
        return module.parser.parse(input)
