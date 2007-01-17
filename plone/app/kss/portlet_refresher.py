# -*- coding: UTF-8 -*-

from zope.interface import implements

from azaxview import AzaxBaseView
from interfaces import IPloneAzaxView

class PortletView(AzaxBaseView):

    # --
    # Portlet refresher actions
    # --

    implements(IPloneAzaxView)
    
    def refreshPortlet(self, name, nodeid=None):
        'Refresh portlet by name.'
        self.getCommandSet('refreshportlet').refreshPortlet(name, nodeid)
        return self.render()
