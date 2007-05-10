# -*- coding: UTF-8 -*-
from zope.interface import implements
from plonekssview import PloneKSSView

from kss.core import kssaction
from interfaces import IPloneKSSView

class ContentMenuView(PloneKSSView):

    # --
    # ContentMenu in-place refreshment
    # --

    implements(IPloneKSSView)

    @kssaction
    def contentMenuRefresh(self, id, menu):
        self.getCommandSet('contentmenu').refreshContentMenu(id, menu)

