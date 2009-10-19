from Products.CMFCore.FSObject import FSObject
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName

def reload_skins(tool):
    counter = 0
    for folder in tool.objectValues():
        for obj in folder.objectValues():
            if isinstance(obj, FSObject):
                parsed = getattr(obj, '_parsed', 0)
                if parsed:
                    obj._parsed = 0
                    counter += 1
    return counter

def reload_template(root):
    counter = 0
    for obj in root.objectValues():
        if ISiteRoot.providedBy(obj):
            tool = getToolByName(obj, 'portal_skins', None)
            if tool is not None:
                counter = reload_skins(tool)
    return counter
