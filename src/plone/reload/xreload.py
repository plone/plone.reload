# xreload.py.

"""Alternative to reload().

This works by executing the module in a scratch namespace, and then
patching classes, methods and functions. This avoids the need to
patch instances. New objects are copied into the target namespace.

Taken and extended from xreload as posted by Guido van Rossum:

    http://mail.python.org/pipermail/edu-sig/2007-February/007787.html

"""

from importlib import reload
from zope.interface.interface import Specification

import importlib
import inspect
import sys
import types

CLASS_STATICS = frozenset(["__dict__", "__doc__", "__module__", "__weakref__"])


class ClosureChanged(Exception):
    pass


class Reloader:
    """Reload a module in place, updating classes, methods and functions.

    Args:
      mod: a module object

    Returns:
      The (updated) input object itself.
    """

    def __init__(self, module):
        self.mod = module

    def reload(self):
        # Get the module name, e.g. 'foo.bar.whatever'
        modname = self.mod.__name__

        # Get the module namespace (dict) early; this is part of the type check
        modns = self.mod.__dict__
        # Parse it into package name and module name, e.g. 'foo.bar' and
        # 'whatever'
        i = modname.rfind(".")
        if i >= 0:
            pkgname, modname = modname[:i], modname[i + 1 :]
        else:
            pkgname = None
        # Compute the search path
        if pkgname:
            # We're not reloading the package, only the module in it
            pkg = sys.modules[pkgname]
        else:
            # Search the top-level module path
            pkg = None
        package_name = pkg.__name__ if pkg else None
        specs = importlib.util.find_spec(self.mod.__name__, package=package_name)
        filename = specs.origin
        if specs.has_location:
            with open(filename, "rb") as stream:
                source = stream.read()
                # PeterB: if we don't strip the source code and add newline we
                # get a SyntaxError even if `python $filename` is perfectly
                # happy.
                source = source.strip() + b"\n"
                code = compile(source, filename, "exec")
        else:
            # Fall back to built-in reload()
            return reload(self.mod)

        # Execute the code im a temporary namespace; if this fails, no changes
        tmpns = {
            "__name__": f"{pkgname}.{modname}",
            "__file__": filename,
            "__doc__": modns["__doc__"],
        }
        exec(code, tmpns)
        # Now we get to the hard part
        _update_scope(modns, tmpns)
        # Now update the rest in place
        for name in set(modns) & set(tmpns):
            modns[name] = self._update(modns[name], tmpns[name])
        # Done!
        return self.mod

    def _update(self, oldobj, newobj):
        """Update oldobj, if possible in place, with newobj.

        If oldobj is immutable, this simply returns newobj.

        Args:
          oldobj: the object to be updated
          newobj: the object used as the source for the update

        Returns:
          either oldobj, updated in place, or newobj.
        """
        if not isinstance(oldobj, type(newobj)):
            # Cop-out: if the type changed, give up
            return newobj

        new_module = getattr(newobj, "__module__", None)
        if new_module != self.mod.__name__:
            # Do not update objects in-place that have been imported.
            # Just update their references.
            return newobj

        if isinstance(newobj, Specification):
            # XXX we can't update interfaces because their internal
            # data structures break. We'll have to implement the reload method
            # for those and patch it in.
            return oldobj
        if inspect.isclass(newobj):
            return _update_class(oldobj, newobj)
        elif inspect.isfunction(newobj):
            return _update_function(oldobj, newobj)

        # XXX Support class methods, static methods, other decorators
        # Not something we recognize, just give up
        # This line is currently not hit at all, since we only call this on
        # a module. It's pretty hard to have a non-function, non-class entity
        # in a module, which has a __module__ pointer to the module itself
        return newobj  # pragma NO COVER


def _closure_changed(oldcl, newcl):
    old = oldcl is None and -1 or len(oldcl)
    new = newcl is None and -1 or len(newcl)
    if old != new:
        return True
    if old > 0 and new > 0:
        for i in range(old):
            same = oldcl[i] == newcl[i]
            if not same:
                return True
    return False


def _update_scope(oldscope, newscope):
    oldnames = set(oldscope)
    newnames = set(newscope)
    # Add newly introduced names
    for name in newnames - oldnames:
        oldscope[name] = newscope[name]
    # Delete names that are no longer current
    for name in oldnames - newnames:
        if not name.startswith("__"):
            del oldscope[name]


def _update_function(oldfunc, newfunc):
    """Update a function object."""
    if _closure_changed(oldfunc.__closure__, newfunc.__closure__):
        raise ClosureChanged()
    setattr(oldfunc, "__code__", newfunc.__code__)
    setattr(oldfunc, "__defaults__", newfunc.__defaults__)
    _update_scope(oldfunc.__globals__, newfunc.__globals__)
    # XXX What else?
    return oldfunc


def _update_method(oldmeth, newmeth):
    """Update a method object."""
    # XXX What if im_func is not a function?
    _update_function(oldmeth, newmeth)
    return oldmeth


def _update_class(oldclass, newclass):
    """Update a class object."""
    # XXX What about __slots__?
    olddict = oldclass.__dict__
    newdict = newclass.__dict__
    oldnames = set(olddict)
    newnames = set(newdict)
    for name in newnames - oldnames:
        setattr(oldclass, name, newdict[name])

    # Note: We do not delete attributes, because various ZCML directives,
    # grokkers and other wiring add class attributes during startup that
    # would get lost if we did this. Note that attributes will still be
    # overwritten if they've changed.
    #
    # for name in oldnames - newnames:
    #     delattr(oldclass, name)

    for name in oldnames & newnames - CLASS_STATICS:
        try:
            new = getattr(newclass, name)
            old = getattr(oldclass, name, None)
            if isinstance(new, (types.FunctionType, types.MethodType)):
                if isinstance(old, property) and not isinstance(new, property):
                    # Removing a decorator
                    setattr(oldclass, name, new)
                elif isinstance(new, types.FunctionType):
                    # Under Py3 there are only functions
                    _update_function(old, new)
                elif isinstance(new, types.MethodType):
                    # Py2-only
                    _update_method(old, new)
            else:
                new2 = newdict.get(name)
                if new is not new2:
                    # Do we have some sort of descriptor? Set the underlying
                    # descriptor and not the result of the descriptor call
                    setattr(oldclass, name, new2)
                else:
                    # Fallback to just replace the item
                    setattr(oldclass, name, new)
        except ClosureChanged:
            # If the closure changed, we need to replace the entire function
            setattr(oldclass, name, new)

    return oldclass
