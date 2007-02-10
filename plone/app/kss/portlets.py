from zope import component
from kss.core.interfaces import IKSSView
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def navigation_portlet_reloader(obj, view, event):
    attrs_that_need_updates = ('title', 'description')
    for description in event.descriptions:
        for attr in attrs_that_need_updates:
            if attr in description.attributes:
                view.getCommandSet('plone-portlets').reload_classic_portlet(
                    '#portlet-navigation-tree', 'plone.leftcolumn', 'portlet_navigation')

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def recent_portlet_reloader(obj, view, event):
    view.getCommandSet('plone-portlets').reload_classic_portlet(
        '#portlet-recent', 'plone.leftcolumn', 'portlet_recent')
