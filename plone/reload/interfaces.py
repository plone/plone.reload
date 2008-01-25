from zope.interface import Attribute
from zope.interface import Interface

class IZCMLReload(Interface):
    """Interface for the ZCML reload view.
    """

    def reload():
        """Reprocess all global ZCML."""
