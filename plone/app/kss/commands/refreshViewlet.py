from kss.core import CommandSet
from zope.viewlet.interfaces import IViewlet
from zope.component import getMultiAdapter

class KSSRefreshViewlet(CommandSet):
    """
    Refresh a viewlet
    """

    def refreshViewlet(self, id, manager, name):
        renderer = getMultiAdapter((self.context, self.request, self.view, manager),
                                  IViewlet,
                                  name=name)
        renderer = renderer.__of__(self.context)
        renderer.update()

        result = renderer.render()
        ksscore = self.getCommandSet('core')
        ksscore.replaceHTML(ksscore.getHtmlIdSelector(id), result)

