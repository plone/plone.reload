import os
import sys

from os.path import abspath
from os.path import dirname
from os.path import isfile
from os.path import join
from os.path import pardir

from plone.reload.xreload import Reloader

_marker = object()

BLACKLIST = _marker
EXCLUDE_EGGS = True
EXCLUDE_SITE_PACKAGES = True
MOD_TIMES = dict()


def blacklist():
    global BLACKLIST
    if BLACKLIST is _marker:
        tmp = os.environ.get('TMPDIR', None)
        swhome = os.environ.get('SOFTWARE_HOME', None)
        zopehome = os.environ.get('ZOPE_HOME', None)
        pyhome = abspath(join(dirname(os.__file__), pardir, pardir))

        if 'plone.reload' not in sys.modules:
            import plone.reload
        # Get the base dir and not the plone/reload package
        pr = dirname(sys.modules['plone.reload'].__file__)
        pr = abspath(os.path.join(pr, '..', '..'))
        BLACKLIST = frozenset([abspath(p) for p in
                              (tmp, swhome, zopehome, pyhome, pr) if p])

    return BLACKLIST


def in_search_path(path):
    if EXCLUDE_SITE_PACKAGES:
        if 'site-packages' in path:
            return False
        elif '.egg' in path:
            return False

    if True in [abspath(path).startswith(b) for b in blacklist()]:
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
            if in_search_path(f):
                modules.append((f, module))
    return modules


def get_mod_time(path):
    mtime = 0
    # If we have the compiled source, look for the source code change date
    # should the file exist
    if path.endswith('pyc') or path.endswith('pyo'):
        source = path[:-1]
        if os.path.isfile(source):
            path = source
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
