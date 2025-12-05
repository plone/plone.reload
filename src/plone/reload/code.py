from importlib.util import cache_from_source
from importlib.util import source_from_cache
from plone.reload import config
from plone.reload.xreload import Reloader

import os
import sys


_marker = object()
MOD_TIMES = dict()


def _cache_from_source(path):
    if "__pycache__" in path:
        return path
    return cache_from_source(path)


def _source_from_cache(path):
    if "__pycache__" in path:
        return source_from_cache(path)
    return path


def in_search_path(path):
    if "site-packages" in path:
        return False
    elif ".egg" in path:
        return False
    return True


def search_modules():
    modules = []
    for _, module in sys.modules.items():
        if module is not None:
            f = getattr(module, "__file__", None)
            # Standard library modules don't have a __file__
            if f is None:
                continue
            f = os.path.abspath(_source_from_cache(f))
            if config.EXCLUDE_SITE_PACKAGES:
                if in_search_path(f):
                    modules.append((f, module))
            else:
                modules.append((f, module))
    return modules


def get_mod_time(path):
    mtime = 0
    # If we have the compiled source, look for the source code change date
    path = _source_from_cache(path)
    # protect against missing and unaccessible files
    if os.path.isfile(path):
        mtime = os.stat(path)[8]
    return mtime


def get_mod_times(event=None):
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
    reloaded = []
    for path, time, module in check_mod_times():
        r = Reloader(module)
        module = r.reload()
        MOD_TIMES[path] = (time, module)
        reloaded.append(path)
    return reloaded
