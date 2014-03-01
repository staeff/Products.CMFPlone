from Products.CMFPlone import PloneMessageFactory as _
from basetool import IPloneBaseTool
from plone.locking.interfaces import ILockSettings
from zope.interface import Interface
from zope import schema


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


class ISecuritySchema(Interface):

    enable_self_reg = schema.Bool(
        title=_(u'Enable self-registration'),
        description=_(
            u"Allows users to register themselves on the site. If "
            u"not selected, only site managers can add new users."),
        default=False,
        required=False)

    enable_user_pwd_choice = schema.Bool(
        title=_(u'Let users select their own passwords'),
        description=_(
            u"If not selected, a URL will be generated and "
            u"e-mailed. Users are instructed to follow the link to "
            u"reach a page where they can change their password and "
            u"complete the registration process; this also verifies "
            u"that they have entered a valid email address."),
        default=False,
        required=False)

    enable_user_folders = schema.Bool(
        title=_(u'Enable User Folders'),
        description=_(
            u"If selected, home folders where users can create "
            u"content will be created when they log in."),
        default=False,
        required=False)

    allow_anon_views_about = schema.Bool(
        title=_(u"Allow anyone to view 'about' information"),
        description=_(
            u"If not selected only logged-in users will be able to "
            u"view information about who created an item and when it "
            u"was modified."),
        default=False,
        required=False)

    use_email_as_login = schema.Bool(
        title=_(u'Use email address as login name'),
        description=_(
            u"Allows new  users to login with their email address "
            u"instead of specifying a separate login name. (Existing "
            u"users must go to the @@personal-information page once "
            u"and save it before this setting has effect for them. "
            u"Or use the @@migrate-to-emaillogin page as a site "
            u"admin)"),
        default=False,
        required=False)


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


class IUserGroupsSettingsSchema(Interface):

    many_groups = schema.Bool(
        title=_(u'Many groups?'),
        description=_(
            u"Determines if your Plone is optimized "
            u"for small or large sites. In environments with a "
            u"lot of groups it can be very slow or impossible "
            u"to build a list all groups. This option tunes the "
            u"user interface and behaviour of Plone for this "
            u"case by allowing you to search for groups instead "
            u"of listing all of them."),
        default=False
    )

    many_users = schema.Bool(
        title=_(u'Many users?'),
        description=_(
            u"Determines if your Plone is optimized "
            u"for small or large sites. In environments with a "
            u"lot of users it can be very slow or impossible to "
            u"build a list all users. This option tunes the user "
            u"interface and behaviour of Plone for this case by "
            u"allowing you to search for users instead of "
            u"listing all of them."),
        default=False
    )
