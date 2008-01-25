from zope.component import getGlobalSiteManager
from zope.interface import implements

from Products.Five.browser import BrowserView
from Products.Five import zcml

from plone.reload.interfaces import IZCMLReload
from plone.reload import PATCHES

class ZCMLReload(BrowserView):
    """Reload all global ZCML.
    """
    implements(IZCMLReload)

    def reload(self):
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
        return 'Global ZCML reloaded.'
