from zope.interface import Interface

class IIssuePortalMessageCommand(Interface):
    '''effects commands'''

class IRefreshPortletCommand(Interface):
    '''effects commands'''

class IKSSRefreshViewlet(Interface):
    '''commands to refresh a viewlet'''

class IKSSPlonePortletCommands(Interface):
    '''These are utility commands for doing stuff with portlets'''

    def reload_classic_portlet(css_selector, column,
                               template, portlet_macro='portlet'):
        '''Reload an old-school portlet'''

class IKSSRefreshContentMenu(Interface):
    '''Utility command for refreshing a content menu
    '''
