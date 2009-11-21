from zope.interface import implements

from Acquisition import aq_base
from Acquisition import aq_inner
import Globals
from Products.Five.browser import BrowserView

from plone.reload.code import reload_code
from plone.reload.interfaces import IReload
from plone.reload.zcml import reload_zcml

HAS_CMF = True
try:
    from plone.reload.template import reload_template
except ImportError:
    HAS_CMF = False


class Reload(BrowserView):
    """Reload view.
    """
    implements(IReload)

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.message = None

    def __call__(self):
        action = self.request.form.get('action')
        if action is not None:
            if self.available():
                if action == 'code':
                    self.message = self.code_reload()
                elif action == 'zcml':
                    self.message = self.zcml_reload()
            if action == 'template':
                self.message = self.template_reload()
        return self.index()

    def available(self):
        if Globals.DevelopmentMode:
            return True
        return False

    def status(self):
        return self.message

    def template_reload_available(self):
        return HAS_CMF and not Globals.DevelopmentMode

    def template_reload(self):
        if HAS_CMF:
            reloaded = reload_template(aq_inner(self.context))
            if reloaded > 0:
                return '%s templates reloaded.' % reloaded
            return 'No templates reloaded.'
        return 'CMF is not installed. Templates cannot be reloaded.'

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
