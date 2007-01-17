# -*- coding: UTF-8 -*-

from urlparse import urlsplit
from kss.core.BeautifulSoup import BeautifulSoup
from zope.interface import implements
from Acquisition import Implicit
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from azaxview import AzaxBaseView
from kss.core import kssaction, KssExplicitError
from interfaces import IPloneAzaxView

class Acquirer(Implicit):
    # XXX the next should be best to avoid - but I don't know how!
    __allow_access_to_unprotected_subobjects__ = 1
    main_template = ZopeTwoPageTemplateFile('browser/main_template_standalone.pt')

def acquirerFactory(context):
    return context.aq_chain[0].__of__(Acquirer().__of__(context.aq_parent))

def getCurrentContext(context):
    """ Check if context is default page in folder and/or portal
    """
    # check if context is default page
    context_state = context.restrictedTraverse('@@plone_context_state')
    portal = getToolByName(context, 'portal_url').getPortalObject()
    if context_state.is_default_page() and context != portal:
        context = context.aq_inner.aq_parent
    return context


class ContentView(Implicit, AzaxBaseView):

    implements(IPloneAzaxView)
    
    # --
    # Replacing content region
    # --

    # Override main template in this context
    main_template2 = ZopeTwoPageTemplateFile('browser/main_template_standalone.pt')

    #@staticmethod
    def _filter_action(actions, id, found=None):
        if found is not None:
            return found
        for action in actions:
            if action['id'] == id:
                return action
    _filter_action = staticmethod(_filter_action)    # for zope 2.8 / python 2.3

    @kssaction
    def replaceContentRegion(self, tabid, url):
        '''Replace content region by tab id

        Usage::
            ul.contentViews li a:click {
	        evt-click-preventdefault: True;
	        action-server: replaceContentRegion;
	        replaceContentRegion-tabid: nodeAttr(id, true);
	        replaceContentRegion-url: nodeAttr(href);
            }

        REMARK:

        We use the acquisition context hack to replace the main template
        with one that only renders the content region. This means that if
        the target template reuses main_template we win. Otherwise we loose
        and we get a full page of which we have to take out the required
        part with BeautifulSoup.

        Warning ("Do you want to...") when we leave the page is not implemented.

        '''
        # REMARK on error handling: 
        # If KssExplicitError is raised, the control will be passed
        # to the error handler defined on the client. I.e. for this rule,
        # the static plone-followLink should be activated. This means that
        # if this method decides it cannot handle the situation, it
        # raises this exception and we fallback to the non-AJAX behaviour.
        #
        # XXX The next checks could be left out - but we won't be able to change the tabs.
        # This could be solved with not using the tabs or doing server side quirks.
        # This affect management screens, for example, that are not real actions.
        if not tabid or tabid == 'content':
            raise KssExplicitError, 'No tabid on the tab'
        if not tabid.startswith('contentview-'):
            raise RuntimeError, 'Not a valid contentview id "%s"' % tabid
        # Split the url into it's components
        (proto, host, path, query, anchor) = urlsplit(url)
        # if the url doesn't use http(s) or has a query string or anchor
        # specification, don't bother
        if query or anchor or proto not in ('http', 'https'):
            raise KssExplicitError, 'Unhandled protocol on the tab'
        # make the wrapping for the context, to overwrite main_template
        # note we have to use aq_chain[0] *not* aq_base.
        # XXX however just context would be good too? Hmmm
        wrapping = acquirerFactory(self.context)
        # Figure out the template to render.
        # We need the physical path which we can obtain from the url
        path = list(self.request.physicalPathFromURL(url))
        obj_path = list(self.context.getPhysicalPath())
        if path == obj_path:
            # target is the default view of the method.
            # url is like: ['http:', '', 'localhost:9777', 'kukitportlets', 'prefs_users_overview']
            # physical path is like: ('', 'kukitportlets')
            # We lookup the default view for the object, which may be
            # another object, if so we give up, otherwise we use the
            # appropriate template
            utils = getToolByName(self.context, 'plone_utils')
            if utils.getDefaultPage(self.context) is not None:
                raise KssExplicitError, 'no default page on the tab'
            viewobj, viewpath = utils.browserDefault(self.context)
            if len(viewpath) == 1:
                viewpath = viewpath[0]
            template = viewobj.restrictedTraverse(viewpath)
        else:
            # see if it is a method on the same context object...
            # url is like: ['http:', '', 'localhost:9777', 'kukitportlets', 'prefs_users_overview']
            # physical path is like: ('', 'kukitportlets')
            if path[:-1] != obj_path:
                raise KssExplicitError, 'cannot reload since the tab visits a different context'
            method = path[-1]
            # Action method may be a method alias: Attempt to resolve to a template.
            try:
                method = self.context.aq_inner.getTypeInfo().queryMethodID(method, default=method)
            except AttributeError:
                # Don't raise if we don't have a CMF 1.5 FTI
                pass
            template = wrapping.restrictedTraverse(method)
        # We render it
        content = template()
        # Now. We take out the required node from it!
        # We need this in any way, as we don't know if the template
        # actually used main_template! In that case we would have
        # the *whole* html which is wrong.
        soup = BeautifulSoup(content)
        replace_id = 'region-content'
        tag = soup.find('div', id=replace_id)
        if tag is None:
            raise RuntimeError, 'Result content did not contain <div id="%s">' % replace_id
        # now we send it back to the client
        result = unicode(tag)
        ##result = unicode(content, 'utf')
        ksscore = self.getCommandSet('core')
        ksscore.replaceHTML(ksscore.getHtmlIdSelector(replace_id), result)
        # to remove old tab highlight,...
        ksscore.setAttribute(ksscore.getCssSelector("ul.contentViews li"), name='class', value='plain');
        # ... and put the highlight to the newly selected tab
        ksscore.setAttribute(ksscore.getHtmlIdSelector(tabid), name='class', value='selected');

    def changeViewTemplate(self, url):
        '''Replace content region after selecting template from drop-down.
        
        Usage::
            dl#templateMenu dd a:click {
            evt-click-preventdefault: True;
            action-server: changeViewTemplate;
            changeViewTemplate-url: nodeAttr(href);
            }

        REMARK:

        Cheat at the moment: we render down the whole page
        but take out the required part only
        This will be optimized more to replace the main template
        for the context of the call

        Warning when we leave the page is not implemented.
        '''
        templateid = url.split('templateId=')[-1].split('&')[0]
        context = getCurrentContext(self.context)
        wrapping = acquirerFactory(context)
        # XXX I believe selectViewTemplate script will be replaced by an
        # adapter or a view in the new implementation of CMFDynamicFTI
        context.selectViewTemplate(templateid)
        # Figure out the template to render.
        template = wrapping.restrictedTraverse(templateid)
        # We render it
        content = template()
        # Now. We take out the required node from it!
        # We need this in any way, as we don't know if the template
        # actually used main_template! In that case we would have
        # the *whole* html which is wrong.

        soup = BeautifulSoup(content)
        replace_id = 'content'
        tag = soup.find('div', id=replace_id)
        if tag is None:
            raise RuntimeError, 'Result content did not contain <div id="%s">' % replace_id
        # now we send it back to the client
        result = unicode(tag)
        ##result = unicode(content, 'utf')
        ksscore = self.getCommandSet('core')
        ksscore.replaceHTML(ksscore.getHtmlIdSelector(replace_id), result)

        self.issueAllPortalMessages()
        self.cancelRedirect()
        # XXX We need to take care of the URL history here,
        # For instance if we come from the edit page and change the view we
        # stay on the edit URL but with a view page
        return self.render()

    def cutObject(self):
        context = getCurrentContext(self.context)
        context.object_cut()
        self.replaceMenu()
        self.issueAllPortalMessages()
        self.cancelRedirect()
        return self.render()

    def copyObject(self):
        context = getCurrentContext(self.context)
        context.object_copy()
        self.replaceMenu()
        self.issueAllPortalMessages()
        self.cancelRedirect()
        return self.render()

    @kssaction
    def changeWorkflowState(self, url):
        (proto, host, path, query, anchor) = urlsplit(url)
        if not path.endswith('content_status_modify'):
            raise KssExplicitError, 'content_status_modify is not handled'
        action = query.split("workflow_action=")[-1].split('&')[0]
        context = self.context
        context.content_status_modify(action)
        self.replaceMenu()
        # XXX This updating has to go away, DCWorkflow has to take care of this
        self.getCommandSet('refreshportlet').refreshPortlet('navigation', 'portlet-navigation-tree')
        self.issueAllPortalMessages()
        self.cancelRedirect()

    def replaceMenu(self):
        # render it
        menu_body = self.macroContent('global_contentviews/macros/content_actions')
        # Good. Now, unfortunately we don't have any marker on the outside div.
        # So we just select the <dl> for insertion.
        # This could be spared with smarter templating.
        # XXX Has to go into a macro in global_contentmenu
        # the the line with replaceInnerHTML should be used again (see below).
        result = unicode(menu_body)
        # Command the replacement
        ksscore = self.getCommandSet('core')
        # ksscore.replaceInnerHTML(ksscore.getCssSelector('div#content div.contentActions'), result)
        ksscore.replaceHTML(ksscore.getCssSelector('div#content div.contentActions'), result)

