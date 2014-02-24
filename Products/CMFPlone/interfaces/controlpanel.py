from Products.CMFPlone import PloneMessageFactory as _
from basetool import IPloneBaseTool
from plone.locking.interfaces import ILockSettings
from zope.interface import Interface
from zope import schema


class IEditingSchema(Interface):

    visible_ids = schema.Bool(
        title=_(u"Show 'Short Name' on content?"),
        description=_(
            u"Display and allow users to edit the "
            u"'Short name' content identifiers, which form the "
            u"URL part of a content item's address. Once "
            u"enabled, users will then be able to enable this "
            u"option in their preferences."),
        default=False,
        required=False)

    default_editor = schema.Choice(
        title=_(u'Default editor'),
        description=_(
            u"Select the default wysiwyg "
            u"editor. Users will be able to choose their "
            u"own or select to use the site default."),
        default=u'TinyMCE',
        missing_value=set(),
        vocabulary="plone.app.vocabularies.AvailableEditors",
        required=True)

    ext_editor = schema.Bool(
        title=_(u'Enable External Editor feature'),
        description=_(
            u"Determines if the external editor "
            u"feature is enabled. This feature requires a "
            u"special client-side application installed. The "
            u"users also have to enable this in their "
            u"preferences."),
        default=False,
        required=False)

    enable_link_integrity_checks = schema.Bool(
        title=_(u"Enable link integrity checks"),
        description=_(
            u"Determines if the users should get "
            u"warnings when they delete or move content that "
            u"is linked from inside the site."),
        default=True,
        required=False)

    lock_on_ttw_edit = schema.Bool(
        title=_(u"Enable locking for through-the-web edits"),
        description=_(
            u"Disabling locking here will only "
            u"affect users editing content through the "
            u"Plone web UI.  Content edited via WebDAV "
            u"clients will still be subject to locking."),
        default=True,
        required=False)


class IControlPanel(IPloneBaseTool):
    """ Interface for the ControlPanel """

    def registerConfiglet(id, name, action, condition='', permission='',
                          category='Plone', visible=1, appId=None,
                          imageUrl=None, description='', REQUEST=None):
        """ Registration of a Configlet """

    def unregisterConfiglet(id):
        """ unregister Configlet """

    def unregisterApplication(appId):
        """ unregister Application with all configlets """

    def getGroupIds():
        """ list of the group ids """

    def getGroups():
        """ list of groups as dicts with id and title """

    def enumConfiglets(group=None):
        """ lists the Configlets of a group, returns them as dicts by
            calling .getAction() on each of them """


class ISearchSchema(Interface):

    enable_livesearch = schema.Bool(
        title=_(u'Enable LiveSearch'),
        description=_(
            u"Enables the LiveSearch feature, which shows live "
            u"results if the browser supports JavaScript."),
        default=True,
        required=True
    )

    types_not_searched = schema.Tuple(
        title=_(u"Define the types to be shown in the site and searched"),
        description=_(
            u"Define the types that should be searched and be "
            u"available in the user facing part of the site. "
            u"Note that if new content types are installed, they "
            u"will be enabled by default unless explicitly turned "
            u"off here or by the relevant installer."
        ),
        required=False,
        default=(
            'ATBooleanCriterion',
            'ATDateCriteria',
            'ATDateRangeCriterion',
            'ATListCriterion',
            'ATPortalTypeCriterion',
            'ATReferenceCriterion',
            'ATSelectionCriterion',
            'ATSimpleIntCriterion',
            'ATSimpleStringCriterion',
            'ATSortCriterion',
            'ChangeSet',
            'Discussion Item',
            'Plone Site',
            'TempFolder',
            'ATCurrentAuthorCriterion',
            'ATPathCriterion',
            'ATRelativePathCriterion',
        ),
        value_type=schema.Choice(
            source="plone.app.vocabularies.PortalTypes"
        ),
    )


# XXX: Why does ISiteSchema inherit from ILockSettings here ???
class ISiteSchema(ILockSettings):

    site_title = schema.TextLine(
        title=_(u'Site title'),
        description=_(
            u"This shows up in the title bar of "
            u"browsers and in syndication feeds."),
        default=u'Plone site')

    exposeDCMetaTags = schema.Bool(
        title=_(u"Expose Dublin Core metadata"),
        description=_(u"Exposes the Dublin Core properties as metatags."),
        default=False,
        required=False)

    enable_sitemap = schema.Bool(
        title=_(u"Expose sitemap.xml.gz"),
        description=_(
            u"Exposes your content as a file "
            u"according to the sitemaps.org standard. You "
            u"can submit this to compliant search engines "
            u"like Google, Yahoo and Microsoft. It allows "
            u"these search engines to more intelligently "
            u"crawl your site."),
        default=False,
        required=False)

    webstats_js = schema.SourceText(
        title=_(u'JavaScript for web statistics support'),
        description=_(
            u"For enabling web statistics support "
            u"from external providers (for e.g. Google "
            u"Analytics). Paste the code snippets provided. "
            u"It will be included in the rendered HTML as "
            u"entered near the end of the page."),
        default=u'',
        required=False)
