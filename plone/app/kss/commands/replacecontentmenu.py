from kss.core.azaxview import AzaxViewAdapter

class ReplaceContentMenuCommand(AzaxViewAdapter):
    """Mainly exists for backward compatibility with old hooks
    """
    def replaceMenu(self):
        self.getCommandSet('refreshprovider').refreshProvider('plone.contentmenu', '#portal-column-content div.contentActions')
