from zope.app.component.hooks import setSite
from zope.component import getGlobalSiteManager

from Products.Five import zcml

from plone.reload import PATCHES


def reload_zcml():
    gsm = getGlobalSiteManager()
    old_gsm_dict = gsm.__dict__.copy()
    try:
        setSite(None)
        gsm.__init__(gsm.__name__)
        # Apply patches
        global PATCHES
        for patch in PATCHES:
            patch()

        # Reload all ZCML
        zcml._initialized = False
        zcml._context._seen_files.clear()
        zcml.load_site()
    except Exception, e:
        gsm.__init__(gsm.__name__)
        gsm.__dict__.clear()
        gsm.__dict__.update(old_gsm_dict)
        raise e
