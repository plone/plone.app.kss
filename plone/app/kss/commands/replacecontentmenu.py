from kss.core.kssview import CommandSet

class ReplaceContentMenuCommand(CommandSet):
    """Mainly exists for backward compatibility with old hooks
    """
    def replaceMenu(self):
        self.getCommandSet('refreshprovider').refreshProvider('plone.contentmenu', '#portal-column-content div.contentActions')
