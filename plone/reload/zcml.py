try:
    from zope.site.hooks import setSite
except ImportError:
    from zope.app.component.hooks import setSite

from zope.component import getGlobalSiteManager
from zope.testing import cleanup

from Products.Five import zcml

CORE_CLEANUPS = frozenset([
    'zope.app.apidoc.classregistry',
    'zope.app.component.hooks',
    'zope.app.security.principalregistry',
    'zope.app.schema.vocabulary',
    'zope.component.globalregistry',
    'zope.schema.vocabulary',
    'zope.security.management',
    'zope.security.checker',
    'zope.site.hooks',
    'Products.Five.zcml',
    'Products.Five.eventconfigure',
    'Products.Five.fiveconfigure',
    'Products.Five.site.metaconfigure',
    'Products.Five.sizeconfigure',
])


def cleanups():
    registered = [c[0] for c in cleanup._cleanups]
    functions = []
    for r in registered:
        if r.__module__ not in CORE_CLEANUPS:
            functions.append(r)
    return functions


def reload_zcml():
    gsm = getGlobalSiteManager()
    old_gsm_dict = gsm.__dict__.copy()
    try:
        setSite(None)
        gsm.__init__(gsm.__name__)
        # Clean up
        for clean in cleanups():
            clean()
        # Reload all ZCML
        zcml._initialized = False
        zcml._context._seen_files.clear()
        zcml.load_site()
    except Exception, e:
        gsm.__init__(gsm.__name__)
        gsm.__dict__.clear()
        gsm.__dict__.update(old_gsm_dict)
        raise e
