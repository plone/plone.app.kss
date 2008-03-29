
from kss.demo.interfaces import (
    IKSSDemoResource,
    IKSSSeleniumTestResource,
    )
from kss.demo.resource import (
    KSSSeleniumTestSuite,
    KSSSeleniumTestDirectory,
    KSSSeleniumTestLayerBase,
    KSSSandboxCreationTestCase,
    )
from zope.interface import implements
     
# Create a mesh of provided interfaces
# This is needed, because an utility must have a single interface.
class IResource(IKSSDemoResource, IKSSSeleniumTestResource):
    pass


class myLayer(KSSSeleniumTestLayerBase):
    setup = KSSSandboxCreationTestCase('@@create_test_site')

class PloneDemos(object):
    implements(IResource)

    selenium_tests = (
        KSSSeleniumTestSuite(
            tests = KSSSeleniumTestDirectory('selenium_tests'),
            layer = myLayer,
            component = 'plone.app.kss',
            application = 'Plone',
            ),
        )
