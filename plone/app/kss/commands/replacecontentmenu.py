from kss.core.azaxview import AzaxViewAdapter


class ReplaceContentMenuCommand(AzaxViewAdapter):


    def replaceMenu(self):
        # render it
	menu_body = self.view.macroContent('global_contentviews/macros/content_actions')
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