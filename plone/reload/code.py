import os
import sys

from os.path import abspath
from os.path import isfile

from plone.reload.xreload import Reloader

_marker = object()

EXCLUDE_SITE_PACKAGES = True
MOD_TIMES = dict()


def in_search_path(path):
    if 'site-packages' in path:
        return False
    elif '.egg' in path:
        return False
    return True


def search_modules():
    modules = []
    for name, module in sys.modules.items():
        if module is not None:
            f = getattr(module, '__file__', None)
            # Standard library modules don't have a __file__
            if f is None:
                continue
            f = abspath(f)
            if EXCLUDE_SITE_PACKAGES:
                if in_search_path(f):
                    modules.append((f, module))
            else:
                modules.append((f, module))
    return modules


def get_mod_time(path):
    mtime = 0
    # If we have the compiled source, look for the source code change date
    if path.endswith('pyc') or path.endswith('pyo'):
        source = path[:-1]
        if os.path.isfile(source):
            path = source
    # protect against missing and unaccessible files
    if isfile(path):
        try:
            mtime = os.stat(path)[8]
        except (OSError, IOError):
            pass
    return mtime


def get_mod_times():
    global MOD_TIMES
    for path, module in search_modules():
        if path not in MOD_TIMES:
            MOD_TIMES[path] = (get_mod_time(path), module)
    return MOD_TIMES


def check_mod_times():
    changed = []
    for path, (time, module) in get_mod_times().items():
        newtime = get_mod_time(path)
        if time < newtime:
            changed.append((path, newtime, module))
    return changed


def reload_code():
    global MOD_TIMES
    reloaded = []
    for path, time, module in check_mod_times():
        r = Reloader(module)
        module = r.reload()
        MOD_TIMES[path] = (time, module)
        reloaded.append(path)
    return reloaded


# setupFinalLogging is the closest I could find, which resembles a
# `Zope is finished loading event`
# Let's initialize our modified times registry once.

def wrap_final_logging(func):
    def init_times(*args, **kwargs):
        get_mod_times()
        return func(*args, **kwargs)
    return init_times

from Zope2.Startup import UnixZopeStarter
from Zope2.Startup import WindowsZopeStarter

UnixZopeStarter.setupFinalLogging = \
    wrap_final_logging(UnixZopeStarter.setupFinalLogging)
WindowsZopeStarter.setupFinalLogging = \
    wrap_final_logging(WindowsZopeStarter.setupFinalLogging)
