from zope.interface import Interface


class IReload(Interface):
    """Interface for the ZCML reload view.
    """


class ICodeReload(Interface):
    """Interface for the code reload view.
    """

    def reload():
        """Reload all changed code."""


class IZCMLReload(Interface):
    """Interface for the ZCML reload view.
    """

    def reload():
        """Reprocess all global ZCML."""
