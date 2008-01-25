from plone.reload.patches import patch_generic_setup
from plone.reload.patches import patch_wicked

# Simple registry for adding more patches
PATCHES = [patch_generic_setup, patch_wicked]
