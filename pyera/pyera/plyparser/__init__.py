from .common import *
import contextlib

def parse(module, input, filename = '<input>', warning_handler = default_warning_handler, error_handler = default_error_handler, *args, **kwargs):
    @contextlib.contextmanager
    def set_variables():
        old_warning_handler = module.warning
        old_error_handler = module.error
        try:
            old_lexer_filename = module.lexer.filename
        except AttributeError:
            old_lexer_filename = None
        try:
            old_parser_filename = module.parser.filename
        except AttributeError:
            old_parser_filename = None
        module.warning = warning_handler
        module.error = error_handler
        module.lexer.filename = filename
        module.parser.filename = filename
        yield
        module.warning = old_warning_handler
        module.error = old_error_handler
        module.lexer.filename = old_lexer_filename
        module.parser.filename = old_parser_filename
    with set_variables():
        if 'parse' in module.__dict__:
            return module.parse(input, *args, **kwargs)
        return module.parser.parse(input, *args, **kwargs)
