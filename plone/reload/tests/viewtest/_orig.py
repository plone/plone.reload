from zope.publisher.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Foo(BrowserView):
    template = ViewPageTemplateFile('test.pt')
    # -*- placeholder -*-
