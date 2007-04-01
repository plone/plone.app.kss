from zope import component
from plone.app.portlets.portlets.navigation import INavigationPortlet
from plone.app.portlets.portlets.recent import IRecentPortlet
from plone.portlets.interfaces import IPortletManager

def generic_portlet_reloader(obj, view, event, interface):
    for manager in component.getAllUtilitiesRegisteredFor(IPortletManager):
        managerRenderer = manager(view.context, view.request, view)
        if not managerRenderer.visible:
            continue
        for p in managerRenderer.portletsToShow():
            if interface.providedBy(p['assignment']):
                view.getCommandSet('refreshportlet').refreshPortlet(p['hash'])

def navigation_portlet_reloader(obj, view, event):
    generic_portlet_reloader(obj, view, event, INavigationPortlet)

def recent_portlet_reloader(obj, view, event):
    generic_portlet_reloader(obj, view, event, IRecentPortlet)
