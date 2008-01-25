from Products.GenericSetup import zcml
from wicked.fieldevent import meta

def patch_generic_setup():
    zcml.cleanUpProfiles()
    zcml.cleanUpImportSteps()
    zcml.cleanUpExportSteps()


def patch_wicked():
    meta.cleanUp()
