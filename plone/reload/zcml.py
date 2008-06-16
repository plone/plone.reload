from zope.app.component.hooks import setSite
from zope.component import getGlobalSiteManager

from Products.Five import zcml

from plone.reload import PATCHES


def reload_zcml():
    setSite(None)
    gsm = getGlobalSiteManager()
    gsm.__init__(gsm.__name__)

    # Apply patches
    global PATCHES
    for patch in PATCHES:
        patch()

    # Reload all ZCML
    zcml._initialized = False
    zcml._context._seen_files.clear()
    zcml.load_site()
