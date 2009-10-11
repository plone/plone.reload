from zope.interface import implements

from Acquisition import aq_base
import Globals
from Products.Five.browser import BrowserView

from plone.reload.code import reload_code
from plone.reload.interfaces import IReload
from plone.reload.zcml import reload_zcml


class Reload(BrowserView):
    """Reload view.
    """
    implements(IReload)

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.message = None

    def __call__(self):
        if self.available():
            action = self.request.form.get('action')
            if action is not None:
                if action == 'code':
                    self.message = self.code_reload()
                elif action == 'zcml':
                    self.message = self.zcml_reload()
        return self.index()

    def available(self):
        if Globals.DevelopmentMode:
            return True
        return False

    def status(self):
        return self.message

    def code_reload(self):
        if not self.available():
            return

        reloaded = reload_code()

        result = ''
        if reloaded:
            result += 'Code reloaded:\n\n'
            result += '\n'.join(reloaded)
        else:
            result = 'No code reloaded!'
        return result

    def zcml_reload(self):
        if not self.available():
            return

        # We always do an implicit code reload so we can register all newly
        # added classes.
        reloaded = reload_code()
        reload_zcml()

        # TODO Minimize all caches, we only really want to invalidate the
        # local site manager from all caches
        aq_base(self.context)._p_jar.db().cacheMinimize()
        result = ''
        if reloaded:
            result += 'Code reloaded:\n\n'
            result += '\n'.join(reloaded)
        else:
            result = 'No code reloaded!'
        result += '\n\nGlobal ZCML reloaded.'
        return result
