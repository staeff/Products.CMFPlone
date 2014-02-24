from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IEditingSchema
from plone.app.registry.browser import controlpanel


class EditingControlPanelForm(controlpanel.RegistryEditForm):

    id = "EditingControlPanel"
    label = _(u"Editing settings")
    description = _("Editing settings.")
    schema = IEditingSchema
    schema_prefix = "plone"


class EditingControlPanel(controlpanel.ControlPanelFormWrapper):
    form = EditingControlPanelForm
