from zope.interface import implements

from Acquisition import aq_base
from Products.Five.browser import BrowserView

from plone.reload.code import reload_code
from plone.reload.interfaces import IReload
from plone.reload.zcml import zcml_reload


class Reload(BrowserView):
    """Reload view.
    """
    implements(IReload)


class CodeReload(BrowserView):
    """Reload all changed code.
    """
    implements(IReload)

    def reload(self):
        reloaded = reload_code()

        result = 'Code reloaded:\n\n'
        result += '\n'.join(reloaded)
        return result


class ZCMLReload(BrowserView):
    """Reload all code and global ZCML.
    """
    implements(IReload)

    def reload(self):
        # We always do an implicit code reload so we can register all newly
        # added classes.
        reloaded = reload_code()
        zcml_reload()

        # TODO Minimize all caches, we only really want to invalidate the
        # local site manager from all caches
        aq_base(self.context)._p_jar.db().cacheMinimize()
        result = 'Global ZCML reloaded.\n\n'
        result += 'Code reloaded:\n\n'
        result += '\n'.join(reloaded)
        return result
