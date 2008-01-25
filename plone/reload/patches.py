# Conditional imports to make it work when those packages are not available

def patch_generic_setup():

    # GS 1.3
    try:
        from Products.GenericSetup.zcml import cleanUp
        cleanUp()
    except ImportError:
        pass
    # GS 1.4
    try:
        from Products.GenericSetup.zcml import cleanUpProfiles
        from Products.GenericSetup.zcml import cleanUpImportSteps
        from Products.GenericSetup.zcml import cleanUpExportSteps
        cleanUpProfiles()
        cleanUpImportSteps()
        cleanUpExportSteps()
    except ImportError:
        pass


def patch_wicked():
    try:
        from wicked.fieldevent.meta import cleanUp
        cleanUp()
    except ImportError:
        pass


def patch_cmfcore():
    try:
        from Products.CMFCore.zcml import cleanUp
        cleanUp()
    except ImportError:
        pass


def patch_pas():
    try:
        from Products.PluggableAuthService.zcml import cleanUp
        cleanUp()
    except ImportError:
        pass
