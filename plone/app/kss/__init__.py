from config import SKINS_DIR, GLOBALS
from Products.CMFCore.DirectoryView import registerDirectory, registerFileExtension
from Products.CMFCore.FSFile import FSFile

__all__ = ()

def initialize(context):

    # register directory views
    registerDirectory(SKINS_DIR, GLOBALS)

    # Register kss extension to allow it used from fs skins
    registerFileExtension('kss', FSFile)
