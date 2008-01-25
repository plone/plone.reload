from plone.reload.patches import patch_cmfcore
from plone.reload.patches import patch_generic_setup
from plone.reload.patches import patch_pas
from plone.reload.patches import patch_wicked

# Simple registry for adding more patches
PATCHES = [
    patch_cmfcore,
    patch_generic_setup,
    patch_pas,
    patch_wicked
    ]
