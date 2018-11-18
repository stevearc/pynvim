"""Code for supporting compatibility across python versions."""

import sys
import warnings
if sys.version_info >= (3, 4):
    from importlib.machinery import PathFinder
    original_find_module = PathFinder.find_spec
else:
    from imp import find_module as original_find_module


IS_PYTHON3 = sys.version_info >= (3, 0)
IS_PYTHON3_7 = sys.version_info >= (3, 7)


if IS_PYTHON3:
    def find_module(fullname, path):
        """Compatibility wrapper for imp.find_module
        (or find_spec in Python 3.7+).

        Automatically decodes arguments (must be Unicode in Python3).
        """
        if isinstance(fullname, bytes):
            fullname = fullname.decode()
        if isinstance(path, bytes):
            path = path.decode()
        elif isinstance(path, list):
            newpath = []
            for element in path:
                if isinstance(element, bytes):
                    newpath.append(element.decode())
                else:
                    newpath.append(element)
            path = newpath
        return original_find_module(fullname, path)

    # There is no 'long' type in Python3 just int
    long = int
    unicode_errors_default = 'surrogateescape'
else:
    find_module = original_find_module
    unicode_errors_default = 'strict'

NUM_TYPES = (int, long, float)


def check_async(async_, kwargs, default):
    """Return a value of 'async' in kwargs or default when async_ is None.

    This helper function exists for backward compatibility (See #274).
    It shows a warning message when 'async' in kwargs is used to note users.
    """
    if async_ is not None:
        return async_
    elif 'async' in kwargs:
        warnings.warn(
            '"async" attribute is deprecated. Use "async_" instead.',
            DeprecationWarning,
        )
        return kwargs.pop('async')
    else:
        return default
