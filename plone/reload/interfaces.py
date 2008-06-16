from zope.interface import Interface


class IReload(Interface):
    """Interface for the ZCML reload view.
    """

    def status():
        """Return a status text."""

    def code_reload():
        """Reload all changed code."""

    def zcml_reload():
        """Reprocess all global ZCML."""
