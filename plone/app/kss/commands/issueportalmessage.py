from kss.core import force_unicode
from kss.core.azaxview import AzaxViewAdapter

class IssuePortalMessageCommand(AzaxViewAdapter):
    __allow_access_to_unprotected_subobjects__ = 1
    
    def issuePortalMessage(self, message):
        'Issue this portal message'
        if message:
            message = self.view.translateMessage(message)
            message = force_unicode(message, 'utf')
        else:
            # allow message = None.
            message = ''
        # XXX David: The macro has to take in account that there might be more
        # than one status message.
        # XXX David: The macro does not take in account the type of the portal message
        ksscore = self.getCommandSet('core')
        ksscore.replaceInnerHTML(ksscore.getHtmlIdSelector('kssPortalMessage'), message) 
        # Now there is always a portal message but it has to be
        # rendered visible or invisible, accordingly
        ksscore.setStyle(ksscore.getHtmlIdSelector('kssPortalMessage'), 
            'display', message and 'block' or 'none') 
