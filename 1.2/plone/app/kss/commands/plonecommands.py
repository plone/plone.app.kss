from zope.interface import implements
from zope.component import getMultiAdapter, getUtility

from Products.statusmessages.message import Message

from plone.portlets.interfaces import IPortletManager, IPortletRenderer
from plone.portlets.utils import unhashPortletInfo

from plone.app.portlets.interfaces import IDeferredPortletRenderer
from plone.app.portlets.utils import assignment_from_key

from kss.core import CommandSet
from interfaces import IPloneCommands

class PloneCommands(CommandSet):
    implements(IPloneCommands)
    
    def issuePortalMessage(self, message, msgtype='info'):
        if message is None:
            message = ''

        if isinstance(message, Message):
            msgtype = message.type
            message = message.message

        # XXX The macro has to take in account that there might be more than
        # one status message.
        ksscore = self.getCommandSet('core')
        selector = ksscore.getHtmlIdSelector('kssPortalMessage')

        # We hide the standard Plone Portal Message
        standar_portal_message_selector = ksscore.getCssSelector('.portalMessage')
        ksscore.setStyle(standar_portal_message_selector, 'display','none')

        # Now there is always a portal message but it has to be
        # rendered visible or invisible, accordingly
        html = '<dt>%s</dt><dd>%s</dd>' % (msgtype, message)
        ksscore.replaceInnerHTML(selector, html)
        ksscore.setAttribute(selector, 'class', "portalMessage %s" % msgtype)
        ksscore.setStyle(selector, 'display', message and 'block' or 'none')

    def refreshPortlet(self, portlethash, **kw):
        # put parameters on the request, by saving the original context
        self.request.form, orig_form = kw, self.request.form
        
        # Prepare the portlet and render the data
        info = unhashPortletInfo(portlethash) 
        manager = getUtility(IPortletManager, info['manager'])
        
        assignment = assignment_from_key(context = self.context, 
                                         manager_name = info['manager'], 
                                         category = info['category'],
                                         key = info['key'],
                                         name = info['name'])
        renderer = getMultiAdapter(
                (self.context, self.request, self.view, manager, assignment.data),
                IPortletRenderer
            )
        renderer = renderer.__of__(self.context)
        
        renderer.update()
        if IDeferredPortletRenderer.providedBy(renderer):
            # if this is a deferred load, prepare now the data
            renderer.deferred_update()
        result = renderer.render()
        
        # Revert the original request
        self.request.form = orig_form
        
        # Command the replacement
        wrapper_id = 'portletwrapper-%s' % portlethash
        ksscore = self.getCommandSet('core')
        ksscore.replaceInnerHTML(ksscore.getHtmlIdSelector(wrapper_id), result)

    def refreshContentMenu(self):
        ksscore = self.getCommandSet('core')
        selector = ksscore.getHtmlIdSelector('contentActionMenus')
        self.getCommandSet('zope').refreshProvider(selector, 'plone.contentmenu')