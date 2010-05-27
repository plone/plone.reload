# xreload.py.

"""Alternative to reload().

This works by executing the module in a scratch namespace, and then
patching classes, methods and functions. This avoids the need to
patch instances. New objects are copied into the target namespace.

Taken and extended from xreload as posted by Guido van Rossum:

    http://mail.python.org/pipermail/edu-sig/2007-February/007787.html

"""

import marshal
import imp
import sys
import types
import inspect

import zope.component


CLASS_STATICS = frozenset(["__dict__", "__doc__", "__module__", "__weakref__"])


class ClosureChanged(Exception):
    pass


class Reloader(object):
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
            pkgname, modname = modname[:i], modname[i+1:]
        else:
            pkgname = None
        # Compute the search path
        if pkgname:
            # We're not reloading the package, only the module in it
            pkg = sys.modules[pkgname]
            path = pkg.__path__  # Search inside the package
        else:
            # Search the top-level module path
            pkg  = None
            path = None  # Make find_module() uses the default search path
        # Find the module; may raise ImportError
        (stream, filename, (suffix, mode, kind)) = imp.find_module(modname, path)
        # Turn it into a code object
        try:
            # Is it Python source code or byte code read from a file?
            # XXX Could handle frozen modules, zip-import modules
            if kind not in (imp.PY_COMPILED, imp.PY_SOURCE):
                # Fall back to built-in reload()
                return reload(self.mod)
            if kind == imp.PY_SOURCE:
                source = stream.read()
                # PeterB: if we don't strip the source code and add newline we
                # get a SyntaxError even if `python $filename` is perfectly
                # happy.
                source = source.strip()+'\n'
                code = compile(source, filename, "exec")
            else:
                # I have no idea how to test this one
                code = marshal.load(stream) #pragma NO COVER
        finally:
            if stream:
                stream.close()
        # Execute the code im a temporary namespace; if this fails, no changes
        tmpns = {'__name__': '%s.%s' % (pkgname, modname),
                 '__file__': filename,
                 '__doc__': modns['__doc__']}
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
        if type(oldobj) is not type(newobj):
            # Cop-out: if the type changed, give up
            return newobj

        new_module = getattr(newobj, '__module__', None)
        if new_module != self.mod.__name__:
            # Do not update objects in-place that have been imported.
            # Just update their references.
            return newobj

        if isinstance(newobj, zope.interface.interface.Specification):
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
        return newobj #pragma NO COVER


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
        if not name.startswith('__'):
            del oldscope[name]


def _update_function(oldfunc, newfunc):
    """Update a function object."""
    if _closure_changed(oldfunc.func_closure, newfunc.func_closure):
        raise ClosureChanged
    oldfunc.func_code = newfunc.func_code
    oldfunc.func_defaults = newfunc.func_defaults
    _update_scope(oldfunc.func_globals, newfunc.func_globals)
    # XXX What else?
    return oldfunc


def _update_method(oldmeth, newmeth):
    """Update a method object."""
    # XXX What if im_func is not a function?
    _update_function(oldmeth.im_func, newmeth.im_func)
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
            if isinstance(new, types.MethodType):
                if isinstance(old, property) and not isinstance(new, property):
                    # Removing a decorator
                    setattr(oldclass, name, new.im_func)
                else:
                    _update_method(old, new)
            elif isinstance(new, types.FunctionType):
                # __init__ is a function
                _update_function(old, new)
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
            setattr(oldclass, name, new.im_func)

    return oldclass
