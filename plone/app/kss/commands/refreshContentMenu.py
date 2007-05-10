from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from kss.core import CommandSet
from plone.app.layout.globals.interfaces import IViewView
from zope.contentprovider.interfaces import IContentProvider

class KSSRefreshContentMenu(CommandSet):
    """
    Refresh a viewlet
    """

    def refreshContentMenu(self, id, name):
        alsoProvides(self.view, IViewView)
        contentMenu = getMultiAdapter((self.context, self.request, self.view), 
                                      IContentProvider, name=name)
        renderer = contentMenu.__of__(self.context)
        renderer.update()
        result = renderer.render()
        ksscore = self.getCommandSet('core')
        ksscore.replaceHTML(ksscore.getHtmlIdSelector(id), result)


