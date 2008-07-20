from kss.core.interfaces import IKSSView
import zope.deferredimport

zope.deferredimport.deprecated(
    "It has moved to Products.CMFPlone.interfaces.IPloneSiteRoot "
    "This reference will be gone in plone.app.kss 1.6",
    IPloneSiteRoot = 'Products.CMFPlone.interfaces:IPloneSiteRoot',
    )

zope.deferredimport.deprecated(
    "You better use OFS.interfaces.IFolder"
    "This reference will be gone in plone.app.kss 1.6",
    IFolderish = 'OFS.interfaces:IFolder',
    )


zope.deferredimport.deprecated(
    "You better use OFS.interfaces.ISimpleItem"
    "This reference will be gone in plone.app.kss 1.6",
    IContentish = 'OFS.interfaces:ISimpleItem',
    )

zope.deferredimport.deprecated(
    "You better use OFS.interfaces.IItem"
    "This reference will be gone in plone.app.kss 1.6",
    IPortalObject = 'OFS.interfaces:IItem',
    )


class IPloneKSSView(IKSSView):
    '''View for Plone'''
