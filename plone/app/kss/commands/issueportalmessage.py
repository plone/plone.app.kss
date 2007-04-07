from kss.core.azaxview import AzaxViewAdapter

from Products.statusmessages.message import Message

type_css_map = {'info' : 'portalMessage',
                'warn' : 'portalWarningMessage',
                'error' : 'portalErrorMessage'}


class IssuePortalMessageCommand(AzaxViewAdapter):

    __allow_access_to_unprotected_subobjects__ = 1

    def issuePortalMessage(self, message, msgtype='portalMessage'):
        'Issue this portal message'
        if message is None:
            # allow message = None.
            message = ''

        if isinstance(message, Message):
            msgtype = message.type
            if type_css_map.has_key(msgtype):
                msgtype = type_css_map[msgtype]
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
        ksscore.replaceInnerHTML(selector, message) 
        #ksscore.setAttribute(selector, 'class', msgtype)
        ksscore.setStyle(selector, 'display', message and 'block' or 'none') 
