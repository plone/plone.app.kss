from zope import component
from kss.core.interfaces import IAzaxEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

@component.adapter(IAzaxEvent)
def portal_tabs_reloader(azax_event):
    orig_event = azax_event.event
    if not IObjectModifiedEvent.providedBy(orig_event):
        return
    azax_event.view.getCommandSet('core').replaceHTML(
        '#portal-globalnav',
        azax_event.view.macroContent('global_sections/macros/portal_tabs'))

@component.adapter(IAzaxEvent)
def portal_breadcrumb_reloader(azax_event):
    orig_event = azax_event.event
    if not IObjectModifiedEvent.providedBy(orig_event):
        return
    azax_event.view.getCommandSet('core').replaceHTML(
        '#portal-breadcrumbs',
        azax_event.view.macroContent('global_pathbar/macros/path_bar'))

