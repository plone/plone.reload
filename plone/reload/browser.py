from zope.app.component.hooks import setSite
from zope.component import getGlobalSiteManager
from zope.interface import implements

from Acquisition import aq_base
from Products.Five.browser import BrowserView
from Products.Five import zcml

from plone.reload.code import reload_code
from plone.reload.interfaces import ICodeReload
from plone.reload.interfaces import IZCMLReload
from plone.reload import PATCHES


class CodeReload(BrowserView):
    """Reload all changed code.
    """
    implements(ICodeReload)

    def reload(self):
        reloaded = reload_code()

        result = 'Code reloaded:\n\n'
        result += '\n'.join(reloaded)
        return result


class ZCMLReload(BrowserView):
    """Reload all global ZCML.
    """
    implements(IZCMLReload)

    def reload(self):
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

        # TODO Minimize all caches, we only really want to invalidate the
        # local site manager from all caches
        aq_base(self.context)._p_jar.db().cacheMinimize()
        return 'Global ZCML reloaded.'
