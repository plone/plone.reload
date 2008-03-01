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
MOD_TIMES = _marker
SEARCH_MODULES = _marker
SEARCH_PATH = _marker

def blacklist():
    global BLACKLIST
    if BLACKLIST is _marker:
        tmp = os.environ.get('TMPDIR', None)
        swhome = os.environ.get('SOFTWARE_HOME', None)
        zopehome = os.environ.get('ZOPE_HOME', None)
        pyhome = abspath(join(dirname(os.__file__), pardir, pardir))

        if 'plone.reload' not in sys.modules:
            import plone.reload
        pr = dirname(sys.modules['plone.reload'].__file__)

        BLACKLIST = frozenset([abspath(p) for p in
                              (tmp, swhome, zopehome, pyhome, pr) if p])

    return BLACKLIST


def search_path():
    global SEARCH_PATH
    if SEARCH_PATH is _marker:
        path = []
        sys_path = [p for p in tuple(sys.path) if p]
        if EXCLUDE_SITE_PACKAGES:
            sys_path = [p for p in sys_path if 'site-packages' not in p]
        if EXCLUDE_SITE_PACKAGES:
            sys_path = [p for p in sys_path if '.egg' not in p]

        for p in sys_path:
            if True not in [abspath(p).startswith(b) for b in blacklist()]:
                path.append(p)

        SEARCH_PATH = frozenset(path)

    return SEARCH_PATH


def in_search_path(path):
    for p in search_path():
        if path.startswith(p):
            return True
    return False


def search_modules():
    global SEARCH_MODULES
    if SEARCH_MODULES is _marker:
        modules = []
        for name, module in sys.modules.items():
            if module is not None:
                f = getattr(module, '__file__', None)
                if f is None:
                    continue
                f = abspath(f)
                if in_search_path(f):
                    modules.append((f, module))
        SEARCH_MODULES = frozenset(modules)
    return SEARCH_MODULES


def get_mod_time(path):
    found = path
    mtime = 0
    if path.endswith('pyc'):
        if os.path.isfile(path[:-1]):
            found = path[:-1]
    if isfile(found):
        try:
            mtime = os.stat(path)[8]
        except (OSError, IOError):
            pass
    return mtime


def setup_mod_times(refresh=False):
    global MOD_TIMES
    if MOD_TIMES is _marker or refresh:
        MOD_TIMES = dict()
        for path, module in search_modules():
            MOD_TIMES[path] = (get_mod_time(path), module)
    return MOD_TIMES


def check_mod_times():
    changed = []
    for path, (time, module) in setup_mod_times().items():
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
