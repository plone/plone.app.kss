'''\
Procedural methods of site setup
'''

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName


def setupMimetype(context):
    '''This setup step is needed after Archetypes has been installed.
    '''
    site = context.getSite()
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('plone-app-kss.txt') is None:
        return
    # register mimetype
    mt = getToolByName(site, 'mimetypes_registry')
    mt.manage_addMimeType('KSS (Kinetic Style Sheet)', ('text/kss', ), ('kss', ), 'text.png',
                       binary=0, globs=('*.kss', ))


def addCacheForResourceRegistry(context):
    ram_cache_id = 'ResourceRegistryCache'
    site = context.getSite()
    if ram_cache_id in site:
        cache = getattr(site, ram_cache_id)
        settings = cache.getSettings()
        settings['max_age'] = 24 * 3600  # keep for up to 24 hours
        settings['request_vars'] = ('URL', )
        cache.manage_editProps('Cache for saved ResourceRegistry files', settings)

    reg = getToolByName(site, 'portal_kss', None)
    if reg is not None and getattr(aq_base(reg), 'ZCacheable_setManagerId', None) is not None:
        reg.ZCacheable_setManagerId(ram_cache_id)
        reg.ZCacheable_setEnabled(1)
