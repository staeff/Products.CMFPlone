# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import ISearchSchema
from Products.CMFPlone.testing import \
    PRODUCTS_CMFPLONE_INTEGRATION_TESTING

from plone.app.testing import TEST_USER_ID, setRoles
from plone.registry.interfaces import IRegistry

from zope.component import getUtility

import unittest2 as unittest


class ProductsCMFPloneSetupTest(unittest.TestCase):

    layer = PRODUCTS_CMFPLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = getUtility(IRegistry)

    def test_controlpanel_registry_is_available(self):
        self.assertTrue(
            self.registry.forInterface(ISearchSchema, prefix="plone")
        )

    def test_enable_livesearch_setting(self):
        self.assertTrue('enable_livesearch' in ISearchSchema.names())

    def test_types_not_searched(self):
        self.assertTrue('types_not_searched' in ISearchSchema.names())
