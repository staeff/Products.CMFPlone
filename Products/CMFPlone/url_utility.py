#from Products.CMFCore.URLTool import URLTool as BaseTool
from Products.CMFCore.utils import getToolByName, registerToolInterface
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
#from Products.CMFPlone.PloneBaseTool import PloneBaseTool

from posixpath import normpath
from urlparse import urlparse, urljoin
import re
from Products.CMFPlone.interfaces import IURLUtility
from zope import interface
from Products.Five.browser import BrowserView
import logging;
from OFS.SimpleItem import SimpleItem
from zope.component.hooks import getSite
from Products.CMFCore.interfaces._content import ISiteRoot
from zope.interface import providedBy
from Acquisition.interfaces import IAcquirer
from Acquisition import Implicit
logger = logging.getLogger(__name__)


class URLUtility(Implicit):
    """This is the portal_url tool rewrite to be a utility"""
    interface.implements(IURLUtility)
    security = ClassSecurityInfo()
    security.declarePublic('__call__')
    security.declarePublic('getPortalObject')
    security.declarePublic('getRelativeContentPath')
    security.declarePublic('getRelativeContentURL')
    security.declarePublic('getPortalPath')
    security.declarePublic('isURLInPortal')
    security.declarePublic('getRelativeUrl')

    def __call__(self, relative=0, *args, **kw):
        """ Get by default the absolute URL of the portal.
        """
#        logger.info('__call__')
        # XXX: this method violates the rules for tools/utilities:
        # absolute_url() depends implicitly on REQUEST
        return self.getPortalObject().absolute_url(relative=relative)

    def getPortalObject(self):
        """ Get the portal object itself.
        """
#        logger.info('getPortalObject')
        #code ripped of plone.api because plone.api is not already parts of
        #of the core.
        #TODO: use plone.api.portal.get()
        closest_site = getSite()
        if closest_site is not None:
            for potential_portal in closest_site.aq_chain:
                if ISiteRoot in providedBy(potential_portal):
                    return potential_portal
        raise ValueError("No portal object found")

    def getRelativeContentPath(self, content):
        """ Get the path for an object, relative to the portal root.
        """
#        logger.info('getRelativeContentPath')
        portal_path_length = len( self.getPortalObject().getPhysicalPath() )
        content_path = content.getPhysicalPath()
        return content_path[portal_path_length:]

    def getRelativeContentURL(self, content):
        """ Get the URL for an object, relative to the portal root.
        """
        return '/'.join( self.getRelativeContentPath(content) )

    getRelativeUrl = getRelativeContentURL

    def getPortalPath(self):
        """ Get the portal object's URL without the server URL component.
        """
        return '/'.join( self.getPortalObject().getPhysicalPath() )

    def isURLInPortal(self, url, context=None):
        """ Check if a given url is on the same host and contains the portal
            path.  Used to ensure that login forms can determine relevant
            referrers (i.e. in portal).  Also return true for some relative
            urls if context is passed in to allow for url parsing. When context
            is not provided, assume that relative urls are in the portal. It is
            assumed that http://portal is the same portal as https://portal.

            External sites listed in 'allow_external_login_sites' of
            site_properties are also considered within the portal to allow for
            single sign on.
        """
        # sanitize url
        url = re.sub('^[\x00-\x20]+', '', url).strip()

        p_url = self()

        _, u_host, u_path, _, _, _ = urlparse(url)
        if not u_host and not u_path.startswith('/'):
            if context is None:
                return True  # old behavior
            if not context.isPrincipiaFolderish:
                useurl = context.aq_parent.absolute_url()
            else:
                useurl = context.absolute_url()
        else:
            useurl = p_url  # when u_path.startswith('/')
        if not useurl.endswith('/'):
            useurl += '/'

        # urljoin to current url to get an absolute path
        _, u_host, u_path, _, _, _ = urlparse(urljoin(useurl, url))

        # normalise to end with a '/' so /foobar is not considered within /foo
        if not u_path:
            u_path = '/'
        else:
            u_path = normpath(u_path)
            if not u_path.endswith('/'):
                u_path += '/'
        _, host, path, _, _, _ = urlparse(p_url)
        if not path.endswith('/'):
            path += '/'
        if host == u_host and u_path.startswith(path):
            return True

        pp = getToolByName(self.getPortalObject(),
                              'portal_properties')
        props = pp.site_properties
        for external_site in props.getProperty('allow_external_login_sites', []):
            _, host, path, _, _, _ = urlparse(external_site)
            if not path.endswith('/'):
                path += '/'
            if host == u_host and u_path.startswith(path):
                return True
        return False


class URLToolView(BrowserView, URLUtility):
    """Alias to let context/portal_url working"""
    interface.implements(IURLUtility)

    def __init__(self, context, request):
        #TODO: add this as deprecated
        logger.info('portal_url throw a browser view')
        BrowserView.__init__(self, context, request)
        URLUtility.__init__(self)

portal_url = URLUtility()
registerToolInterface('portal_url', IURLUtility)

InitializeClass(URLUtility)

