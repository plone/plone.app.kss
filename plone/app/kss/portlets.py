from zope import component
from kss.core.interfaces import IAzaxEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

@component.adapter(IAzaxEvent)
def navigation_portlet_reloader(azax_event):
    orig_event = azax_event.event
    if not IObjectModifiedEvent.providedBy(orig_event):
        return
    attrs_that_need_updates = ('title', 'description')
    for description in orig_event.descriptions:
        for attr in attrs_that_need_updates:
            if attr in description.attributes:
                azax_event.view.getCommandSet('plone-portlets').reload_classic_portlet(
                    '#portlet-navigation-tree', 'plone.leftcolumn', 'portlet_navigation')

@component.adapter(IAzaxEvent)
def recent_portlet_reloader(azax_event):
    orig_event = azax_event.event
    if not IObjectModifiedEvent.providedBy(orig_event):
        return
    azax_event.view.getCommandSet('plone-portlets').reload_classic_portlet(
        '#portlet-recent', 'plone.leftcolumn', 'portlet_recent')

