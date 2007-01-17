'''\
Procedural methods of site setup

To replace code that used to be in Extensions/Install
'''

from Products.CMFCore.utils import getToolByName

def setupMimetype(context):
    '''This setup step is needed after Archetypes has been installed.
    '''
    site = context.getSite()
    # register mimetype
    mt = getToolByName(site, 'mimetypes_registry')
    mt.manage_addMimeType('KSS (Kinetic Style Sheet)', ('text/kss', ), ('kss', ), 'text.png',
                       binary=0, globs=('*.kss', ))
