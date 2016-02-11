from zope.component import getGlobalSiteManager
from zope.site.hooks import setSite
from zope.testing import cleanup

# BBB: Zope 2.12
try:
    from Zope2.App import zcml
    zcml  # pyflakes
except ImportError:
    from Products.Five import zcml


CORE_CLEANUPS = frozenset([
    'OFS.metaconfigure',
    'Products.Five.zcml',
    'Products.Five.eventconfigure',
    'Products.Five.fiveconfigure',
    'Products.Five.sizeconfigure',
    'zope.component.globalregistry',
    'zope.schema.vocabulary',
    'zope.security.management',
    'zope.security.checker',
    'zope.site.hooks',
    'Zope2.App.zcml',
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
    except Exception as e:
        gsm.__init__(gsm.__name__)
        gsm.__dict__.clear()
        gsm.__dict__.update(old_gsm_dict)
        raise e
