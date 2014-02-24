# -*- coding: utf-8 -*-
from Products.CMFPlone.testing import \
    PRODUCTS_CMFPLONE_INTEGRATION_TESTING
from plone.registry import Registry
from Products.CMFPlone.interfaces import IEditingSchema
import unittest2 as unittest

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles


class EditingControlPanelIntegrationTest(unittest.TestCase):
    """Tests that the editing settings are stored as plone.app.registry
    settings.
    """

    layer = PRODUCTS_CMFPLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_editing_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="editing-controlpanel")
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_editing_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue('EditingSettings' in [
            a.getAction(self)['id']
            for a in self.controlpanel.listActions()
        ])

    def test_visible_ids_setting(self):
        self.assertTrue('visible_ids' in IEditingSchema.names())

    def test_default_editor_setting(self):
        self.assertTrue('default_editor' in IEditingSchema.names())

    def test_ext_editor_setting(self):
        self.assertTrue('ext_editor' in IEditingSchema.names())

    def test_enable_link_integrity_checks_setting(self):
        self.assertTrue(
            'enable_link_integrity_checks' in IEditingSchema.names())

    def test_lock_on_ttw_edit_setting(self):
        self.assertTrue('lock_on_ttw_edit' in IEditingSchema.names())
