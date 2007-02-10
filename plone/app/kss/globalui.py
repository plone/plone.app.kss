from zope import component
from kss.core.interfaces import IKSSView
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def portal_tabs_reloader(obj, view, event):
    view.getCommandSet('core').replaceHTML(
        '#portal-globalnav',
        view.macroContent('global_sections/macros/portal_tabs'))

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def portal_breadcrumb_reloader(obj, view, event):
    view.getCommandSet('core').replaceHTML(
        '#portal-breadcrumbs',
        view.macroContent('global_pathbar/macros/path_bar'))

