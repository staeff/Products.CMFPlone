from Acquisition import aq_parent, aq_inner, Explicit
from Products.CMFCore.permissions import ManagePortal

from OFS.Folder import Folder
from DateTime import DateTime
from App.class_init import InitializeClass
from zope.interface import implements
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary

from OFS.PropertyManager import PropertyManager
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo
from Products.CMFPlone.PloneBaseTool import PloneBaseTool
from Products.CMFPlone.interfaces \
    import IPropertiesTool, ISimpleItemWithProperties
from Products.MailHost.interfaces import IMailHost

from plone.registry.interfaces import IRegistry
from plone.registry import Record
from plone.registry import field

from Products.Five import BrowserView
from OFS.Traversable import Traversable
from persistent.list import PersistentList

from datetime import datetime
import logging
from .utils import log

_marker = object()

class DummySheet(object, Traversable, Explicit):
    """ Dummy Sheet """

    security = ClassSecurityInfo()
    __allow_access_to_unprotected_subobjects__ = True

    def __init__(self, name):
        self.sheet_name = name
        self.registry = getUtility(IRegistry)

    security.declarePublic('unrestrictedTraverse')
    def unrestrictedTraverse(self, path, default=_marker, restricted=False):
        """ ABC """
        return self.registry['plone.%s.%s' % (self.sheet_name, path)]

    def __getattr__(self, name):
        """ ABC """
        if not name.startswith('_'):
            return self.registry['plone.%s.%s' % (self.sheet_name, name)]
        return super(DummySheet, self).__getattr__(name)

InitializeClass(DummySheet)

class PropertiesTool(PloneBaseTool, Folder):
    """ A backwards compatibility wrapper to get values from the registry
    """

    id = 'portal_properties'
    toolicon = 'skins/plone_images/topic_icon.png'

    meta_type = 'Plone Properties Tool'

    implements(IPropertiesTool)

    security = ClassSecurityInfo()
    migrated = False

    def title(self):
        """ title  """
        return self.meta_type

    prop2regmap = {
        'boolean': field.Bool,
        'date': field.Datetime,
        'float': field.Float,
        'int': field.Int,
        'lines': field.Tuple,
        'long': field.Int,
        'string': field.TextLine,
        'text': field.Text,
        'tokens': field.Tuple,
        }

    sheets = []

    def migrate(self):
        self.sheets = PersistentList()
        if not self.migrated:
            registry = getUtility(IRegistry)
            for sheet_name, sheet in self.objectItems('Plone Property Sheet'):
                self.sheets.append(sheet_name)
                for prop in sheet._properties:
                    prop_id = prop['id']
                    if prop_id in ('title',):
                        # Exclude properties like title
                        continue
                    value = getattr(sheet, prop['id'])
                    fieldconstructor = self.prop2regmap[prop['type']]
                    if prop['type'] in ('selection', 'multiple selection'):
                        log('Skipping >%s< field >%s<' % (prop['type'], prop['id']), severity=logging.WARN)
                        continue
                    elif prop['type'] == 'date':
                        propfield = fieldconstructor(title=unicode(prop_id, 'utf-8'))
                        value = DateTime(value).asdatetime()
                    elif fieldconstructor == field.Tuple:
                        propfield = fieldconstructor(title=unicode(prop_id, 'utf-8'), value_type=field.TextLine())
                        value = tuple([unicode(item, 'utf-8') for item in value])
                    else:
                        propfield = fieldconstructor(title=unicode(prop_id, 'utf-8'))
                    if isinstance(value, str):
                        value = unicode(value, 'utf-8') 
                    record = Record(propfield, value=value)
                    registry.records['plone.%s.%s' % (sheet_name, prop_id) ] = record
            
            self.migrated = True

    def __bobo_traverse__(self, REQUEST, name):
        self.migrated = False
        if not self.migrated:
            self.migrate()
        if name in self.sheets:
            return DummySheet(name).__of__(self)
        return super(PropertiesTool, self).__bobo_traverse__(REQUEST, name)
       

    def __getattr__(self, name):
        if name in self.sheets:
            return DummySheet(name).__of__(self)
        return super(PropertiesTool, self).__getattr__(name)

    # Taken from CMFDefault.PropertiesTool since this is no base class any longer
    def smtp_server(self):
        return getUtility(IMailHost).smtp_host

InitializeClass(PropertiesTool)


class SimpleItemWithProperties (PropertyManager, SimpleItem):
    """
    A common base class for objects with configurable
    properties in a fixed schema.
    """

    implements(ISimpleItemWithProperties)

    def __init__(self, id, title=''):
        self.id = id
        self.title = title

    meta_type = 'Plone Property Sheet'

    manage_options = (PropertyManager.manage_options
                     + SimpleItem.manage_options)

InitializeClass(SimpleItemWithProperties)
