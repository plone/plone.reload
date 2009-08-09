import os
import tempfile
import unittest

from plone.reload import xreload

TESTS = os.path.join(os.path.dirname(__file__), 'data')


class TestReload(unittest.TestCase):

    def _create_temp(self):
        # This creates both a temporary file used as a module and also adds
        # an __init__.py to the data subfolder, to temporarily make it a
        # package
        temp = tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', dir=TESTS, delete=False)
        temp.close()
        fd = open(os.path.join(TESTS, '__init__.py'), mode="w")
        fd.write("#")
        fd.close()
        name = os.path.split(temp.name)[-1]
        modulename = 'plone.reload.tests.data.' + name[:-3]
        module = __import__(modulename,
            fromlist=['plone', 'reload', 'tests', 'data'])
        return temp.name, module

    def reload(self, text=None):
        module = self.module
        if text is not None:
            temp = open(self.name, mode='w')
            temp.write(text)
            temp.close()
        newmodule = self.reloader.reload()

    def setUp(self):
        self.name, self.module = self._create_temp()
        self.reloader = xreload.Reloader(self.module)

    def tearDown(self):
        os.unlink(self.name)
        sfile = self.name + 'c'
        if os.path.isfile(sfile):
            os.unlink(sfile)
        data_init = os.path.join(TESTS, '__init__.py')
        if os.path.isfile(data_init):
            os.unlink(data_init)
        if os.path.isfile(data_init + 'c'):
            os.unlink(data_init + 'c')


class TestReloadModule(TestReload):

    def test_immutable_constant_added(self):
        self.reload("FOO = 15")
        self.assertEquals(self.module.FOO, 15)

    def test_mutable_constant_added(self):
        self.reload("FOO = [1, 2]")
        self.assertEquals(self.module.FOO, [1, 2])

    def test_instance_constant_added(self):
        self.reload("FOO = object()")
        self.failUnless(isinstance(self.module.FOO, object))

    def test_function_added(self):
        self.reload("def foo(): return True")
        self.failUnless(self.module.foo())

    def test_class_added(self):
        self.reload(
            "class Foo(object):\n\tdef __init__(self):\n\t\tself.bar = 1"
        )
        self.assertEquals(self.module.Foo().bar, 1)

    def test_import_added(self):
        self.reload("def foo(): pass")
        self.reload("import os\ndef foo(): return os.pathsep")
        self.assertEquals(self.module.foo(), os.pathsep)


class TestReloadFunction(TestReload):

    def test_function_added(self):
        source = "def foo(): return True"
        self.reload(source)
        source = source + "\ndef bar(): return True\n"
        self.reload(source)
        self.failUnless(self.module.foo())
        self.failUnless(self.module.bar())

    def test_function_changed(self):
        self.reload("def foo(): return True")
        self.reload("def foo(): return False")
        self.failIf(self.module.foo())

    def test_function_changed_to_constant(self):
        self.reload("def foo(): return True")
        self.reload("foo = 15")
        self.assertEquals(self.module.foo, 15)

    def test_function_removed(self):
        source = "def foo(): return True"
        self.reload(source + "\ndef bar(): return True\n")
        self.reload(source)
        self.failUnless(self.module.foo())
        self.failUnless(getattr(self.module, 'bar', None) is None)


class TestReloadClass(TestReload):

    def test_class_added(self):
        source = "class Foo(object):\n\tdef __init__(self):\n\t\tself.bar = 1"
        self.reload(source)
        source = source + "\nclass Bar(object): bar = 2"
        self.reload(source)
        self.assertEquals(self.module.Foo().bar, 1)
        self.assertEquals(self.module.Bar().bar, 2)

    def test_class_variable_added(self):
        source = "class Foo(object):\n\tfoo = 1"
        self.reload(source)
        source = source + "\n\tbar = 2"
        self.reload(source)
        self.assertEquals(self.module.Foo().foo, 1)
        self.assertEquals(self.module.Foo().bar, 2)

    def test_class_variable_changed(self):
        self.reload("class Foo(object):\n\tfoo = 1")
        self.reload("class Foo(object):\n\tfoo = 2")
        self.assertEquals(self.module.Foo().foo, 2)

    def test_class_variable_removed(self):
        self.reload("class Foo(object):\n\tfoo = 1")
        self.reload("class Foo(object):\n\tpass")
        # We don't remove any class variables
        self.assertEquals(self.module.Foo().foo, 1)

    def test_class_init_added(self):
        base = "class Foo(object):\n"
        self.reload(base + "\tpass")
        self.reload(base + "\tdef __init__(self):\n\t\tself.bar = 2")
        self.assertEquals(self.module.Foo().bar, 2)

    def test_class_init_changed(self):
        base = "class Foo(object):\n\tdef __init__(self):\n"
        self.reload(base + "\t\tself.bar = 1")
        self.reload(base + "\t\tself.bar = 2")
        self.assertEquals(self.module.Foo().bar, 2)

    def test_class_init_removed(self):
        base = "class Foo(object):\n"
        self.reload(base + "\tdef __init__(self):\n\t\tself.bar = 2")
        self.reload(base + "\tpass")
        # We don't remove anything from a class
        self.assertEquals(self.module.Foo().bar, 2)

    def test_class_method_added(self):
        source = "class Foo(object):\n\tfoo = 1"
        self.reload(source)
        source = source + "\n\tdef bar(self):\n\t\treturn 2"
        self.reload(source)
        self.assertEquals(self.module.Foo().foo, 1)
        self.assertEquals(self.module.Foo().bar(), 2)

    def test_class_method_changed(self):
        base = "class Foo(object):\n\tdef foo(self, a):\n"
        self.reload(base + "\t\treturn a + 1")
        self.reload(base + "\t\treturn a + 2")
        self.assertEquals(self.module.Foo().foo(2), 4)

    def test_class_method_arguments_changed(self):
        base = "class Foo(object):\n"
        self.reload(base + "\tdef foo(self, a):\n\t\treturn a + 1")
        self.reload(base + "\tdef foo(self, a, b):\n\t\treturn a + b")
        self.assertEquals(self.module.Foo().foo(2, 3), 5)

    def test_class_property_added(self):
        base = "class Foo(object):\n"
        self.reload(base + "\tpass")
        self.reload(base + "\t@property\n\tdef foo(self):\n\t\treturn 1")
        self.assertEquals(self.module.Foo().foo, 1)

    def test_class_property_changed(self):
        base = "class Foo(object):\n\t@property\n\tdef foo(self):\n"
        self.reload(base + "\t\treturn 1")
        self.reload(base + "\t\treturn 2")
        self.assertEquals(self.module.Foo().foo, 2)

    def test_class_property_changed_to_method(self):
        base = "class Foo(object):\n"
        self.reload(base + "\t@property\n\tdef foo(self):\n\t\treturn 1")
        self.reload(base + "\n\tdef foo(self):\n\t\treturn 2")
        self.assertEquals(self.module.Foo().foo(), 2)

    def test_class_method_changed_to_property(self):
        base = "class Foo(object):\n"
        self.reload(base + "\n\tdef foo(self):\n\t\treturn 2")
        self.reload(base + "\t@property\n\tdef foo(self):\n\t\treturn 1")
        self.assertEquals(self.module.Foo().foo, 1)

    def test_class_staticmethod_added(self):
        base = "class Foo(object):\n"
        self.reload(base + "\tpass")
        self.reload(base + "\t@staticmethod\n\tdef foo():\n\t\treturn 1")
        self.assertEquals(self.module.Foo.foo(), 1)

    def test_class_staticmethod_changed(self):
        base = "class Foo(object):\n\t@staticmethod\n\tdef foo():\n"
        self.reload(base + "\t\treturn 1")
        self.reload(base + "\t\treturn 2")
        self.assertEquals(self.module.Foo.foo(), 2)

    def test_class_nested_function_changed(self):
        base = "class Foo(object):\n\tdef foo(self, a):\n"
        self.reload(base + "\t\tdef bar(a): return a + a\n\t\treturn bar(a)")
        self.reload(base + "\t\tdef bar(a): return a + 2\n\t\treturn bar(a)")
        self.assertEquals(self.module.Foo().foo(5), 7)

class TestReloadDecorator(TestReload):

    base = """\
def outer(func):
    def inner(self, *args):
        return func(self, *args)
    return inner

class Foo(object):
"""

    def test_class_decorater_added(self):
        self.reload(self.base + "\tdef foo(self, a): return a + 1")
        self.reload(self.base + "\t@outer\n\tdef foo(self, a): return a + 2")
        self.assertEquals(self.module.Foo().foo(2), 4)

    def test_class_decorated_method_changed(self):
        self.reload(self.base + "\t@outer\n\tdef foo(self, a): return a + 1")
        self.reload(self.base + "\t@outer\n\tdef foo(self, a): return a + 2")
        self.assertEquals(self.module.Foo().foo(3), 5)

    def test_class_decorator_changed(self):
        source = self.base + "\t@outer\n\tdef foo(self, a): return a + 1"
        self.reload(source)
        source = source.replace("func(self, *args)", "func(self, 15)")
        self.reload(source)
        self.assertEquals(self.module.Foo().foo(4), 16)

    def test_class_decorator_removed(self):
        self.reload(self.base + "\t@outer\n\tdef foo(self, a): return a + 1")
        self.reload(self.base + "\tdef foo(self, a): return a + 2")
        self.assertEquals(self.module.Foo().foo(5), 7)


class TestReloadInterface(TestReload):

    base = '''\
from zope.interface import Interface
class IFoo(Interface):
    def bar():
        """A true bar."""
'''

    def test_interface_method_added(self):
        self.reload(self.base)
        self.reload(self.base + '\tdef baz():\n\t\t"""Maybe a baz?"""')
        self.failUnless('bar' in self.module.IFoo.names())
        # Reloading interfaces doesn't work yet at all
        self.failIf('baz' in self.module.IFoo.names())


def test_modules():
    suite = unittest.TestSuite()
    suite.addTestSuite(TestReloadModule)
    suite.addTestSuite(TestReloadFunction)
    suite.addTestSuite(TestReloadClass)
    suite.addTestSuite(TestReloadDecorator)
    suite.addTestSuite(TestReloadInterface)
    return suite