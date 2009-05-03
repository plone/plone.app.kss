# -*- coding: UTF-8 -*-

import types
from Acquisition import aq_inner    

from zope.interface import implements
from zope.component import getAdapters, queryMultiAdapter, getUtility
from zope.viewlet.interfaces import IViewletManager, IViewlet

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
try:
    from Products.Five.browser.pagetemplatefile import BoundPageTemplate
    ZOPE2_12 = True
except ImportError:
    ZOPE2_12 = False

from Products.statusmessages import STATUSMESSAGEKEY
from Products.statusmessages.adapter import _decodeCookieValue

from kss.core import KSSView as base
from kss.core import force_unicode

from plone.portlets.interfaces import IPortletManager, IPortletRenderer

from interfaces import IPloneKSSView

header_macros = ViewPageTemplateFile('browser/macro_wrapper.pt')

class PloneKSSView(base):
    '''The base view that contains helpers, to be imported
    be other plone products
    '''

    implements(IPloneKSSView)
  
    def _macroContent(self, provider, macro_name, context=None, **kw):
        """
        """

        # Determine context to use for rendering
        if context is None:
            render_context = aq_inner(self.context)
        else:
            render_context = context

        # Build extra context. These variables will be in
        # scope for the macro.        
        extra_context = {'options':{}}
        extra_context.update(kw)
        the_macro = None

        # Determine what type of provider we are dealing with
        if isinstance(provider, types.StringType):
            # Page template or browser view. Traversal required.
            pt_or_view = render_context.restrictedTraverse(provider)
            if provider.startswith('@@'):            
                the_macro = pt_or_view.index.macros[macro_name]
            else:          
                the_macro = pt_or_view.macros[macro_name]

            # template_id seems to be needed, so add to options
            # if it is not there
            if not extra_context['options'].has_key('template_id'):
                extra_context['options']['template_id'] = provider.split('/')[-1]

        elif IViewlet.isImplementedBy(provider) or IPortletRenderer.isImplementedBy(provider):
            the_macro = provider.render.macros[macro_name]
        
        # Adhere to header_macros convention. Setting the_macro here
        # ensures that code calling this method cannot override the_macro.
        extra_context['options']['the_macro'] = the_macro

        # If context is explicitly passed in then make available
        if context is not None:
            extra_context['context'] = context

        content = header_macros.__of__(self).__of__(render_context).pt_render(
                        extra_context=extra_context)

        # IE6 has problems with whitespace at the beginning of content
        content = content.strip()

        # Always encoded as utf-8
        content = force_unicode(content, 'utf')
        return content

    def viewletMacroContent(self, manager_name, viewlet_name, macro_name, 
        context=None, **kw):
        """
        manager_name is the name of the viewlet manager
        viewlet_name is the name of the viewlet
        todo: lookup viewlet based on a single marker interface
        and thus eliminate the need for manager_name and viewlet_name
        """       
        manager = queryMultiAdapter(
            (self.context, self.request, self), 
            IViewletManager, 
            name=manager_name)

        viewlets = getAdapters(
            (manager.context, manager.request, manager.__parent__, manager), 
            IViewlet)

        target = None
        for order, (name, viewlet) in enumerate(viewlets):
            if name == viewlet_name:               
                return self._macroContent(viewlet, macro_name, context, **kw)

        # Raise on lookup error
        msg = "No viewlet %s registered with manager %s" % \
            (viewlet_name, manager_name)
        raise RuntimeError, msg

    def portletMacroContent(self, manager_name, iface, macro_name, 
        context=None, **kw):
        """
        manager_name is the name of the portlet manager
        iface is a marker interface which subclasses IPortletDataProvider
        todo: get rid of manager_name as required parameter
        """       
        # Determine lookup context
        if context is None:
            lookup_context = aq_inner(self.context)
        else:
            lookup_context = context

        manager = getUtility(
                    IPortletManager, 
                    name=manager_name, 
                    context=lookup_context)
        view = lookup_context.restrictedTraverse('@@plone')
        manager_renderer = manager(lookup_context, lookup_context.REQUEST, view)
        for di in manager_renderer.portletsToShow():
            if iface.isImplementedBy(di['assignment']):
                return self._macroContent(di['renderer'],
                    macro_name, 
                    context, **kw)

        # Raise on lookup error
        msg = "No portlet %s registered with manager %s" % \
            (iface.__name__, manager_name)
        raise RuntimeError, msg

    # xxx: macroContent currently (2009-05-02) has no unit tests,
    # so hopefully the backwards compatibility change is correct
    def macroContent(self, macropath, **kw):
        'Renders a macro and returns its text'
        path = macropath.split('/')
        if len(path) < 2 or path[-2] != 'macros':
            raise RuntimeError, 'Path must end with macros/name_of_macro (%s)' % (repr(macropath), )
        # needs string, do not tolerate unicode (causes but at traverse)
        jointpath = '/'.join(path[:-2]).encode('ascii')

        # put parameters on the request, by saving the original context
        self.request.form, orig_form = kw, self.request.form
        content = self._macroContent(
                    provider=jointpath, 
                    macro_name=path[-1],                  
                    )
        self.request.form = orig_form

        return content
 
    def issueAllPortalMessages(self):
        if hasattr(self.request.RESPONSE, 'cookies'):
            cookie = self.request.RESPONSE.cookies.get(STATUSMESSAGEKEY)
            if cookie:
                encodedstatusmessages = cookie['value']
                statusmessages = _decodeCookieValue(encodedstatusmessages)
            else:
                statusmessages = []
            for msg in statusmessages:
                self.getCommandSet('plone').issuePortalMessage(msg)
            self.request.RESPONSE.expireCookie(STATUSMESSAGEKEY, path='/')
