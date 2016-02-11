import os
import sys
import types
import unittest

TESTS = os.path.dirname(__file__)


class TestSearch(unittest.TestCase):

    def test_in_search_path(self):
        from plone.reload.code import in_search_path
        self.assertTrue(in_search_path('/home/foo/plone.reload'))
        prefix = sys.prefix
        s1 = os.path.join(prefix, 'lib', 'site-packages')
        self.assertFalse(in_search_path(s1))
        python = 'python-%s.%s' % sys.version_info[:2]
        s2 = os.path.join(prefix, 'lib', python, 'site-packages')
        self.assertFalse(in_search_path(s2))
        import setuptools
        egg = os.path.dirname(setuptools.__file__)
        if '.egg' in egg:
            self.assertFalse(in_search_path(egg))

    def test_search_modules(self):
        from plone.reload.code import search_modules
        found = False
        we = 'plone' + os.sep + 'reload' + os.sep + '__init__.py'
        for f, m in search_modules():
            if we in f:
                found = True
                break
        self.assertTrue(found)

    def test_search_modules_eggs(self):
        from plone.reload.code import search_modules
        from plone.reload import config
        try:
            esp = config.EXCLUDE_SITE_PACKAGES
            config.EXCLUDE_SITE_PACKAGES = False
            found = False
            for f, m in search_modules():
                if '.egg' in f:
                    found = True
            self.assertTrue(found)
        finally:
            config.EXCLUDE_SITE_PACKAGES = esp


class TestTimes(unittest.TestCase):

    def test_get_mod_time(self):
        from plone.reload.code import get_mod_time
        tests = os.path.join(TESTS, '__init__.py')
        our_time = get_mod_time(tests)
        self.assertEqual(our_time, os.stat(tests)[8])

    def test_get_mod_time_compiled(self):
        from plone.reload.code import get_mod_time
        tests = os.path.join(TESTS, '__init__.py')
        tests_c = os.path.join(TESTS, '__init__.pyc')
        our_time = get_mod_time(tests_c)
        self.assertEqual(our_time, os.stat(tests)[8])

    def test_get_mod_times(self):
        from plone.reload.code import get_mod_times
        our_package = os.path.abspath(
            os.path.join(TESTS, os.pardir, '__init__.pyc'))
        times = get_mod_times()
        self.assertTrue(our_package in times)
        self.assertTrue(isinstance(times[our_package][1], types.ModuleType))

    def test_check_mod_times(self):
        from plone.reload.code import check_mod_times
        self.assertEqual(len(check_mod_times()), 0)

    def test_check_mod_times_change(self):
        from plone.reload.code import check_mod_times
        from plone.reload.code import MOD_TIMES
        our_package = os.path.abspath(
            os.path.join(TESTS, os.pardir, '__init__.pyc'))
        our_entry = MOD_TIMES[our_package]
        try:
            MOD_TIMES[our_package] = (our_entry[0] - 10, our_entry[1])
            self.assertEqual(len(check_mod_times()), 1)
        finally:
            MOD_TIMES[our_package] = our_entry

    def test_reload_code(self):
        from plone.reload.code import reload_code
        self.assertEqual(len(reload_code()), 0)

    def test_reload_code_change(self):
        from plone.reload.code import reload_code
        from plone.reload.code import MOD_TIMES
        our_package = os.path.abspath(
            os.path.join(TESTS, os.pardir, '__init__.pyc'))
        our_entry = MOD_TIMES[our_package]
        try:
            MOD_TIMES[our_package] = (our_entry[0] - 10, our_entry[1])
            self.assertEqual(len(reload_code()), 1)
        finally:
            MOD_TIMES[our_package] = our_entry
