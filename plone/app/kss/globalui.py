from zope import component
from zope.component import getMultiAdapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from kss.core.interfaces import IKSSView

from plone.app.kss.portlets import attributesModified

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def attributesTriggerPortalTabsReload(obj, view, event):
    import logging
    logger = logging.getLogger('KSS')
    logger.error('attributesTriggerPortalTabsReload event is buggy, need to fix')
    return
    triggeringAttributes = ('title', 'description')
    if attributesModified(triggeringAttributes, event):
        ksscore = view.getCommandSet('core')
        ksscore.replaceHTML(
            ksscore.getHtmlIdSelector('portal-globalnav'),
            view.macroContent('global_sections/macros/portal_tabs'),
            withKssSetup='False')

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def attributesTriggerDocumentBylineReload(obj, view, event):
    ksscore = view.getCommandSet('core')
    selector = ksscore.getHtmlIdSelector('plone-document-byline')
    zopecommands = view.getCommandSet('zope')
    zopecommands.refreshViewlet(selector,
                                'plone.belowcontenttitle',
                                'plone.belowcontenttitle.documentbyline')

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def attributesTriggerBreadcrumbsReload(obj, view, event):
    import logging
    logger = logging.getLogger('KSS')
    logger.error('attributesTriggerBreadcrumbsReload event is buggy, need to fix')
    return
    triggeringAttributes = ('title', 'description')
    if attributesModified(triggeringAttributes, event):
        ksscore = view.getCommandSet('core')
        ksscore.replaceHTML(
            ksscore.getHtmlIdSelector('portal-breadcrumbs'),
            view.macroContent('global_pathbar/macros/path_bar'),
            withKssSetup='False')

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def attributesTriggerHeadTitleReload(obj, view, event):
    triggeringAttributes = ('title', )
    if attributesModified(triggeringAttributes, event):
        htmlhead = getMultiAdapter((obj, view.request, view), name=u'plone.htmlhead')
        headtitle = getMultiAdapter((obj, view.request, view, htmlhead), name=u'plone.htmlhead.title')
        headtitle.update()
        ksscore = view.getCommandSet('core')
        ksscore.replaceHTML(
            'head title',
            headtitle.render(),
            withKssSetup='False')

