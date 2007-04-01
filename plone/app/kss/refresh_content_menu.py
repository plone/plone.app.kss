# -*- coding: UTF-8 -*-
from zope.interface import implements
from azaxview import AzaxBaseView
from kss.core import kssaction
from interfaces import IPloneAzaxView

class ContentMenuView(AzaxBaseView):

    # --
    # ContentMenu in-place refreshment
    # --

    implements(IPloneAzaxView)

    @kssaction
    def contentMenuRefresh(self, id, menu):
        self.getCommandSet('contentmenu').refreshContentMenu(id, menu)

